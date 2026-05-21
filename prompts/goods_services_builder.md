# Redacción de Productos y Servicios

## Objetivo

Construir una descripción usable por clase, sin exagerar ni dejar vacíos relevantes.

## Reglas

- Redacte por clase.
- Describa solo lo que el titular ofrece o planea ofrecer razonablemente.
- Evite copiar listados interminables si el negocio es simple.
- Mantenga una redacción profesional y clara.
- Si la clase es 9, 35, 36, 41 o 42, contraste la propuesta con `references/class_templates.md`.
- Si el caso es tech, distinga entre:
  - software descargable;
  - SaaS/PaaS;
  - servicios comerciales;
  - educación;
  - pagos;
  - telecomunicaciones.

## Formato de salida

Generar:

- `MarcaINPI/Borradores/ProductosServicios.json`
- `MarcaINPI/Borradores/ProductosServicios.md`

Puede usar `tools/build_goods_services_draft.py` para generar una primera versión editable.

## JSON sugerido

```json
{
  "classes": [
    {
      "class_number": 42,
      "description": "",
      "reason": ""
    }
  ]
}
```

## Cierre obligatorio

```text
STOP_FOR_USER
NEXT_ACTION: Confirme la redacción final de productos y servicios antes de consolidar la solicitud.
```
