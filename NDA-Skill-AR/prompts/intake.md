# Relevamiento Inicial NDA

## Objetivo

Recolectar el contexto mínimo del acuerdo.

## Preguntas mínimas

1. ¿Quiénes son las partes?
2. ¿Para qué se compartirá la información?
3. ¿El NDA es unilateral o mutuo?
4. ¿Qué tipo de información se compartirá?
5. ¿Habrá acceso a código, datos, pricing o clientes?
6. ¿Qué plazo o duración se imagina?
7. ¿Cómo se firmará el documento?

## Formato de salida

- `AcuerdoConfidencialidad/Borradores/IntakeNDA.json`
- `AcuerdoConfidencialidad/Borradores/IntakeNDA.md`

## JSON sugerido

```json
{
  "party_a": "",
  "party_b": "",
  "nda_type": "",
  "purpose": "",
  "confidential_assets": [],
  "term_summary": "",
  "signature_mode": "",
  "notes": ""
}
```

## Cierre obligatorio

```text
STOP_FOR_USER
NEXT_ACTION: Confirme partes, tipo de NDA, propósito y activos confidenciales antes de seguir.
```
