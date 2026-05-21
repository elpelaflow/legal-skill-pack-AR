---
name: acuerdo-confidencialidad-argentina
description: >
  Genera materiales preparatorios para acuerdos de confidencialidad (NDA) unilaterales o mutuos
  en Argentina, con foco en alcance, excepciones, plazo, devolución/destrucción, remedios y
  preparación para firma electrónica o digital conforme a la Ley 25.506.
metadata:
  short-description: Preparación guiada de NDAs para Argentina
---

# Acuerdos de Confidencialidad (NDA) - Argentina

Este skill organiza la preparación de acuerdos de confidencialidad en contexto argentino.

- **Directorio de salida:** `AcuerdoConfidencialidad/` en el directorio de trabajo actual.
- **Flujo:** Intake -> Tipo de NDA -> Alcance confidencial -> Exclusiones y plazo -> Remedios -> Firma -> Revisión final.
- **Objetivo:** Reducir ambigüedad y acelerar la preparación de NDAs negociables y firmables.
- **Regla operativa crítica:** No redactar la cláusula de confidencialidad sin definir primero qué queda dentro y qué queda fuera.

## Puertas de Confirmación Obligatoria (STOP_FOR_USER)

El agente debe detenerse y esperar confirmación en estas etapas:

- `intake`: Confirmar partes, contexto y objetivo de intercambio.
- `scope`: Confirmar tipo de información confidencial y exclusiones.
- `term`: Confirmar plazo y persistencia de la obligación.
- `signature`: Confirmar si el documento se firmará electrónicamente o con firma digital.
- `final-review`: Confirmar el borrador final antes de circularlo.

## Flujo de Trabajo

### 1. Relevamiento inicial

Lea `prompts/intake.md` y releve:

- partes;
- contexto de la relación;
- finalidad del intercambio;
- si el NDA es unilateral o mutuo;
- si habrá acceso a código, datos, pricing, arquitectura, clientes o estrategia.

### 2. Tipo de NDA

Lea `prompts/nda_type.md`.

El agente debe distinguir:

- NDA unilateral;
- NDA mutuo.

### 3. Matriz de confidencialidad

Lea `prompts/confidential_information.md` y `references/confidentiality_scope_rules.md`.

Para consolidar la matriz:

```bash
python3 tools/build_confidentiality_matrix.py --input AcuerdoConfidencialidad/Borradores/IntakeNDA.json --out-dir AcuerdoConfidencialidad/Borradores
```

La matriz debe distinguir especialmente:

- código fuente y repositorios;
- credenciales y accesos;
- pricing y propuestas;
- datasets o información de clientes;
- información regulada o datos personales.

### 4. Exclusiones y plazo

Lea `prompts/exclusions_and_term.md`.

El agente debe definir:

- exclusiones típicas;
- duración del acuerdo;
- duración de la obligación de confidencialidad.

### 5. Devolución, destrucción y remedios

Lea `prompts/return_destroy_remedies.md`.

Separar:

- devolución o destrucción de información;
- copias de resguardo;
- cese de uso;
- remedios por incumplimiento.

### 6. Firma

Lea `prompts/signature_mode.md` y `references/signature_rules_argentina.md`.

Para preparar el paquete de firma:

```bash
python3 tools/build_signature_packet.py --input AcuerdoConfidencialidad/Borradores/IntakeNDA.json --out-dir AcuerdoConfidencialidad/Borradores
```

### 7. Borrador final

Lea `references/nda_clause_guide.md`.

Para consolidar el borrador:

```bash
python3 tools/build_nda_draft.py \
  --intake AcuerdoConfidencialidad/Borradores/IntakeNDA.json \
  --matrix AcuerdoConfidencialidad/Borradores/MatrizConfidencialidad.json \
  --signature AcuerdoConfidencialidad/Borradores/PaqueteFirma.json \
  --out-dir AcuerdoConfidencialidad/Borradores
```

### 8. Revisión final

Lea `prompts/final_review.md`.

## Recursos

- Reglas generales: `references/workflow_rules.md`
- Guía de cláusulas NDA: `references/nda_clause_guide.md`
- Firma en Argentina: `references/signature_rules_argentina.md`
- Reglas de alcance confidencial: `references/confidentiality_scope_rules.md`
- Especialización futura: `references/specialization_paths.md`

## Entregables esperados

Como mínimo, el skill debe producir:

- `AcuerdoConfidencialidad/Borradores/IntakeNDA.json`
- `AcuerdoConfidencialidad/Borradores/MatrizConfidencialidad.md`
- `AcuerdoConfidencialidad/Borradores/PaqueteFirma.md`
- `AcuerdoConfidencialidad/Borradores/AcuerdoConfidencialidad.md`
