# Software Copyright Registration (Argentina)

Este repositorio contiene una skill para preparar materiales de registro de software ante la Direccion Nacional del Derecho de Autor en Argentina.

La skill esta pensada para productos digitales, SaaS, apps, sistemas internos y software a medida que necesitan ordenar:

- evidencia tecnica del proyecto;
- borrador de campos para TAD;
- material de identificacion del software;
- y una descripcion funcional consistente.

## Que hace

La skill ayuda a:

1. relevar datos del titular, autores y obra;
2. analizar el proyecto y detectar estructura, tecnologias y modulo principal;
3. construir un borrador de campos de presentacion;
4. armar un dossier de codigo con trazabilidad por archivo;
5. redactar una descripcion funcional basada en evidencia real;
6. dejar checklist final de consistencia antes de la carga.

## Base conceptual

El registro no debe apoyarse en textos inventados.

La skill separa:

- datos declarativos;
- evidencia tecnica;
- material de identificacion;
- y descripcion funcional.

## Estructura

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── prompts/
│   ├── intake.md
│   ├── project_scan.md
│   ├── filing_fields.md
│   ├── code_dossier.md
│   ├── functional_brief.md
│   └── final_review.md
├── references/
│   ├── official_sources.md
│   ├── workflow_rules.md
│   ├── dnda_fields_map.md
│   └── evidence_rules.md
└── tools/
    ├── scan_project.py
    ├── build_filing_draft.py
    ├── build_code_dossier.py
    └── build_functional_brief.py
```

## Uso basico

Una vez instalada en tu entorno de IA, podes iniciar el flujo diciendo:

> "Usa la skill DNDA para preparar el registro de este software."

La skill trabaja sobre un directorio de salida llamado `RegistroSoftwareDNDA/`.

## Fuentes oficiales base

- Ley 11.723 en InfoLEG: https://servicios.infoleg.gob.ar/infolegInternet/anexos/40000-44999/42755/texact.htm
- DNDA / tramites de software: https://www.argentina.gob.ar/tramitar/tramites_y_servicios/software
- Registrar un software puesto en conocimiento publico: https://www.argentina.gob.ar/node/37071
- TAD: https://tramitesadistancia.gob.ar/

## Aviso

La skill genera borradores preparatorios. No reemplaza validacion legal cuando hay:

- conflictos de titularidad;
- multiples autores o cesiones;
- obras derivadas;
- software con componentes de terceros cuyo tratamiento documental sea sensible.
