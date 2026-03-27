# Observabilidad sin violar SRP: el patrón Decorator

## El problema

Un use case que mezcla lógica de negocio con observabilidad tiene **dos razones para cambiar**,
violando SRP (la S de SOLID).

```
execute():
  ┌─ OBSERVABILIDAD ──────────────────────────────────┐
  │  start_span(...)                                   │
  │  start_time = time.time()                          │
  │                                                    │
  │  ┌─ NEGOCIO ──────────────────────────────────┐   │
  │  │  course = uow.course_repository.get(...)   │   │
  │  │  if not course: raise CourseNotFoundError  │   │
  │  │  course.add_lesson(...)                    │   │
  │  │  uow.commit()                              │   │
  │  └────────────────────────────────────────────┘   │
  │                                                    │
  │  logger.log(INFO, "...")                           │
  │  tracer.set_status(OK)                             │
  │  except: logger.log(ERROR, "...")                  │
  │           tracer.record_exception(...)             │
  │  finally: metrics.increment_counter(...)           │
  │           metrics.record_histogram(...)            │
  └────────────────────────────────────────────────────┘
```

La observabilidad **envuelve** al negocio como una cebolla. El patrón Decorator modela exactamente esa forma.

---

## Parte 1: El servicio puro (sólo negocio)

```python
class AddLessonService:
    """Una sola razón para cambiar: la lógica de negocio de añadir una lección."""

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    def execute(self, course_id: int, title: str, content: Dict[str, str], minutes: int) -> None:
        with self._uow as uow:
            course = uow.course_repository.get(course_id=course_id)
            if not course:
                raise CourseNotFoundError("No fue hallado el curso al cual se asociará la lección.")
            course.add_lesson(title=title, content=content, duration=Duration(minutes))
            uow.commit()
```

Sin `logger`, sin `metrics`, sin `tracer`. Si la regla de negocio cambia, sólo cambia esto.

---

## Parte 2: El decorator (sólo observabilidad)

```python
# infrastructure/observability/instrumented_add_lesson.py
#
# Una sola razón para cambiar: cómo se observa esta operación.
# Implementa la misma interfaz que AddLessonService.

class InstrumentedAddLessonService:

    def __init__(
        self,
        service: AddLessonService,   # <── recibe el servicio real
        logger: Logger,
        metrics: Metrics,
        tracer: Tracer,
    ) -> None:
        self._service = service
        self._logger = logger
        self._metrics = metrics
        self._tracer = tracer

    def execute(self, course_id: int, title: str, content: Dict[str, str], minutes: int) -> None:
        success = False
        start_time = time.time()

        with self._tracer.start_span(name="internal.add_lesson", kind=Kind.INTERNAL):
            try:
                self._service.execute(course_id, title, content, minutes)  # delega

                success = True
                self._logger.log(LogLevel.INFO, f"Se asoció una nueva lección al curso {course_id}")
                self._tracer.set_status(status=Code.OK)

            except Exception as e:
                self._logger.log(LogLevel.ERROR, message="No fue posible crear la lección.")
                self._tracer.record_exception(exception=e)
                self._tracer.set_status(status=Code.ERROR, description=f"Error al asociar la lección al curso {course_id}")
                raise

            finally:
                elapsed = time.time() - start_time
                self._metrics.increment_counter("internal.create_lesson.duration", {"success": success})
                self._metrics.record_histogram("internal.create_lesson.duration", elapsed, "ms", {"success": success})
```

Si mañana quieres cambiar a Datadog en vez de OpenTelemetry, sólo cambia esto. El negocio no se toca.

---

## Parte 3: El wiring en el contenedor DI

```python
# infrastructure/container.py  (o donde armes tu grafo de dependencias)

# 1. El servicio puro
service = AddLessonService(uow=sql_unit_of_work)

# 2. Lo envuelves con observabilidad
service = InstrumentedAddLessonService(
    service=service,
    logger=structlog_logger,
    metrics=prometheus_metrics,
    tracer=otel_tracer,
)

# 3. El caller usa `service.execute(...)` sin saber qué hay adentro.
#    La interfaz es idéntica.
```

---

## Escalado: Generic Decorator

Si tienes 10 use cases, tendrías 10 `InstrumentedXxxService` con código casi idéntico.
La solución es un **Generic Decorator**:

```python
# Una sola clase para observar CUALQUIER servicio que tenga .execute()

class InstrumentedService:
    def __init__(self, service, operation_name: str, logger, metrics, tracer):
        self._service = service
        self._operation_name = operation_name
        self._logger = logger
        self._metrics = metrics
        self._tracer = tracer

    def execute(self, *args, **kwargs):
        success = False
        start = time.time()
        with self._tracer.start_span(name=self._operation_name, kind=Kind.INTERNAL):
            try:
                result = self._service.execute(*args, **kwargs)
                success = True
                self._logger.log(LogLevel.INFO, f"{self._operation_name} completed")
                self._tracer.set_status(Code.OK)
                return result
            except Exception as e:
                self._logger.log(LogLevel.ERROR, f"{self._operation_name} failed")
                self._tracer.record_exception(e)
                self._tracer.set_status(Code.ERROR)
                raise
            finally:
                elapsed = time.time() - start
                self._metrics.record_histogram(
                    f"{self._operation_name}.duration", elapsed, "ms", {"success": success}
                )


# Wiring para todos tus servicios:
add_lesson  = InstrumentedService(AddLessonService(uow),  "internal.add_lesson",  ...)
add_course  = InstrumentedService(AddCourseService(uow),  "internal.add_course",  ...)
add_student = InstrumentedService(AddStudentService(uow), "internal.add_student", ...)
```

---

## Cuándo ir al siguiente nivel: Message Bus con Middleware

Si además usas un **Message Bus**, ni siquiera necesitas `InstrumentedService`.
El bus aplica observabilidad a todos los handlers automáticamente en el `dispatch`:

```python
bus = QueryBus(middlewares=[
    LoggingMiddleware(logger),
    TracingMiddleware(tracer),
    MetricsMiddleware(metrics),
])

bus.register(AddLessonCommand, AddLessonService(uow))
bus.register(AddCourseCommand, AddCourseService(uow))
# Todos los handlers heredan observabilidad. Agregar uno nuevo no requiere pensar en esto.
```

---

## Resumen de patrones

| Patrón | Cuando usarlo |
|---|---|
| **Decorator específico** (`InstrumentedAddLessonService`) | Observabilidad diferente por use case |
| **Generic Decorator** (`InstrumentedService`) | Observabilidad uniforme, múltiples use cases |
| **Middleware Bus** | CQRS estricto; zero-friction al agregar handlers |
| **AOP `@decorated`** | Apps pequeñas, equipos que priorizan simplicidad |
