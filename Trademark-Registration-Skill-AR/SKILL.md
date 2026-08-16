---
name: registro-marca-inpi-argentina
description: >
  Genera materiales preparatorios para solicitudes de registro de marca ante el INPI Argentina.
  Uso: búsqueda de antecedentes marcarios, clasificación Niza, redacción de productos y servicios,
  armado de formularios y revisión documental para marcas de startups, software, ecommerce y servicios digitales.
metadata:
  short-description: Preparación guiada de solicitudes de marca INPI Argentina
---

# Registro de Marca (INPI Argentina)

Este skill organiza la preparación de una solicitud marcaria ante el INPI Argentina con foco en:

- búsqueda previa de antecedentes;
- elección de clase o clases Niza;
- redacción de productos y servicios;
- consistencia de datos del titular y del signo;
- generación de borradores listos para revisión humana.

- **Directorio de salida:** `MarcaINPI/` en el directorio de trabajo actual.
- **Flujo:** Relevamiento -> Búsqueda previa -> Clasificación -> Productos/Servicios -> Solicitud por clase -> Revisión final.
- **Objetivo:** Reducir errores frecuentes antes de cargar la presentación en el portal del INPI.
- **Límite:** No garantiza registrabilidad ni sustituye estrategia profesional ante conflictos, oposiciones o signos débiles.
- **Regla operativa crítica:** Si hay más de una clase, generar un borrador de solicitud separado por cada clase.

## Puertas de Confirmación Obligatoria (STOP_FOR_USER)

El agente debe detenerse y esperar confirmación del usuario en estas etapas:

- `intake`: Confirmar titular, denominación exacta, tipo de marca y si se reclamará logo/colores.
- `prior-search`: Confirmar resultados de búsqueda previa y si se continúa pese a similitudes detectadas.
- `classes`: Confirmar clase o clases Niza seleccionadas.
- `goods-services`: Confirmar la redacción final de productos/servicios por clase.
- `application-draft`: Confirmar el borrador completo antes de presentar o copiar al portal.

## Flujo de Trabajo

### 1. Relevamiento inicial

Lea `prompts/intake.md` y complete los datos mínimos del caso:

- marca exacta;
- titular;
- actividad;
- países de interés;
- uso actual o proyectado;
- tipo de signo: denominativa, figurativa, mixta, tridimensional u otra.

Si falta contexto normativo o de revisión, lea `references/workflow_rules.md` y `references/application_fields.md`.

### 2. Búsqueda de antecedentes

Lea `prompts/prior_mark_search.md` y `references/prior_search_rules.md`.

Para preparar variantes de búsqueda y la planilla base, use:

```bash
python3 tools/prepare_prior_search.py --input MarcaINPI/Borradores/IntakeMarca.json --out-dir MarcaINPI/Borradores
```

La búsqueda debe priorizar:

- base pública de marcas del INPI;
- coincidencias idénticas;
- similitudes fonéticas;
- similitudes gráficas o conceptuales;
- coincidencia o cercanía en clases relacionadas.

El resultado de esta etapa debe guardarse como:

- `MarcaINPI/Borradores/BusquedaAntecedentes.md`
- `MarcaINPI/Borradores/BusquedaAntecedentes.json`

### 3. Sugerencia de clases Niza

Lea `prompts/nice_classification.md` y `references/nice_classification_rules.md`.

Para automatizar una primera propuesta, use:

```bash
python3 tools/suggest_nice_classes.py --input MarcaINPI/Borradores/IntakeMarca.json --out-dir MarcaINPI/Borradores
```

El agente debe revisar el resultado y ajustar manualmente si el caso mezcla:

- software descargable y SaaS;
- marketplace y retail;
- educación y software;
- fintech y software;
- branding/publicidad y plataforma tecnológica.

### 4. Redacción de productos y servicios

Lea `prompts/goods_services_builder.md`.

La redacción debe:

- describir lo que el titular realmente ofrece o ofrecerá;
- evitar amplitud artificial;
- evitar tecnicismos innecesarios;
- separar claramente cada clase.

Para una primera redacción guiada de clases frecuentes, use:

```bash
python3 tools/build_goods_services_draft.py \
  --intake MarcaINPI/Borradores/IntakeMarca.json \
  --classes MarcaINPI/Borradores/ClasesSugeridas.json \
  --out-dir MarcaINPI/Borradores
```

Antes de ejecutar, lea `references/class_templates.md` si el caso involucra clases 9, 35, 36, 41 o 42.

### 5. Borrador de solicitud

Lea `prompts/application_builder.md` y genere el resumen estructurado del trámite.

Para consolidar el borrador use:

```bash
python3 tools/build_application_draft.py \
  --intake MarcaINPI/Borradores/IntakeMarca.json \
  --classes MarcaINPI/Borradores/ClasesSugeridas.json \
  --goods-services MarcaINPI/Borradores/ProductosServicios.json \
  --out-dir MarcaINPI/Borradores
```

La salida debe incluir:

- un índice general del caso;
- un archivo `SolicitudMarca_ClaseNN.md` por cada clase confirmada.

### 6. Revisión final

Lea `prompts/final_review.md`.

El agente debe verificar:

- consistencia total del nombre de la marca;
- titularidad;
- clases;
- productos/servicios;
- prioridad o reivindicaciones especiales;
- decisión sobre continuar o no frente a conflictos detectados.

## Recursos

- Reglas generales del flujo: `references/workflow_rules.md`
- Búsqueda de antecedentes: `references/prior_search_rules.md`
- Clasificación Niza: `references/nice_classification_rules.md`
- Plantillas por clase: `references/class_templates.md`
- Campos de solicitud: `references/application_fields.md`

## Entregables esperados

El skill debe producir, como mínimo:

- `MarcaINPI/Borradores/IntakeMarca.json`
- `MarcaINPI/Borradores/BusquedaAntecedentes.md`
- `MarcaINPI/Borradores/ClasesSugeridas.md`
- `MarcaINPI/Borradores/ProductosServicios.md`
- `MarcaINPI/Borradores/SolicitudMarca.md`
- `MarcaINPI/Borradores/SolicitudMarca_Clase9.md` u otros equivalentes por clase

Si el caso está listo para carga manual o revisión externa, el borrador final debe incluir una sección visible:

```text
STOP_FOR_USER
NEXT_ACTION: Revise el borrador completo y confirme antes de presentar la solicitud ante el INPI.
```
