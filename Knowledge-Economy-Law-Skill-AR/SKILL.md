---
name: economia-conocimiento-argentina
description: >
  Prepara materiales de elegibilidad, evidencia técnica, solicitud orientada al
  régimen de promoción de la Economía del Conocimiento en Argentina, junto con
  checklist de permanencia y estimación orientativa de beneficios.
metadata:
  short-description: Preparación guiada para Ley de Economía del Conocimiento
---

# Economía del Conocimiento (Argentina)

Este skill organiza la preparación de materiales para ingreso y permanencia en el régimen.

- **Directorio de salida:** `RegistroLEC/` en el directorio de trabajo actual.
- **Flujo:** Intake -> Escaneo técnico -> Mapeo de elegibilidad -> Evidencia -> Requisitos adicionales -> Solicitud -> Permanencia -> Beneficios -> Revisión final.
- **Objetivo:** Traducir estructura empresarial y técnica a un expediente ordenado y defendible.
- **Regla operativa crítica:** No afirmar elegibilidad ni proyectar beneficios sin separar antes actividad promovida, evidencia técnica y requisitos adicionales.

## Puertas de Confirmación Obligatoria (STOP_FOR_USER)

El agente debe detenerse y esperar confirmación en estas etapas:

- `intake`: Confirmar empresa, actividad principal, tamaño y proyecto analizado.
- `eligibility`: Confirmar qué actividades promovidas se invocarán y cuáles no.
- `technical-evidence`: Confirmar la matriz de evidencia antes del borrador de solicitud.
- `application`: Confirmar datos societarios, fiscales y narrativos antes del borrador final.
- `benefits`: Confirmar hipótesis de cálculo.
- `final-review`: Confirmar expediente y checklist de permanencia.

## Flujo de Trabajo

### 1. Relevamiento inicial

Lea `prompts/intake.md` y releve:

- razón social y CUIT;
- tamaño de empresa;
- actividad principal;
- exportaciones;
- nómina afectada;
- certificaciones;
- proyecto o unidad de negocio promovida;
- fecha deseada de presentación.

### 2. Escaneo técnico y señales de actividad

Lea `prompts/eligibility_mapping.md` y `references/eligible_activities_rules.md`.

Para inspeccionar el proyecto:

```bash
python3 tools/scan_eligible_activity_signals.py \
  --project /ruta/al/proyecto \
  --out-dir RegistroLEC/Borradores
```

### 3. Evidencia técnica

Lea `prompts/technical_evidence.md`.

Para consolidar la evidencia:

```bash
python3 tools/build_technical_evidence.py \
  --signals RegistroLEC/Borradores/SenalesActividadElegible.json \
  --out-dir RegistroLEC/Borradores
```

### 4. Borrador de solicitud

### 4. Carril de requisitos adicionales

Lea `references/requirements_paths.md`.

Para sugerir el mejor carril con vacíos de evidencia:

```bash
python3 tools/build_requirement_path.py \
  --input RegistroLEC/Borradores/IntakeLEC.json \
  --signals RegistroLEC/Borradores/SenalesActividadElegible.json \
  --out-dir RegistroLEC/Borradores
```

### 5. Borrador de solicitud

Lea `prompts/registry_application.md` y `references/application_fields.md`.

Para generar el borrador orientado a `F.1278 + TAD`:

```bash
python3 tools/build_registry_draft.py \
  --intake RegistroLEC/Borradores/IntakeLEC.json \
  --signals RegistroLEC/Borradores/SenalesActividadElegible.json \
  --evidence RegistroLEC/Borradores/EvidenciaTecnicaLEC.json \
  --requirements RegistroLEC/Borradores/CarrilRequisitosLEC.json \
  --out-dir RegistroLEC/Borradores
```

### 6. Permanencia y control

Lea `prompts/annual_compliance.md` y `references/maintenance_obligations.md`.

Para preparar el plan de mantenimiento:

```bash
python3 tools/build_compliance_checklist.py \
  --intake RegistroLEC/Borradores/IntakeLEC.json \
  --requirements RegistroLEC/Borradores/CarrilRequisitosLEC.json \
  --out-dir RegistroLEC/Borradores
```

### 7. Estimación orientativa de beneficios

Lea `prompts/benefits_estimation.md` y `references/benefits_rules.md`.

Para generar una proyección simple:

```bash
python3 tools/estimate_benefits.py \
  --input RegistroLEC/Borradores/IntakeLEC.json \
  --out-dir RegistroLEC/Borradores
```

### 8. Revisión final

Lea `prompts/final_review.md`.

## Recursos

- Reglas generales: `references/workflow_rules.md`
- Actividades elegibles: `references/eligible_activities_rules.md`
- Campos del expediente: `references/application_fields.md`
- Carriles de requisitos: `references/requirements_paths.md`
- Permanencia y control: `references/maintenance_obligations.md`
- Beneficios y límites: `references/benefits_rules.md`

## Entregables esperados

Como mínimo, el skill debe producir:

- `RegistroLEC/Borradores/IntakeLEC.json`
- `RegistroLEC/Borradores/SenalesActividadElegible.md`
- `RegistroLEC/Borradores/EvidenciaTecnicaLEC.md`
- `RegistroLEC/Borradores/CarrilRequisitosLEC.md`
- `RegistroLEC/Borradores/SolicitudLEC.md`
- `RegistroLEC/Borradores/ChecklistPermanenciaLEC.md`
- `RegistroLEC/Borradores/EstimacionBeneficiosLEC.md`
