# Búsqueda de Antecedentes Marcarios

## Objetivo

Organizar una búsqueda previa razonable antes de avanzar con clases y redacción final.

## Orden de análisis

1. Buscar la marca exacta.
2. Buscar variantes ortográficas.
3. Buscar variantes fonéticas.
4. Buscar términos dominantes del signo.
5. Revisar clases iguales y cercanas.

Antes de buscar, ejecute `tools/prepare_prior_search.py` para generar variantes y una matriz base de registro.

## Registro de hallazgos

Por cada resultado relevante incluir:

- signo encontrado;
- clase;
- similitud;
- comentario de riesgo;
- URL verificable;
- recomendación.

## Criterio

No hace falta encontrar una oposición segura para frenar el caso. Basta con detectar una cercanía seria para marcar riesgo.

## Salida recomendada

- Tabla de antecedentes.
- Conclusión ejecutiva breve.
- Semáforo:
  - verde;
  - amarillo;
  - rojo.
- URLs oficiales o verificables por cada resultado consignado.

## Cierre obligatorio

```text
STOP_FOR_USER
NEXT_ACTION: Revise los antecedentes detectados y confirme si desea continuar con esta marca o reformularla.
```
