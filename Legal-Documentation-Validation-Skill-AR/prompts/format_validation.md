# Revisión de formato

La skill debe controlar señales formales frecuentes:

- fechas;
- moneda;
- identificadores;
- expedientes;
- tamaño de página si hay PDF.

## Criterios

- Detectar fechas numéricas ambiguas como `05/06/2026`.
- Detectar monedas extranjeras o formatos mixtos si no están justificados.
- Detectar CUIT/CUIL si el documento debería incluirlos.
- Si hay PDF, verificar si la página parece A4.

## Regla

No asumir que un formato distinto es inválido en todos los casos. La skill debe marcar `revisar` cuando el contexto pueda justificarlo.
