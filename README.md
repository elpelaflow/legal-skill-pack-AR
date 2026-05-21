# Smart Contracts y Lógica Contractual Automatizada (Argentina)

Este repositorio contiene una **Skill** para agentes de IA diseñada para asistir en el modelado de **smart contracts** y acuerdos con ejecución automatizada, con foco en compatibilidad conceptual con el marco jurídico argentino.

La skill está pensada para equipos legales, founders, desarrolladores blockchain, estudios y consultores que necesitan traducir un acuerdo o una mecánica de negocio a una lógica ejecutable sin perder de vista:

- qué parte del acuerdo puede automatizarse;
- qué parte debe quedar fuera de la cadena;
- qué eventos activan una ejecución;
- qué riesgos regulatorios o contractuales existen;
- y cómo dejar una especificación clara antes de escribir código.

## ¿Qué hace esta Skill?

La skill ayuda a:

1. **Modelar la lógica jurídica y operativa** del acuerdo.
2. **Separar on-chain y off-chain**.
3. **Detectar dependencias de oráculos, datos externos o validaciones humanas**.
4. **Construir una matriz de riesgos** para Argentina.
5. **Generar una especificación de smart contract** lista para revisión legal/técnica.

## Base conceptual

La skill parte de una regla central:

- un smart contract no reemplaza automáticamente al contrato jurídico;
- solo automatiza determinadas condiciones, eventos o prestaciones;
- por eso hace falta separar cuidadosamente:
  - lógica ejecutable;
  - texto contractual;
  - validaciones humanas;
  - remedios fuera de cadena.

## Estructura

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── prompts/
│   ├── intake.md
│   ├── legal_logic_mapping.md
│   ├── onchain_offchain_split.md
│   ├── oracles_and_triggers.md
│   ├── risk_compliance.md
│   ├── execution_controls.md
│   └── final_review.md
├── references/
│   ├── workflow_rules.md
│   ├── smart_contract_boundaries.md
│   ├── argentina_legal_risks.md
│   ├── blockchain_execution_patterns.md
│   ├── execution_templates.md
│   └── specialization_paths.md
└── tools/
    ├── build_legal_logic_matrix.py
    ├── build_onchain_offchain_map.py
    ├── build_risk_matrix.py
    └── build_smart_contract_spec.py
```

## Uso básico

Una vez instalada en tu entorno de IA, podés iniciar el flujo diciendo:

> *"Usá la skill de smart contracts para modelar este acuerdo y su ejecución automática."*

La skill trabaja sobre un directorio de salida llamado `SmartContractSpecAR/`.

## Alcance

Esta skill es útil para:

- escrow o liberación condicionada;
- vesting;
- hitos automáticos;
- revenue split;
- licencias con activación técnica;
- gobernanza o permisos;
- automatización de eventos verificables.

No está pensada para saltar directamente a contratos complejos sin análisis, especialmente cuando hay:

- consumo;
- datos personales;
- regulación financiera;
- activos reales tokenizados;
- KYC/AML;
- pagos masivos o recaudación pública.

## Posibilidad de especialización

Esta skill puede evolucionar de dos maneras:

- **v2**: expansión del mismo repo con más patrones y mejores controles;
- **v3**: especialización por vertical o caso de uso.

### Qué es una v2

Una v2 sigue siendo la misma skill, pero más fuerte.

Ejemplos:

- patrones más finos de escrow, vesting o revenue split;
- mejor clasificación de riesgos;
- mejores controles de pausabilidad, fallback y oráculos;
- matrices más precisas de on-chain/off-chain.

### Qué es una v3

Una v3 ya no es sólo expansión: es **especialización**.

Ejemplos:

- smart contracts para fintech;
- smart contracts para tokenización de activos;
- smart contracts para DAOs;
- smart contracts para royalties;
- smart contracts para escrow comercial.

### Cómo se haría

#### Opción 1: especializar este mismo repo

Eso implicaría tocar:

- [SKILL.md](/home/dev-flow/Smart-Contracts-Skill-AR/SKILL.md)
- [references/argentina_legal_risks.md](/home/dev-flow/Smart-Contracts-Skill-AR/references/argentina_legal_risks.md)
- [references/blockchain_execution_patterns.md](/home/dev-flow/Smart-Contracts-Skill-AR/references/blockchain_execution_patterns.md)
- [references/execution_templates.md](/home/dev-flow/Smart-Contracts-Skill-AR/references/execution_templates.md)
- [tools/build_risk_matrix.py](/home/dev-flow/Smart-Contracts-Skill-AR/tools/build_risk_matrix.py)
- [tools/build_smart_contract_spec.py](/home/dev-flow/Smart-Contracts-Skill-AR/tools/build_smart_contract_spec.py)

#### Opción 2: crear una skill derivada

Ejemplos:

- `Smart-Contracts-Skill-AR-Fintech`
- `Smart-Contracts-Skill-AR-Escrow`
- `Smart-Contracts-Skill-AR-Tokenization`

### Qué cambiaría una v3 real

1. taxonomía de riesgos;
2. patrones de ejecución;
3. oráculos típicos;
4. controles y fallback;
5. límites regulatorios del vertical.

La explicación detallada queda también en:

- [specialization_paths.md](/home/dev-flow/Smart-Contracts-Skill-AR/references/specialization_paths.md)

## Aviso

La skill genera **borradores de modelado y especificación**, no opiniones legales definitivas ni código listo para producción sin revisión humana.
