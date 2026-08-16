# Ley de Economía del Conocimiento (Argentina)

Este repositorio contiene una **Skill** para agentes de IA diseñada para preparar materiales de ingreso y permanencia en el **Régimen de Promoción de la Economía del Conocimiento** en Argentina.

La skill está pensada para empresas de software, SaaS, IA, cloud, servicios IT y proyectos digitales que necesitan ordenar la evidencia técnica y administrativa para postularse al registro y sostener la inscripción en el tiempo.

## ¿Qué hace esta Skill?

La skill ayuda a:

1. **Relevar el perfil de la empresa**: tamaño, actividad principal, exportaciones, nómina y certificaciones.
2. **Analizar el proyecto o código fuente** para detectar señales de actividades elegibles.
3. **Mapear actividades promovidas** con evidencia técnica trazable.
4. **Preparar un borrador del expediente** orientado al flujo actual de `Formulario 1278 + TAD`.
5. **Sugerir un carril de requisitos adicionales** con vacíos de evidencia.
6. **Ordenar la permanencia** con checklist de presentación anual y revalidación bienal.
7. **Estimar beneficios** de forma orientativa para bono de crédito fiscal y reducción de ganancias.

## Base conceptual

La skill parte de una regla simple:

- el régimen no se gana con una descripción comercial;
- se gana con **actividad promovida demostrable**, consistencia documental y mantenimiento posterior.

Por eso la skill separa:

- elegibilidad;
- evidencia técnica;
- borrador de solicitud;
- mantenimiento del régimen;
- estimación de beneficios.

## Estructura

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── prompts/
│   ├── intake.md
│   ├── eligibility_mapping.md
│   ├── technical_evidence.md
│   ├── registry_application.md
│   ├── annual_compliance.md
│   ├── benefits_estimation.md
│   └── final_review.md
├── references/
│   ├── workflow_rules.md
│   ├── eligible_activities_rules.md
│   ├── application_fields.md
│   ├── maintenance_obligations.md
│   └── benefits_rules.md
└── tools/
    ├── scan_eligible_activity_signals.py
    ├── build_technical_evidence.py
    ├── build_requirement_path.py
    ├── build_registry_draft.py
    ├── build_compliance_checklist.py
    └── estimate_benefits.py
```

## Uso básico

Una vez instalada en tu entorno de IA, podés iniciar el flujo diciendo:

> *"Usá la skill de Economía del Conocimiento para preparar el expediente de mi empresa."*

La skill trabaja sobre un directorio de salida llamado `RegistroLEC/`.

## Alcance

Esta skill es especialmente útil para:

- software a medida;
- SaaS;
- plataformas cloud;
- soluciones de IA y datos;
- servicios profesionales IT exportables;
- productos digitales con equipos registrados en Argentina.

## Qué no hace sola

La skill no reemplaza:

- certificaciones de calidad;
- informes contables;
- validaciones fiscales o societarias;
- ni criterio profesional cuando la actividad elegible es fronteriza.

## Qué suma la v2

La v2 endurece tres cosas:

- recomienda por qué carril de requisito adicional conviene sostener el caso;
- marca vacíos de evidencia por `calidad`, `capacitacion`, `I+D` y `exportaciones`;
- y arrastra esa lógica al borrador del expediente y al checklist de permanencia.

## Fuentes oficiales base

La skill fue estructurada en torno a fuentes oficiales vigentes al **21 de mayo de 2026**:

- Ley 27.506 actualizada: https://www.argentina.gob.ar/normativa/nacional/ley-27506-324101/actualizacion
- Acceso a beneficios del régimen: https://www.argentina.gob.ar/acceder-los-beneficios-del-regimen-de-promocion-de-la-economia-del-conocimiento
- Revalidación bienal: https://www.argentina.gob.ar/servicio/presentar-la-revalidacion-bienal-al-regimen-de-promocion-de-la-economia-del-conocimiento
- Tasa de verificación y control: https://www.argentina.gob.ar/servicio/abonar-la-tasa-en-concepto-de-verificacion-y-control-del-regimen-de-promocion-de-la

## Aviso

La skill genera **borradores preparatorios** y una **matriz de evidencia**. No reemplaza revisión legal, contable o tributaria cuando:

- hay actividades mixtas o dudosas;
- la empresa depende de autodesarrollo no elegible;
- la facturación promovida no está claramente segregada;
- la nómina afectada a actividades promovidas no está bien documentada;
- o se pretende maximizar beneficios sin base registral suficiente.
