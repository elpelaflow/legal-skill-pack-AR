# Contrato de Desarrollo de Software (Argentina)

Este repositorio contiene una **Skill** para agentes de IA diseñada para preparar borradores de contratos de desarrollo de software adaptables a proyectos a medida en Argentina.

La skill está pensada para freelancers, estudios, software factories, startups y clientes que necesitan ordenar por escrito:

- alcance;
- entregables;
- cronograma;
- aceptación;
- pagos;
- propiedad intelectual;
- confidencialidad;
- soporte y garantías;
- terminación del vínculo.

## ¿Qué hace esta Skill?

La skill ayuda a:

1. **Relevar el negocio del proyecto** y el rol de cada parte.
2. **Definir alcance y entregables** para evitar zonas grises.
3. **Ordenar la mecánica económica**: precio, hitos, anticipo, mora e impuestos.
4. **Construir una matriz de propiedad intelectual**:
   - código preexistente del desarrollador;
   - desarrollos a medida;
   - librerías o componentes de terceros;
   - cesión, licencia o reserva de derechos.
5. **Redactar un borrador contractual** listo para revisión humana.

## Base conceptual y jurídica

La skill parte de una advertencia importante para contratos de software en Argentina:

- no conviene confiar en fórmulas ambiguas como “trabajo por encargo” sin definir expresamente qué derechos se ceden, cuáles se reservan y desde cuándo;
- tampoco conviene mezclar en una misma bolsa código preexistente, componentes open source, entregables a medida y know-how del proveedor.

Por eso esta skill fuerza una **matriz de IP** antes de redactar el contrato.

## Estructura

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── prompts/
│   ├── intake.md
│   ├── scope_definition.md
│   ├── deliverables_acceptance.md
│   ├── payment_terms.md
│   ├── ip_structure.md
│   ├── confidentiality_data.md
│   ├── support_warranty.md
│   └── final_review.md
├── references/
│   ├── contract_workflow_rules.md
│   ├── clause_guide.md
│   ├── ip_rules_argentina.md
│   ├── acceptance_rules.md
│   └── payment_models.md
└── tools/
    ├── build_scope_matrix.py
    ├── build_ip_matrix.py
    ├── build_payment_schedule.py
    └── build_contract_draft.py
```

## Uso básico

Una vez instalada en tu entorno de IA, podés iniciar el flujo diciendo:

> *"Usá la skill de contrato de desarrollo para preparar un borrador para este proyecto."*

La skill trabaja sobre un directorio de salida llamado `ContratoDesarrolloSoftware/`.

## Posibles skills hermanas

Esta skill encaja dentro de una familia más amplia de skills contractuales diarias para freelancers y startups de software.

Ejemplos naturales de skills relacionadas:

- NDA / Acuerdo de Confidencialidad;
- Términos y Condiciones de SaaS;
- Acuerdo de mantenimiento y soporte;
- Acuerdo de licencia de software;
- Acuerdo de cesión de código o activos digitales;
- Contrato de staff augmentation / outsourcing.

## Aviso

Esta herramienta genera **borradores contractuales preparatorios**. No reemplaza revisión legal profesional, especialmente cuando hay:

- montos relevantes;
- clientes extranjeros;
- cesión total de IP;
- uso de open source crítico;
- tratamiento de datos personales;
- integraciones regulatorias;
- exclusividad, penalidades o limitaciones fuertes de responsabilidad.
