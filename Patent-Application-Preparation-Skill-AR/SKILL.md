---
name: inpi-patent-preparation-argentina
description: >
  Prepara materiales de divulgacion tecnica para patentes en Argentina:
  intake, escaneo del proyecto, candidatos de invencion, matriz de antecedentes
  y borrador de memoria descriptiva inicial.
metadata:
  short-description: Preparacion guiada de patente tecnica para INPI Argentina
---

# Patent Application Preparation (Argentina)

Este skill organiza la preparacion de materiales para una divulgacion tecnica inicial.

- **Directorio de salida:** `PreparacionPatenteINPI/`
- **Flujo:** Intake -> Escaneo -> Candidatos -> Antecedentes -> Borrador -> Revision final
- **Objetivo:** convertir un proyecto tecnico en una base ordenada para evaluacion de patentabilidad
- **Regla critica:** no presentar software abstracto como si fuera invencion patentable sin problema tecnico y efecto tecnico claros

## STOP_FOR_USER

El agente debe detenerse en:

- `intake`: definicion del caso y modulo principal
- `candidates`: confirmacion de candidatos inventivos
- `prior-art`: matriz de antecedentes antes del borrador
- `draft`: revision del esquema de memoria descriptiva
- `final-review`: validacion final antes de uso externo

## Flujo

### 1. Intake

Lea `prompts/intake.md`.

### 2. Escaneo

Lea `prompts/project_scan.md`.

```bash
python3 tools/scan_project.py \
  --project /ruta/al/proyecto \
  --out-dir PreparacionPatenteINPI/Borradores
```

### 3. Candidatos de invencion

Lea `prompts/invention_candidates.md` y `references/patentability_rules.md`.

```bash
python3 tools/build_invention_candidates.py \
  --intake PreparacionPatenteINPI/Borradores/IntakePatente.json \
  --scan PreparacionPatenteINPI/Borradores/AnalisisProyectoPatente.json \
  --out-dir PreparacionPatenteINPI/Borradores
```

### 4. Matriz de antecedentes

Lea `prompts/prior_art_matrix.md`.

```bash
python3 tools/build_prior_art_matrix.py \
  --candidates PreparacionPatenteINPI/Borradores/CandidatosInvencion.json \
  --out-dir PreparacionPatenteINPI/Borradores
```

### 5. Borrador de divulgacion

Lea `prompts/disclosure_draft.md` y `references/disclosure_sections.md`.

```bash
python3 tools/build_disclosure_skeleton.py \
  --intake PreparacionPatenteINPI/Borradores/IntakePatente.json \
  --candidates PreparacionPatenteINPI/Borradores/CandidatosInvencion.json \
  --prior-art PreparacionPatenteINPI/Borradores/MatrizAntecedentes.json \
  --out-dir PreparacionPatenteINPI/Borradores
```

### 6. Revision final

Lea `prompts/final_review.md`.

## Recursos

- `references/official_sources.md`
- `references/legal_boundaries.md`
- `references/patentability_rules.md`
- `references/disclosure_sections.md`

## Entregables minimos

- `PreparacionPatenteINPI/Borradores/AnalisisProyectoPatente.md`
- `PreparacionPatenteINPI/Borradores/CandidatosInvencion.md`
- `PreparacionPatenteINPI/Borradores/MatrizAntecedentes.md`
- `PreparacionPatenteINPI/Borradores/BorradorDivulgacionPatente.md`
