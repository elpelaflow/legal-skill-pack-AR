---
name: factura-exportacion-servicios-argentina
description: >
  Prepara materiales para facturacion de exportacion de servicios desde Argentina:
  lectura de contrato, guia de factura E, matriz fiscal orientativa y checklist
  cambiario para cobro y liquidacion de divisas.
metadata:
  short-description: Preparación guiada para factura E y cobro del exterior
---

# Facturación de Exportación de Servicios (Argentina)

Este skill organiza la preparación de materiales para facturar servicios al exterior.

- **Directorio de salida:** `FacturaExportacionAR/` en el directorio de trabajo actual.
- **Flujo:** Intake -> Contrato -> Clasificación -> Factura E -> Impuestos -> Cambios -> Revisión final.
- **Objetivo:** Convertir un acuerdo comercial con cliente del exterior en un instructivo fiscal y cambiario operativo.
- **Regla operativa crítica:** No responder impuestos o cambios sin separar primero tipo de servicio, moneda, cobro y canal de liquidación.

## Puertas de Confirmación Obligatoria (STOP_FOR_USER)

El agente debe detenerse y esperar confirmación en estas etapas:

- `intake`: Confirmar contribuyente, régimen fiscal y cliente exterior.
- `contract-review`: Confirmar servicio, país, moneda y forma de pago.
- `invoice`: Confirmar campos críticos de factura E antes del borrador final.
- `tax`: Confirmar hipótesis impositivas.
- `fx`: Confirmar banco, cuenta receptora y circuito de cobro.
- `final-review`: Confirmar guía final antes de usarla operativamente.

## Flujo de Trabajo

### 1. Relevamiento inicial

Lea `prompts/intake.md` y releve:

- contribuyente;
- CUIT;
- régimen fiscal;
- tipo de servicio;
- país del cliente;
- moneda;
- medio de cobro;
- fecha estimada de facturación;
- fecha estimada de cobro.

### 2. Lectura del contrato

Lea `prompts/contract_review.md` y `references/service_classification.md`.

Para detectar señales del acuerdo:

```bash
python3 tools/parse_contract_signals.py \
  --contract /ruta/al/contrato.txt \
  --out-dir FacturaExportacionAR/Borradores
```

### 3. Guía de factura E

Lea `prompts/invoice_requirements.md` y `references/invoice_e_rules.md`.

Para ordenar el comprobante:

```bash
python3 tools/build_invoice_matrix.py \
  --intake FacturaExportacionAR/Borradores/IntakeFacturaE.json \
  --contract FacturaExportacionAR/Borradores/SenalesContratoExportacion.json \
  --out-dir FacturaExportacionAR/Borradores
```

### 4. Matriz fiscal

Lea `prompts/tax_matrix.md` y `references/tax_rules.md`.

Para preparar la matriz orientativa:

```bash
python3 tools/build_tax_matrix.py \
  --intake FacturaExportacionAR/Borradores/IntakeFacturaE.json \
  --contract FacturaExportacionAR/Borradores/SenalesContratoExportacion.json \
  --invoice FacturaExportacionAR/Borradores/MatrizFacturaE.json \
  --out-dir FacturaExportacionAR/Borradores
```

### 5. Checklist cambiario

Lea `prompts/fx_settlement.md` y `references/fx_rules.md`.

Para preparar el circuito de cobro y liquidación:

```bash
python3 tools/build_fx_checklist.py \
  --intake FacturaExportacionAR/Borradores/IntakeFacturaE.json \
  --contract FacturaExportacionAR/Borradores/SenalesContratoExportacion.json \
  --tax FacturaExportacionAR/Borradores/MatrizFiscalExportacion.json \
  --out-dir FacturaExportacionAR/Borradores
```

### 6. Guía final consolidada

Lea `prompts/final_review.md`.

Para consolidar la salida final:

```bash
python3 tools/build_export_invoice_guide.py \
  --intake FacturaExportacionAR/Borradores/IntakeFacturaE.json \
  --contract FacturaExportacionAR/Borradores/SenalesContratoExportacion.json \
  --invoice FacturaExportacionAR/Borradores/MatrizFacturaE.json \
  --tax FacturaExportacionAR/Borradores/MatrizFiscalExportacion.json \
  --fx FacturaExportacionAR/Borradores/ChecklistCambiosExportacion.json \
  --out-dir FacturaExportacionAR/Borradores
```

## Recursos

- Reglas de trabajo: `references/workflow_rules.md`
- Factura E: `references/invoice_e_rules.md`
- Clasificación del servicio: `references/service_classification.md`
- Reglas fiscales: `references/tax_rules.md`
- Reglas cambiarias: `references/fx_rules.md`
- Canales de cobro: `references/payment_channels.md`

## Entregables esperados

Como mínimo, el skill debe producir:

- `FacturaExportacionAR/Borradores/IntakeFacturaE.json`
- `FacturaExportacionAR/Borradores/SenalesContratoExportacion.md`
- `FacturaExportacionAR/Borradores/MatrizFacturaE.md`
- `FacturaExportacionAR/Borradores/MatrizFiscalExportacion.md`
- `FacturaExportacionAR/Borradores/ChecklistCambiosExportacion.md`
- `FacturaExportacionAR/Borradores/GuiaFacturaEExportacion.md`
