# Relevamiento Inicial del Contrato

## Objetivo

Recolectar el contexto mínimo del vínculo contractual.

## Preguntas mínimas

1. ¿Quién contrata y quién desarrolla?
2. ¿Qué se va a construir?
3. ¿Es proyecto cerrado, evolutivo o por horas?
4. ¿Cuál es el objetivo del cliente?
5. ¿Hay fecha o plazo clave?
6. ¿El cliente espera código fuente, acceso a repo o sólo entregable ejecutable?
7. ¿Hay anticipo, hitos o mensualidad?
8. ¿Cómo se imagina la propiedad intelectual?

## Formato de salida

- `ContratoDesarrolloSoftware/Borradores/IntakeContrato.json`
- `ContratoDesarrolloSoftware/Borradores/IntakeContrato.md`

## JSON sugerido

```json
{
  "client_name": "",
  "provider_name": "",
  "project_name": "",
  "project_summary": "",
  "engagement_model": "",
  "timeline_summary": "",
  "deliverable_expectation": "",
  "payment_model": "",
  "ip_expectation": "",
  "personal_data_access": false,
  "notes": ""
}
```

## Cierre obligatorio

```text
STOP_FOR_USER
NEXT_ACTION: Confirme partes, proyecto, modalidad y expectativa de propiedad intelectual antes de seguir.
```
