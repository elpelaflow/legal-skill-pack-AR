# Preparación para Registro de Datos Personales (AAIP - Argentina)

Este repositorio contiene una **Skill** para agentes de IA diseñada para asistir en la preparación documental vinculada al **Registro Nacional de Bases de Datos** y al cumplimiento operativo básico de la **Ley 25.326** en Argentina.

La skill está pensada para empresas tecnológicas, startups, SaaS, ecommerce y plataformas que tratan datos personales de usuarios, empleados, leads, clientes, proveedores u otros titulares.

## ¿Qué hace esta Skill?

La skill ayuda a:

1. **Relevar al responsable** del tratamiento.
2. **Identificar bases de datos personales reales** dentro del sistema y la operación.
3. **Preparar borradores de inscripción** del responsable y de cada base.
4. **Generar un plan documental de seguridad** alineado con las medidas técnicas y organizativas exigibles.
5. **Redactar un procedimiento básico de derechos del titular**.
6. **Detectar riesgos** de transferencias internacionales, datos sensibles, videovigilancia o conservación indefinida.

## Alcance operativo

Esta skill está diseñada para:

- mapeo inicial de tratamientos;
- preparación de borradores para TAD/AAIP;
- documentación de seguridad y cumplimiento básico;
- readiness documental para revisión interna o externa.

No reemplaza asesoramiento jurídico especializado ni auditoría integral de privacidad.

## Estructura

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── prompts/
│   ├── intake.md
│   ├── system_scan.md
│   ├── database_identification.md
│   ├── responsible_registration.md
│   ├── database_registration.md
│   ├── security_measures.md
│   ├── rights_procedure.md
│   ├── international_transfers.md
│   └── final_review.md
├── references/
│   ├── aaip_workflow_rules.md
│   ├── registration_fields.md
│   ├── security_rules_res47_2018.md
│   ├── inspection_readiness.md
│   ├── database_taxonomy.md
│   └── sector_templates.md
└── tools/
    ├── scan_data_flows.py
    ├── suggest_databases.py
    ├── build_responsible_draft.py
    ├── build_database_registry_draft.py
    ├── build_security_plan.py
    ├── build_rights_procedure.py
    ├── build_international_transfers.py
    └── build_inspection_checklist.py
```

## Uso básico

Una vez instalada en tu entorno de IA, podés iniciar el flujo diciendo:

> *"Usá la skill AAIP para relevar nuestras bases de datos personales y preparar la documentación de registro."*

La skill trabaja sobre un directorio de salida llamado `RegistroDatosAAIP/`.

## Base normativa y operativa

La estructura de esta skill se apoya en el flujo visible de la AAIP al **21 de mayo de 2026**, incluyendo:

- inscripción del responsable;
- registro de bases de datos;
- medidas de seguridad;
- inspecciones y evidencia documental de cumplimiento.

## Posibilidad de especialización

Esta skill fue diseñada como una base **horizontal** y reusable. Eso significa que sirve para muchas organizaciones distintas, pero también puede **especializarse** cuando un sector necesita más precisión.

No es necesario hacerlo desde el inicio. Conviene especializarla cuando:

- el mismo tipo de empresa aparece repetidamente;
- las bases de datos siempre siguen patrones parecidos;
- los riesgos del sector son específicos;
- la documentación general empieza a quedarse corta.

### Qué significa “especializarla”

Especializarla no es “agregar más texto”. Es adaptar la lógica del skill a un vertical concreto, por ejemplo:

- fintech;
- healthtech;
- HR / recruiting;
- videovigilancia;
- ecommerce;
- legaltech;
- edtech.

En una especialización, cambian principalmente estas piezas:

1. **Taxonomía de bases**
   La skill deja de usar sólo categorías generales y pasa a reconocer bases propias del sector.

2. **Heurísticas de detección**
   Los scripts empiezan a buscar señales más específicas en código, documentación y vendors.

3. **Riesgos y controles**
   El semáforo de riesgo y el plan de seguridad se ajustan a la sensibilidad real del vertical.

4. **Prompts y referencias**
   Se agregan instrucciones sectoriales para que el agente no trate todos los casos como si fueran iguales.

### Cómo se haría

La especialización puede hacerse de dos maneras:

#### Opción 1: evolucionar este mismo repo

Se mantiene una sola skill y se agregan ramas de comportamiento por vertical.

Esto implicaría:

- ampliar `references/sector_templates.md`;
- ampliar `references/database_taxonomy.md`;
- ajustar `tools/suggest_databases.py`;
- ajustar `tools/scan_data_flows.py`;
- ajustar el checklist de inspección y el plan de seguridad.

Ventaja:

- un solo repo;
- una sola base de mantenimiento.

Desventaja:

- más complejidad interna;
- más riesgo de que la skill se vuelva demasiado genérica o demasiado cargada.

#### Opción 2: crear una skill derivada

Se usa esta skill como base y se crea otra más específica, por ejemplo:

- `AAIP-Fintech-Skill-AR`
- `AAIP-Healthtech-Skill-AR`

Esa derivada conserva el flujo general, pero cambia referencias, prompts, heurísticas y plantillas.

Ventaja:

- más precisión;
- menos ambigüedad para el usuario final.

Desventaja:

- más repos para mantener.

### Qué tocaría en una v3 especializada

Si alguien quisiera especializar esta skill, lo razonable sería intervenir estas piezas:

- [SKILL.md](/home/dev-flow/Personal-Data-Registry-Skill-AR/SKILL.md)
- [references/database_taxonomy.md](/home/dev-flow/Personal-Data-Registry-Skill-AR/references/database_taxonomy.md)
- [references/sector_templates.md](/home/dev-flow/Personal-Data-Registry-Skill-AR/references/sector_templates.md)
- [prompts/database_identification.md](/home/dev-flow/Personal-Data-Registry-Skill-AR/prompts/database_identification.md)
- [prompts/security_measures.md](/home/dev-flow/Personal-Data-Registry-Skill-AR/prompts/security_measures.md)
- [tools/scan_data_flows.py](/home/dev-flow/Personal-Data-Registry-Skill-AR/tools/scan_data_flows.py)
- [tools/suggest_databases.py](/home/dev-flow/Personal-Data-Registry-Skill-AR/tools/suggest_databases.py)
- [tools/build_inspection_checklist.py](/home/dev-flow/Personal-Data-Registry-Skill-AR/tools/build_inspection_checklist.py)

### Ejemplo conceptual

La skill actual puede detectar una base como:

- `Pagos / Fraude / Riesgo`

Una especialización fintech podría separarla en:

- `Onboarding / KYC`
- `Pagos y liquidaciones`
- `Fraude y monitoreo transaccional`
- `Soporte regulatorio / compliance`

La diferencia no es estética. Esa separación mejora:

- la calidad del registro;
- la documentación de seguridad;
- el análisis de terceros;
- la preparación para inspecciones.

### Recomendación práctica

No especializar por anticipación. Conviene hacerlo cuando:

- ya existen varios casos del mismo vertical;
- aparecen siempre las mismas bases;
- y el costo de seguir usando una skill general empieza a generar fricción.

En otras palabras:

- esta skill sirve como base general;
- una v3 especializada sirve cuando hace falta **criterio sectorial**, no solo estructura.

## Aviso

Esta herramienta genera **borradores y documentación preparatoria**. Debe ser revisada antes de su uso formal ante la AAIP o en un proceso de auditoría, inspección o due diligence.
