# Relevamiento Inicial AAIP

## Objetivo

Recolectar el contexto mínimo del responsable y del tratamiento.

## Preguntas mínimas

1. ¿Quién es el responsable?
2. ¿Qué hace la empresa?
3. ¿Qué productos o sistemas utiliza?
4. ¿Qué categorías de titulares trata?
5. ¿Qué tipos de datos personales usa?
6. ¿Dónde se almacenan o procesan?
7. ¿Qué proveedores o terceros intervienen?
8. ¿Hay datos sensibles, financieros, biométricos o de menores?

## Formato de salida

Generar:

- `RegistroDatosAAIP/Borradores/IntakeAAIP.json`
- `RegistroDatosAAIP/Borradores/IntakeAAIP.md`

## JSON sugerido

```json
{
  "controller_name": "",
  "controller_id": "",
  "controller_address": "",
  "controller_country": "Argentina",
  "contact_email": "",
  "business_activity": "",
  "systems": [],
  "data_subject_groups": [],
  "data_categories": [],
  "sensitive_data": false,
  "minor_data": false,
  "vendors": [],
  "hosting_locations": [],
  "notes": ""
}
```

## Cierre obligatorio

```text
STOP_FOR_USER
NEXT_ACTION: Confirme el responsable, sistemas, titulares y categorías de datos antes de seguir.
```
