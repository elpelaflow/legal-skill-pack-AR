---
name: validacion-documentacion-legal-argentina
description: >
  Revisa documentación legal y regulatoria para Argentina, detectando referencias
  extranjeras impropias, inconsistencias de localización, problemas de formato y
  señales de revisión en documentos generados por otras skills o por equipos internos.
metadata:
  short-description: Control de calidad legal/documental para Argentina
---

# Validación de Documentación Legal (Argentina)

Este skill organiza una revisión final de documentos legales y regulatorios orientados a Argentina.

- **Directorio de salida:** `ValidacionLegalAR/` en el directorio de trabajo actual.
- **Flujo:** Intake -> Inventario -> Lenguaje -> Referencias -> Formato -> Revisión final.
- **Objetivo:** Reducir errores de localización, referencias impropias y problemas formales antes de publicar o presentar documentos.
- **Regla operativa crítica:** No dar por “válido” un documento solo porque no tenga errores sintácticos. También debe ser consistente con Argentina y con el organismo aplicable.

## Puertas de Confirmación Obligatoria (STOP_FOR_USER)

El agente debe detenerse y esperar confirmación en estas etapas:

- `intake`: Confirmar carpeta a revisar y contexto esperado.
- `references`: Confirmar observaciones críticas de ley u organismo.
- `final-review`: Confirmar el reporte final antes de cerrar la validación.

## Flujo de Trabajo

### 1. Relevamiento inicial

Lea `prompts/intake.md` y releve:

- carpeta o conjunto de documentos a revisar;
- tipo de trámite o documento;
- organismo esperado;
- si debe haber PDF final;
- si el control es general o centrado en una skill previa.

### 2. Inventario documental

Lea `prompts/document_inventory.md`.

Para inventariar documentos y señales base:

```bash
python3 tools/scan_document_text.py \
  --input-dir CarpetaDocumentos \
  --out-dir ValidacionLegalAR/Borradores
```

### 3. Revisión de lenguaje y localización

Lea `prompts/language_review.md` y `references/argentina_localization_rules.md`.

### 4. Revisión de referencias legales

Lea `prompts/legal_references_check.md` y `references/official_sources.md`.

Para consolidar señales de contexto:

```bash
python3 tools/check_reference_signals.py \
  --inventory ValidacionLegalAR/Borradores/InventarioDocumental.json \
  --expected-context general \
  --out-dir ValidacionLegalAR/Borradores
```

### 5. Revisión de formato

Lea `prompts/format_validation.md` y `references/format_rules.md`.

Para ordenar el semáforo de revisión:

```bash
python3 tools/build_validation_matrix.py \
  --inventory ValidacionLegalAR/Borradores/InventarioDocumental.json \
  --reference-signals ValidacionLegalAR/Borradores/SenalesReferencia.json \
  --out-dir ValidacionLegalAR/Borradores
```

### 6. Reporte final

Lea `prompts/final_review.md` y `references/validation_rules.md`.

Para consolidar el resultado:

```bash
python3 tools/build_validation_report.py \
  --inventory ValidacionLegalAR/Borradores/InventarioDocumental.json \
  --reference-signals ValidacionLegalAR/Borradores/SenalesReferencia.json \
  --matrix ValidacionLegalAR/Borradores/MatrizValidacion.json \
  --out-dir ValidacionLegalAR/Borradores
```

## Recursos

- Fuentes oficiales: `references/official_sources.md`
- Localización argentina: `references/argentina_localization_rules.md`
- Reglas de validación: `references/validation_rules.md`
- Reglas de formato: `references/format_rules.md`

## Entregables esperados

Como mínimo, el skill debe producir:

- `ValidacionLegalAR/Borradores/InventarioDocumental.json`
- `ValidacionLegalAR/Borradores/InventarioDocumental.md`
- `ValidacionLegalAR/Borradores/SenalesReferencia.json`
- `ValidacionLegalAR/Borradores/MatrizValidacion.json`
- `ValidacionLegalAR/Borradores/MatrizValidacion.md`
- `ValidacionLegalAR/Borradores/ReporteValidacionLegal.md`
