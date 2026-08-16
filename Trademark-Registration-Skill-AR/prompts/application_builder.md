# Armado del Borrador de Solicitud

## Objetivo

Consolidar todos los datos del caso en un único documento claro para revisión o carga manual.

## Insumos esperados

- `IntakeMarca.json`
- `ClasesSugeridas.json`
- `ProductosServicios.json`
- `BusquedaAntecedentes.json` si existe

## Contenido mínimo del borrador

- marca exacta;
- tipo de signo;
- titular;
- CUIT/CUIL;
- domicilio;
- correo;
- clases seleccionadas;
- productos/servicios por clase;
- prioridad extranjera si aplica;
- reivindicación de color si aplica;
- resumen de búsqueda de antecedentes;
- advertencias o decisiones pendientes.

## Regla de salida

Si el caso tiene varias clases, el agente debe generar:

- un índice general del caso, y
- una solicitud separada por clase.

## Requisito

Si el caso tiene riesgo alto por antecedentes, el borrador debe decirlo explícitamente.

## Salida

- `MarcaINPI/Borradores/SolicitudMarca.json`
- `MarcaINPI/Borradores/SolicitudMarca.md`
- `MarcaINPI/Borradores/SolicitudMarca_ClaseNN.md`

## Cierre obligatorio

```text
STOP_FOR_USER
NEXT_ACTION: Revise el borrador completo de la solicitud y confirme antes de presentar ante el INPI.
```
