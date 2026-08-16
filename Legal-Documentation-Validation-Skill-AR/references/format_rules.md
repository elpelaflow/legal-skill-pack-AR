# Reglas de formato

## Fechas

Señales que conviene revisar:

- fechas ambiguas tipo `05/06/2026`;
- meses en inglés;
- mezcla de varios formatos sin criterio claro.

## Moneda

Señales que conviene revisar:

- mezcla de `ARS`, `$`, `USD` o `US$` sin aclaración;
- moneda extranjera en documentos que deberían estar solo en pesos y sin justificación;
- formato decimal inconsistente.

## Identificadores

Cuando el documento lo requiera, la skill debe observar si faltan o están incompletos:

- CUIT/CUIL;
- razón social;
- expediente o solicitud;
- clase o número registral;
- datos del responsable.

## PDF

Si existe PDF y la librería disponible permite leer tamaño de página, la skill debe verificar si cada hoja coincide razonablemente con A4:

- ancho aproximado: 210 mm
- alto aproximado: 297 mm

Si no puede leerse el PDF, debe dejar la validación como `pendiente`.
