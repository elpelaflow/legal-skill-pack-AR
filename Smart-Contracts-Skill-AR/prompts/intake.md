# Relevamiento Inicial

## Objetivo

Recolectar el contexto mínimo del acuerdo o negocio automatizable.

## Preguntas mínimas

1. ¿Qué relación o negocio se quiere automatizar?
2. ¿Qué partes intervienen?
3. ¿Qué evento gatilla la ejecución?
4. ¿Qué se transfiere, bloquea o libera?
5. ¿Qué blockchain o entorno se usaría?
6. ¿Hace falta un oráculo o dato externo?
7. ¿Qué parte no debería automatizarse?

## Formato de salida

- `SmartContractSpecAR/Borradores/IntakeSmartContract.json`
- `SmartContractSpecAR/Borradores/IntakeSmartContract.md`

## JSON sugerido

```json
{
  "project_name": "",
  "parties": [],
  "business_purpose": "",
  "automated_action": "",
  "assets_involved": [],
  "blockchain_target": "",
  "external_dependencies": [],
  "notes": ""
}
```

## Cierre obligatorio

```text
STOP_FOR_USER
NEXT_ACTION: Confirme el negocio, la acción automatizada y las dependencias externas antes de seguir.
```
