# Preparacion de Patentes ante INPI (Argentina)

Este repositorio contiene una skill para preparar materiales de divulgacion tecnica y borradores de memoria descriptiva para patentes de invencion en Argentina.

La skill esta pensada para software, sistemas, automatizacion, IA, plataformas y otras soluciones tecnicas que necesitan:

- identificar puntos inventivos;
- contrastarlos con antecedentes;
- y ordenar una memoria descriptiva inicial para revision profesional.

## Que hace

La skill ayuda a:

1. delimitar el caso y el problema tecnico;
2. escanear proyecto y documentacion;
3. detectar candidatos de invencion;
4. ordenar una matriz basica de antecedentes;
5. generar una estructura de divulgacion tecnica;
6. dejar alertas de patentabilidad y revision.

## Base conceptual

La skill no trata al software como patentable por si mismo.

Su enfoque es:

- problema tecnico;
- solucion tecnica;
- efecto tecnico;
- implementacion concreta;
- y consistencia con el marco argentino.

## Estructura

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── prompts/
│   ├── intake.md
│   ├── project_scan.md
│   ├── invention_candidates.md
│   ├── prior_art_matrix.md
│   ├── disclosure_draft.md
│   └── final_review.md
├── references/
│   ├── official_sources.md
│   ├── legal_boundaries.md
│   ├── patentability_rules.md
│   └── disclosure_sections.md
└── tools/
    ├── scan_project.py
    ├── build_invention_candidates.py
    ├── build_prior_art_matrix.py
    └── build_disclosure_skeleton.py
```

## Uso basico

Una vez instalada en tu entorno de IA, podes iniciar el flujo diciendo:

> "Usa la skill INPI para analizar este proyecto y preparar una divulgacion tecnica."

La skill trabaja sobre un directorio de salida llamado `PreparacionPatenteINPI/`.

## Fuentes oficiales base

- Ley 24.481 en InfoLEG: https://www.infoleg.gob.ar/wp-content/uploads/2014/10/LEY-F-1997.htm
- INPI / Patentes de invencion y modelos de utilidad: https://www.argentina.gob.ar/inpi/patentes-de-invencion-y-modelos-de-utilidad
- INPI / Patentar tu invento: https://www.argentina.gob.ar/servicio/patentar-tu-invento
- INPI / Buscar patentes: https://www.argentina.gob.ar/inpi/patentes-de-invencion-y-modelos-de-utilidad/buscar-patentes-de-invencion-o-modelos-de-utilidad
- WIPO Patentscope: https://patentscope.wipo.int/search/es/search.jsf

## Aviso

La skill genera borradores y matrices de trabajo. No reemplaza un agente de la propiedad industrial cuando:

- el caso es fronterizo en patentabilidad;
- hay multiples familias de invencion posibles;
- o el alcance de proteccion necesita estrategia profesional.
