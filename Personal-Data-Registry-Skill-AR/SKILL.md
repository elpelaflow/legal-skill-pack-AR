---
name: registro-datos-personales-aaip-argentina
description: >
  Genera materiales preparatorios para inscripción de responsables y bases de datos personales
  ante la AAIP Argentina, incluyendo mapeo de tratamientos, borradores de inscripción, medidas
  de seguridad, procedimiento de derechos del titular y revisión de transferencias internacionales.
metadata:
  short-description: Preparación guiada para cumplimiento AAIP y registro de bases
---

# Registro de Datos Personales (AAIP Argentina)

Este skill organiza la preparación documental para cumplimiento inicial en materia de datos personales en Argentina.

- **Directorio de salida:** `RegistroDatosAAIP/` en el directorio de trabajo actual.
- **Flujo:** Intake -> Escaneo -> Bases detectadas -> Responsable -> Bases -> Seguridad -> Derechos -> Transferencias -> Revisión final.
- **Objetivo:** Reducir errores y omisiones antes de avanzar con trámites o revisiones documentales vinculadas a la AAIP.
- **Regla operativa crítica:** Separar claramente la inscripción del **responsable** de la inscripción de cada **base de datos**.

## Puertas de Confirmación Obligatoria (STOP_FOR_USER)

El agente debe detenerse y esperar confirmación en estas etapas:

- `intake`: Confirmar identidad del responsable, actividad, sistemas y categorías de titulares.
- `databases`: Confirmar las bases detectadas y su finalidad.
- `responsible`: Confirmar los datos del responsable antes de consolidar su borrador.
- `security`: Confirmar el nivel de medidas de seguridad y proveedores críticos.
- `transfers`: Confirmar transferencias internacionales y terceros.
- `final-review`: Confirmar el paquete final antes de usarlo formalmente.

## Flujo de Trabajo

### 1. Relevamiento inicial

Lea `prompts/intake.md` y complete:

- identidad del responsable;
- actividad y modelo de negocio;
- sistemas usados;
- tipos de titulares;
- categorías de datos;
- ubicación de infraestructura y proveedores.

### 2. Escaneo del sistema y documentación

Lea `prompts/system_scan.md`.

Para obtener una primera evidencia estructurada, use:

```bash
python3 tools/scan_data_flows.py --project <ruta> --out-dir RegistroDatosAAIP/analysis
```

### 3. Identificación de bases

Lea `prompts/database_identification.md`, `references/database_taxonomy.md` y `references/sector_templates.md` si el caso es HR, fintech, healthtech o videovigilancia.

Para una propuesta inicial de bases, use:

```bash
python3 tools/suggest_databases.py \
  --intake RegistroDatosAAIP/Borradores/IntakeAAIP.json \
  --scan RegistroDatosAAIP/analysis/data_flows.json \
  --out-dir RegistroDatosAAIP/Borradores
```

### 4. Borrador del responsable

Lea `prompts/responsible_registration.md` y `references/registration_fields.md`.

Para consolidar el borrador:

```bash
python3 tools/build_responsible_draft.py \
  --intake RegistroDatosAAIP/Borradores/IntakeAAIP.json \
  --out-dir RegistroDatosAAIP/Borradores
```

### 5. Borradores por base

Lea `prompts/database_registration.md`.

Para generar fichas por base:

```bash
python3 tools/build_database_registry_draft.py \
  --intake RegistroDatosAAIP/Borradores/IntakeAAIP.json \
  --databases RegistroDatosAAIP/Borradores/BasesDetectadas.json \
  --out-dir RegistroDatosAAIP/Borradores
```

### 6. Medidas de seguridad

Lea `prompts/security_measures.md` y `references/security_rules_res47_2018.md`.

Para una primera estructura documental:

```bash
python3 tools/build_security_plan.py \
  --intake RegistroDatosAAIP/Borradores/IntakeAAIP.json \
  --databases RegistroDatosAAIP/Borradores/BasesDetectadas.json \
  --out-dir RegistroDatosAAIP/Borradores
```

### 7. Derechos del titular

Lea `prompts/rights_procedure.md`.

Para generar el procedimiento:

```bash
python3 tools/build_rights_procedure.py \
  --intake RegistroDatosAAIP/Borradores/IntakeAAIP.json \
  --out-dir RegistroDatosAAIP/Borradores
```

### 8. Transferencias internacionales y terceros

Lea `prompts/international_transfers.md`.

El agente debe marcar:

- nube fuera de Argentina;
- soporte remoto desde otros países;
- vendors con acceso a datos;
- servicios de emailing, analytics, CRM o ticketing;
- cesiones o disponibilizaciones a terceros.

Para consolidar el borrador, use:

```bash
python3 tools/build_international_transfers.py \
  --intake RegistroDatosAAIP/Borradores/IntakeAAIP.json \
  --databases RegistroDatosAAIP/Borradores/BasesDetectadas.json \
  --out-dir RegistroDatosAAIP/Borradores
```

### 9. Revisión final

Lea `prompts/final_review.md` y `references/inspection_readiness.md`.

Para cerrar con una matriz de madurez e inspección, use:

```bash
python3 tools/build_inspection_checklist.py \
  --intake RegistroDatosAAIP/Borradores/IntakeAAIP.json \
  --databases RegistroDatosAAIP/Borradores/BasesDetectadas.json \
  --security RegistroDatosAAIP/Borradores/PlanSeguridadAAIP.json \
  --out-dir RegistroDatosAAIP/Borradores
```

## Recursos

- Flujo general: `references/aaip_workflow_rules.md`
- Campos de registro: `references/registration_fields.md`
- Medidas de seguridad: `references/security_rules_res47_2018.md`
- Inspección y evidencia: `references/inspection_readiness.md`
- Taxonomía de bases: `references/database_taxonomy.md`
- Plantillas sectoriales: `references/sector_templates.md`

## Entregables esperados

Como mínimo, el skill debe producir:

- `RegistroDatosAAIP/Borradores/IntakeAAIP.json`
- `RegistroDatosAAIP/analysis/data_flows.json`
- `RegistroDatosAAIP/Borradores/BasesDetectadas.md`
- `RegistroDatosAAIP/Borradores/ResponsableAAIP.md`
- `RegistroDatosAAIP/Borradores/Base_<NOMBRE>.md`
- `RegistroDatosAAIP/Borradores/PlanSeguridadAAIP.md`
- `RegistroDatosAAIP/Borradores/ProcedimientoDerechosTitular.md`
- `RegistroDatosAAIP/Borradores/TransferenciasInternacionales.md`
- `RegistroDatosAAIP/Borradores/ChecklistInspeccionAAIP.md`
