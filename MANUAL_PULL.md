# Manual Pull en Cloud Pub/Sub

## Conceptos base

En Cloud Pub/Sub existen dos entidades separadas:

- **Topic**: canal donde se publican mensajes (`projects/{project}/topics/{topic}`)
- **Subscription**: punto de entrega de mensajes a un consumidor (`projects/{project}/subscriptions/{sub}`)

Un topic puede tener múltiples subscriptions. Cada subscription recibe una copia independiente de todos los mensajes publicados en el topic.

---

## Modos de entrega

### Push (subscriber constante)

Pub/Sub llama a un endpoint HTTP tuyo cada vez que llega un mensaje. No tienes control sobre el timing.

```
[Mensaje publicado] → Pub/Sub → POST https://tu-servicio.com/handler
```

### Pull (consulta manual)

Tu código decide **cuándo** pedir mensajes al broker. El broker los retiene hasta que los pidas o hasta que expiren.

```
[Mensaje publicado] → Pub/Sub lo retiene
                            ↑
              tu código hace pull cuando quiere
```

Este segundo modo es el relevante para el patrón de cola de espera.

---

## Configuración en GCP

### 1. Crear el topic de espera

```bash
gcloud pubsub topics create waiting-shipments
```

### 2. Crear la subscription con retención extendida

La clave es configurar la subscription para que los mensajes **no expiren rápido** y no se reentreguen solos:

```bash
gcloud pubsub subscriptions create waiting-shipments-sub \
  --topic=waiting-shipments \
  --ack-deadline=60 \
  --message-retention-duration=7d \
  --expiration-period=never
```

| Parámetro | Por qué importa |
|-----------|-----------------|
| `--ack-deadline=60` | Pub/Sub espera 60s tu ACK antes de redelivery |
| `--message-retention-duration=7d` | Los mensajes sobreviven 7 días sin ser consumidos |
| `--expiration-period=never` | La subscription no se borra por inactividad |

---

## Publicar en la cola de espera

Cuando `DriverAssignment` no encuentra conductores disponibles, publicas el envío pendiente:

```python
from google.cloud import pubsub_v1
import json

publisher = pubsub_v1.PublisherClient()
TOPIC = "projects/{project_id}/topics/waiting-shipments"

def publish_waiting_shipment(shipment_id: str, payload: dict) -> None:
    data = json.dumps(payload).encode("utf-8")
    future = publisher.publish(
        TOPIC,
        data=data,
        shipment_id=shipment_id,   # atributo para filtrar si hace falta
    )
    future.result()  # bloquea hasta confirmar la publicación
```

---

## Hacer pull manual desde el handler de DriverFreed

Este es el núcleo del patrón. El handler de `DriverFreed` consulta activamente la cola de espera:

```python
from google.cloud import pubsub_v1
import json

subscriber = pubsub_v1.SubscriberClient()
SUBSCRIPTION = "projects/{project_id}/subscriptions/waiting-shipments-sub"

class DriverFreedHandler:

    def handle(self, event) -> None:
        # 1. Marcar conductor como disponible (lógica de dominio)
        driver = self.driver_repo.find(event.driver_id)
        driver.mark_as_available()

        # 2. Intentar tomar un envío pendiente
        shipment = self._pull_one_waiting_shipment()
        if shipment:
            driver.assign(shipment["shipment_id"])

    def _pull_one_waiting_shipment(self) -> dict | None:
        response = subscriber.pull(
            request={
                "subscription": SUBSCRIPTION,
                "max_messages": 1,   # solo uno por conductor liberado
            }
        )

        if not response.received_messages:
            return None

        msg = response.received_messages[0]

        # ACK: le dice a Pub/Sub que ya procesamos el mensaje
        subscriber.acknowledge(
            request={
                "subscription": SUBSCRIPTION,
                "ack_ids": [msg.ack_id],
            }
        )

        return json.loads(msg.message.data.decode("utf-8"))
```

### ¿Qué pasa si NO haces ACK?

Si el handler falla antes del ACK, Pub/Sub reentrega el mensaje después de que vence el `ack-deadline`. El envío vuelve a la cola de espera automáticamente.

---

## Flujo completo

```
[Orden llega, conductores ocupados]
        ↓
DriverAssignment.execute([]) → None
        ↓
publish_waiting_shipment(shipment_id, payload)
        ↓
Pub/Sub retiene el mensaje en "waiting-shipments-sub"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Conductor termina su entrega]
        ↓
Se publica evento DriverFreed
        ↓
DriverFreedHandler.handle(event)
        ├── driver.mark_as_available()
        └── _pull_one_waiting_shipment()
                ↓
            Pub/Sub entrega el mensaje más antiguo
                ↓
            driver.assign(shipment_id)
            subscriber.acknowledge(ack_id)
```

---

## Puntos importantes

**El orden está garantizado (con condiciones)**

Pub/Sub no garantiza orden por defecto. Si necesitas FIFO estricto (atender envíos en el orden en que llegaron), debes habilitar mensajes ordenados al crear la subscription y usar un `ordering_key` al publicar:

```bash
gcloud pubsub subscriptions create waiting-shipments-sub \
  --topic=waiting-shipments \
  --enable-message-ordering
```

```python
publisher.publish(TOPIC, data=data, ordering_key="shipments")
```

**Concurrencia: dos conductores liberados al mismo tiempo**

Si dos eventos `DriverFreed` ocurren simultáneamente, cada handler llama a `pull(max_messages=1)` por separado. Pub/Sub garantiza que un mismo mensaje no se entrega a dos pulls concurrentes, por lo que cada conductor tomará un envío distinto.

**La subscription no necesita un listener activo**

A diferencia de un subscriber push, esta subscription puede estar "dormida" días sin problema. Los mensajes se acumulan y esperan. Solo se consumen cuando un `DriverFreed` dispara el pull.
