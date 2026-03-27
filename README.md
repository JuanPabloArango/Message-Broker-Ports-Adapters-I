# Reto: Sistema de Delivery de Paquetes

## Contexto

Una empresa de mensajería necesita gestionar el ciclo de vida de sus envíos. Cuando un remitente es verificado puede crear paquetes. Cada paquete debe ser asignado a un conductor disponible. Cuando el conductor entrega el paquete, el remitente debe ser notificado por un sistema externo.

---

## Los tres agregados

**`Sender`** — el remitente
- Puede estar pendiente de verificación o verificado
- Solo un `Sender` verificado puede crear paquetes

**`Package`** — el paquete
- Estados: `PENDING` → `ASSIGNED` → `IN_TRANSIT` → `DELIVERED`
- El estado nunca puede retroceder
- Solo puede ser asignado a un conductor disponible

**`Driver`** — el conductor
- Puede estar disponible u ocupado
- Solo puede llevar un paquete a la vez

---

## Invariantes de negocio

```
Sender:
  - No puede crear paquetes si no está verificado

Package:
  - No puede asignarse si ya tiene conductor
  - No puede entregarse si no está en tránsito

Driver:
  - No puede aceptar un paquete si ya lleva uno
```

---

## Eventos de dominio a modelar

| Operación | Evento |
|---|---|
| Sender verificado | `SenderVerified` |
| Paquete creado | `PackageCreated` |
| Conductor asignado | `DriverAssigned` |
| Paquete en tránsito | `PackageInTransit` |
| Paquete entregado | `PackageDelivered` |
| Conductor liberado | `DriverFreed` |

---

## El flujo EDA completo

```
Sistema externo (verificación de identidad)
  → mensaje en broker: "sender.verified"
    → SenderVerifiedListener
      → bus.handle(VerifySender)
        → Sender.verify()
          → emite SenderVerified
            → handler: notifica al sender por mail


Sender hace POST /packages
  → bus.handle(CreatePackage)
    → valida que Sender esté verificado
    → Package.create()
      → emite PackageCreated
        → handler: bus.handle(AssignDriver)  ← event → command
          → busca Driver disponible
          → Driver.assign()  → emite DriverAssigned
          → Package.assign() → emite PackageInTransit


Sistema externo (GPS del conductor)
  → mensaje en broker: "package.delivered"
    → PackageDeliveredListener
      → bus.handle(ConfirmDelivery)
        → Package.deliver() → emite PackageDelivered
          → handler: bus.handle(FreeDriver)
            → Driver.free() → emite DriverFreed
              → handler: publica notificación al broker
```

---

## Etapas sugeridas

**Etapa 1** — Modelar el dominio

Agregados, value objects, invariantes, eventos. Sin infraestructura.

**Etapa 2** — Message Bus interno

Comandos, handlers, event handlers encadenados (`PackageCreated → AssignDriver`).

**Etapa 3** — HTTP + Message Broker

Dos endpoints POST (`/senders`, `/packages`) + dos subscribers externos
(`sender.verified`, `package.delivered`). Patrón Flask API + Event Subscriber.

**Etapa 4** — Outbox Pattern

Garantizar que `PackageDelivered` nunca se pierda aunque el broker caiga.

---

## Lo que ejercita

- Invariantes entre agregados (Sender debe estar verificado antes de crear Package)
- Cadena Event → Command → Event (PackageCreated → AssignDriver → DriverAssigned)
- Entrada desde broker externo (GPS) + salida hacia broker externo (notificación)
- Patrón Flask API + Event Subscriber
- Outbox Pattern para garantía de entrega
