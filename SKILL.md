---
name: smart-contracts-argentina
description: >
  Genera materiales preparatorios para modelar smart contracts y lógica contractual automatizada
  en Argentina, separando términos jurídicos, eventos ejecutables, componentes on-chain/off-chain,
  oráculos, controles de ejecución y riesgos regulatorios.
metadata:
  short-description: Modelado guiado de smart contracts con foco legal argentino
---

# Smart Contracts y Lógica Contractual Automatizada (Argentina)

Este skill organiza el modelado previo de acuerdos con componentes de ejecución automática.

- **Directorio de salida:** `SmartContractSpecAR/` en el directorio de trabajo actual.
- **Flujo:** Intake -> Lógica legal -> División on-chain/off-chain -> Oráculos y triggers -> Riesgos -> Controles -> Especificación final.
- **Objetivo:** Traducir una relación jurídica o negocio automatizable a una especificación defendible y revisable.
- **Regla operativa crítica:** No intentar automatizar una obligación sin verificar primero si depende de interpretación humana, prueba externa o discreción jurídica.

## Puertas de Confirmación Obligatoria (STOP_FOR_USER)

El agente debe detenerse y esperar confirmación en estas etapas:

- `intake`: Confirmar el negocio o acuerdo base.
- `logic`: Confirmar qué obligación o evento se quiere automatizar.
- `split`: Confirmar qué va on-chain y qué queda off-chain.
- `risk`: Confirmar riesgos regulatorios o de ejecución.
- `final-review`: Confirmar la especificación final antes de usarla como base legal o técnica.

## Flujo de Trabajo

### 1. Relevamiento inicial

Lea `prompts/intake.md` y releve:

- partes;
- negocio o relación base;
- prestación automatizable;
- activos o tokens involucrados;
- blockchain o entorno objetivo;
- necesidad de oráculos o datos externos.

### 2. Mapa de lógica jurídica

Lea `prompts/legal_logic_mapping.md`.

Para consolidar la matriz:

```bash
python3 tools/build_legal_logic_matrix.py --input SmartContractSpecAR/Borradores/IntakeSmartContract.json --out-dir SmartContractSpecAR/Borradores
```

### 3. División on-chain / off-chain

Lea `prompts/onchain_offchain_split.md` y `references/smart_contract_boundaries.md`.

Para ordenar esta división:

```bash
python3 tools/build_onchain_offchain_map.py --input SmartContractSpecAR/Borradores/IntakeSmartContract.json --out-dir SmartContractSpecAR/Borradores
```

### 4. Oráculos y triggers

Lea `prompts/oracles_and_triggers.md`.

El agente debe distinguir:

- eventos internos a la cadena;
- eventos externos;
- oráculos;
- validaciones humanas;
- pausas o cancelaciones.

### 5. Riesgo y compliance

Lea `prompts/risk_compliance.md` y `references/argentina_legal_risks.md`.

Para preparar la matriz:

```bash
python3 tools/build_risk_matrix.py --input SmartContractSpecAR/Borradores/IntakeSmartContract.json --out-dir SmartContractSpecAR/Borradores
```

Si el caso encaja en un patrón conocido, consulte `references/blockchain_execution_patterns.md` y `references/execution_templates.md`.

### 6. Controles de ejecución

Lea `prompts/execution_controls.md` y `references/blockchain_execution_patterns.md`.

Separar:

- pausabilidad;
- roles;
- autorización;
- upgrade;
- fallback;
- reversión posible o imposible;
- logs / evidencia.

### 7. Especificación final

Para consolidar la especificación:

```bash
python3 tools/build_smart_contract_spec.py \
  --intake SmartContractSpecAR/Borradores/IntakeSmartContract.json \
  --logic SmartContractSpecAR/Borradores/MatrizLogicaLegal.json \
  --split SmartContractSpecAR/Borradores/MapaOnchainOffchain.json \
  --risk SmartContractSpecAR/Borradores/MatrizRiesgo.json \
  --out-dir SmartContractSpecAR/Borradores
```

### 8. Revisión final

Lea `prompts/final_review.md`.

## Recursos

- Reglas generales: `references/workflow_rules.md`
- Límites de smart contracts: `references/smart_contract_boundaries.md`
- Riesgos legales argentinos: `references/argentina_legal_risks.md`
- Patrones de ejecución: `references/blockchain_execution_patterns.md`
- Plantillas de ejecución: `references/execution_templates.md`
- Especialización futura: `references/specialization_paths.md`

## Entregables esperados

Como mínimo, el skill debe producir:

- `SmartContractSpecAR/Borradores/IntakeSmartContract.json`
- `SmartContractSpecAR/Borradores/MatrizLogicaLegal.md`
- `SmartContractSpecAR/Borradores/MapaOnchainOffchain.md`
- `SmartContractSpecAR/Borradores/MatrizRiesgo.md`
- `SmartContractSpecAR/Borradores/SmartContractSpec.md`
