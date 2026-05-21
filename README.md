# Registro de Marca (Argentina - INPI)

Este repositorio contiene una **Skill** para agentes de IA diseñada para asistir en la preparación de solicitudes de **registro de marca ante el INPI Argentina**.

La idea central es transformar un proceso normalmente manual, repetitivo y propenso a errores en un flujo guiado con validaciones, borradores y entregables consistentes.

## ¿Qué hace esta Skill?

La skill ayuda a:

1. **Relevar la marca y su contexto comercial**: nombre, logo, tipo de marca, titular, uso actual o proyectado.
2. **Guiar la búsqueda de antecedentes**: organiza la consulta en la base pública del INPI y ordena hallazgos por similitud visual, fonética y conceptual.
3. **Sugerir clases Niza**: propone clases probables según el modelo de negocio, productos y servicios.
4. **Redactar la descripción de productos/servicios**: arma borradores claros y defensables para cada clase.
5. **Preparar la solicitud**: genera un resumen estructurado con los datos que luego deben cargarse o revisarse antes de presentar la solicitud.

## Alcance operativo de esta versión

Esta skill está diseñada para:

- marcas denominativas, mixtas y figurativas;
- startups, software, SaaS, apps, ecommerce, fintech, educación y servicios digitales;
- preparación documental previa a la carga en el portal del INPI;
- armado de una **solicitud por cada clase**, en línea con el flujo actual del portal.

## ¿Por qué una versión para Argentina?

El registro marcario en Argentina tiene particularidades prácticas:

- La revisión depende de una correcta **delimitación por clase**.
- Una mala **descripción de productos o servicios** puede generar observaciones o debilitar el alcance.
- La búsqueda previa en la base pública del INPI es clave para evitar presentar marcas con conflictos obvios.
- Datos como titularidad, domicilio, prioridad, colores reivindicados y tipo de signo deben mantenerse consistentes.

Esta versión está pensada para el contexto del **INPI Argentina**, con terminología legal y administrativa en español rioplatense/profesional.

La skill fue ajustada al flujo visible del portal del INPI al **21 de mayo de 2026**:

- se recomienda buscar antecedentes antes de presentar;
- el portal exige seleccionar clase y productos/servicios;
- si se quieren proteger varias clases, el propio portal indica presentar **una solicitud por cada clase**.

## Estructura

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── prompts/
│   ├── intake.md
│   ├── prior_mark_search.md
│   ├── nice_classification.md
│   ├── goods_services_builder.md
│   ├── application_builder.md
│   └── final_review.md
├── references/
│   ├── workflow_rules.md
│   ├── prior_search_rules.md
│   ├── nice_classification_rules.md
│   ├── class_templates.md
│   └── application_fields.md
└── tools/
    ├── prepare_prior_search.py
    ├── suggest_nice_classes.py
    ├── build_goods_services_draft.py
    └── build_application_draft.py
```

## Uso básico

Una vez instalada en tu entorno de IA, podés iniciar el flujo diciendo:

> *"Usá la skill de registro de marca para Argentina y prepará la solicitud para mi marca."*

La skill trabaja sobre un directorio de salida llamado `MarcaINPI/`.

## Aviso

Esta herramienta genera **borradores y material de preparación**. No garantiza registrabilidad ni reemplaza el análisis profesional cuando existen conflictos relevantes, oposiciones, observaciones o estrategias multiclase complejas.
