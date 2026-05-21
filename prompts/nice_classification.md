# Clasificación Niza

## Objetivo

Traducir el negocio del usuario a una o más clases concretas y defendibles.

## Instrucciones

1. Lea el `IntakeMarca.json`.
2. Identifique qué ofrece realmente el titular.
3. Separe producto descargable, software en línea, intermediación comercial y servicio profesional.
4. Use `tools/suggest_nice_classes.py` como punto de partida, no como decisión final.
5. Explique por qué cada clase sugerida corresponde.
6. Señale clases alternativas o complementarias si hay dudas reales.

## Formato de salida

Generar:

- `MarcaINPI/Borradores/ClasesSugeridas.json`
- `MarcaINPI/Borradores/ClasesSugeridas.md`

Cada clase debe incluir:

- número;
- puntaje o prioridad;
- motivo;
- advertencia;
- ejemplos de productos o servicios compatibles.

## Cierre obligatorio

```text
STOP_FOR_USER
NEXT_ACTION: Confirme la clase o clases seleccionadas antes de redactar productos y servicios.
```
