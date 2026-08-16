---
name: contrato-desarrollo-software-argentina
description: >
  Genera materiales preparatorios para contratos de desarrollo de software a medida en Argentina.
  Uso: alcance, entregables, aceptación, pagos, confidencialidad, soporte y propiedad intelectual
  para freelancers, startups, software factories y clientes de desarrollo.
metadata:
  short-description: Preparación guiada de contratos de desarrollo de software
---

# Contrato de Desarrollo de Software (Argentina)

Este skill organiza la preparación de un borrador contractual para proyectos de software a medida.

- **Directorio de salida:** `ContratoDesarrolloSoftware/` en el directorio de trabajo actual.
- **Flujo:** Intake -> Alcance -> Entregables -> Pagos -> IP -> Confidencialidad/Datos -> Soporte -> Revisión final.
- **Objetivo:** Reducir ambigüedades contractuales antes de negociar o firmar.
- **Regla operativa crítica:** No redactar la cláusula de propiedad intelectual sin antes separar código preexistente, entregables a medida, componentes de terceros y reservas del proveedor.

## Puertas de Confirmación Obligatoria (STOP_FOR_USER)

El agente debe detenerse y esperar confirmación en estas etapas:

- `intake`: Confirmar partes, proyecto, modalidad y objetivo comercial.
- `scope`: Confirmar alcance, exclusiones y entregables.
- `payment`: Confirmar esquema económico y cronograma.
- `ip`: Confirmar cesión, licencia o reserva de derechos.
- `final-review`: Confirmar el borrador final antes de usarlo en negociación o firma.

## Flujo de Trabajo

### 1. Relevamiento inicial

Lea `prompts/intake.md` y complete:

- partes;
- tipo de proyecto;
- modalidad de prestación;
- país y domicilio contractual;
- plazo estimado;
- objetivo del cliente.

### 2. Definición de alcance

Lea `prompts/scope_definition.md`.

Para ordenar el alcance, use:

```bash
python3 tools/build_scope_matrix.py --input ContratoDesarrolloSoftware/Borradores/IntakeContrato.json --out-dir ContratoDesarrolloSoftware/Borradores
```

### 3. Entregables y aceptación

Lea `prompts/deliverables_acceptance.md` y `references/acceptance_rules.md`.

El agente debe distinguir entre:

- entregables concretos;
- hitos;
- criterio de aceptación;
- correcciones incluidas;
- cambios fuera de alcance.

### 4. Pagos

Lea `prompts/payment_terms.md` y `references/payment_models.md`.

Para consolidar un esquema base:

```bash
python3 tools/build_payment_schedule.py --input ContratoDesarrolloSoftware/Borradores/IntakeContrato.json --out-dir ContratoDesarrolloSoftware/Borradores
```

### 5. Propiedad intelectual

Lea `prompts/ip_structure.md` y `references/ip_rules_argentina.md`.

Para preparar la matriz de IP:

```bash
python3 tools/build_ip_matrix.py --input ContratoDesarrolloSoftware/Borradores/IntakeContrato.json --out-dir ContratoDesarrolloSoftware/Borradores
```

### 6. Confidencialidad y datos

Lea `prompts/confidentiality_data.md`.

El agente debe marcar:

- información confidencial;
- secretos comerciales;
- accesos del proveedor a ambientes del cliente;
- posible tratamiento de datos personales;
- terceros y proveedores.

### 7. Soporte, garantía y post-entrega

Lea `prompts/support_warranty.md`.

Separar:

- desarrollo inicial;
- garantía de corrección;
- soporte evolutivo;
- mantenimiento posterior.

### 8. Borrador contractual

Lea `references/clause_guide.md`.

Para consolidar el borrador:

```bash
python3 tools/build_contract_draft.py \
  --intake ContratoDesarrolloSoftware/Borradores/IntakeContrato.json \
  --scope ContratoDesarrolloSoftware/Borradores/MatrizAlcance.json \
  --payment ContratoDesarrolloSoftware/Borradores/EsquemaPagos.json \
  --ip ContratoDesarrolloSoftware/Borradores/MatrizPI.json \
  --out-dir ContratoDesarrolloSoftware/Borradores
```

### 9. Revisión final

Lea `prompts/final_review.md`.

## Recursos

- Reglas generales: `references/contract_workflow_rules.md`
- Guía de cláusulas: `references/clause_guide.md`
- Reglas de PI en Argentina: `references/ip_rules_argentina.md`
- Aceptación y cambios: `references/acceptance_rules.md`
- Modelos de pago: `references/payment_models.md`

## Entregables esperados

Como mínimo, el skill debe producir:

- `ContratoDesarrolloSoftware/Borradores/IntakeContrato.json`
- `ContratoDesarrolloSoftware/Borradores/MatrizAlcance.md`
- `ContratoDesarrolloSoftware/Borradores/EsquemaPagos.md`
- `ContratoDesarrolloSoftware/Borradores/MatrizPI.md`
- `ContratoDesarrolloSoftware/Borradores/ContratoDesarrolloSoftware.md`
