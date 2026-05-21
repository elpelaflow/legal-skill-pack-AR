# Relevamiento Inicial de Marca

## Objetivo

Recolectar los datos esenciales del caso antes de buscar antecedentes o sugerir clases.

## Preguntas mínimas

1. ¿Cuál es la marca exacta a registrar?
2. ¿La marca es denominativa, mixta, figurativa u otra?
3. ¿Quién será el titular?
4. ¿Qué producto o servicio identifica la marca?
5. ¿La actividad ya está en marcha o es un lanzamiento próximo?
6. ¿Dónde se usa o se usará la marca?
7. ¿Hay logo? ¿Se quiere proteger con o sin color?
8. ¿Existe una solicitud o registro previo en otro país?

## Formato de salida

Generar:

- `MarcaINPI/Borradores/IntakeMarca.json`
- `MarcaINPI/Borradores/IntakeMarca.md`

## JSON sugerido

```json
{
  "brand_name": "",
  "brand_type": "",
  "holder_name": "",
  "holder_id": "",
  "holder_country": "Argentina",
  "holder_address": "",
  "contact_email": "",
  "business_summary": "",
  "current_offering": [],
  "channels": [],
  "has_logo": false,
  "claims_color": false,
  "foreign_priority": false,
  "priority_details": "",
  "notes": ""
}
```

## Cierre obligatorio

Termine con:

```text
STOP_FOR_USER
NEXT_ACTION: Confirme la identidad exacta de la marca, el titular y el tipo de signo antes de seguir.
```
