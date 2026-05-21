---
name: dnda-software-registry-argentina
description: >
  Prepara materiales para el registro de software ante DNDA en Argentina:
  intake, analisis del proyecto, borrador de campos para TAD, dossier de codigo
  y descripcion funcional basada en evidencia real.
metadata:
  short-description: Preparacion guiada para registro de software ante DNDA
---

# Software Copyright Registration (Argentina)

Este skill organiza la preparacion de materiales para el registro de software.

- **Directorio de salida:** `RegistroSoftwareDNDA/`
- **Flujo:** Intake -> Analisis -> Campos -> Dossier -> Descripcion funcional -> Revision final
- **Objetivo:** transformar un proyecto real en un expediente tecnico claro y consistente
- **Regla critica:** no inventar autores, fechas, titularidad ni caracteristicas del software

## STOP_FOR_USER

El agente debe detenerse y esperar confirmacion en:

- `intake`: autores, titularidad, tipo de obra y fecha de finalizacion
- `fields`: campos declarativos antes del borrador final
- `code-dossier`: seleccion o alcance del material de codigo
- `functional-brief`: descripcion funcional antes del cierre
- `final-review`: revision completa antes de uso operativo

## Flujo

### 1. Relevamiento inicial

Lea `prompts/intake.md`.

### 2. Analisis del proyecto

Lea `prompts/project_scan.md`.

```bash
python3 tools/scan_project.py \
  --project /ruta/al/proyecto \
  --out-dir RegistroSoftwareDNDA/Borradores
```

### 3. Borrador de campos

Lea `prompts/filing_fields.md` y `references/dnda_fields_map.md`.

```bash
python3 tools/build_filing_draft.py \
  --intake RegistroSoftwareDNDA/Borradores/IntakeDNDA.json \
  --scan RegistroSoftwareDNDA/Borradores/AnalisisProyectoDNDA.json \
  --out-dir RegistroSoftwareDNDA/Borradores
```

### 4. Dossier de codigo

Lea `prompts/code_dossier.md` y `references/evidence_rules.md`.

```bash
python3 tools/build_code_dossier.py \
  --project /ruta/al/proyecto \
  --scan RegistroSoftwareDNDA/Borradores/AnalisisProyectoDNDA.json \
  --out-dir RegistroSoftwareDNDA/Borradores
```

### 5. Descripcion funcional

Lea `prompts/functional_brief.md`.

```bash
python3 tools/build_functional_brief.py \
  --intake RegistroSoftwareDNDA/Borradores/IntakeDNDA.json \
  --scan RegistroSoftwareDNDA/Borradores/AnalisisProyectoDNDA.json \
  --out-dir RegistroSoftwareDNDA/Borradores
```

### 6. Revision final

Lea `prompts/final_review.md`.

## Recursos

- `references/official_sources.md`
- `references/workflow_rules.md`
- `references/dnda_fields_map.md`
- `references/evidence_rules.md`

## Entregables minimos

- `RegistroSoftwareDNDA/Borradores/AnalisisProyectoDNDA.md`
- `RegistroSoftwareDNDA/Borradores/BorradorCamposDNDA.md`
- `RegistroSoftwareDNDA/Borradores/DossierCodigoDNDA.md`
- `RegistroSoftwareDNDA/Borradores/DescripcionFuncionalDNDA.md`
