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

## Aviso

Esta herramienta genera **borradores y documentación preparatoria**. Debe ser revisada antes de su uso formal ante la AAIP o en un proceso de auditoría, inspección o due diligence.
