# Facturación de Exportación de Servicios (Argentina)

Este repositorio contiene una **Skill** para agentes de IA diseñada para preparar materiales de facturación de exportación de servicios desde Argentina.

La skill está pensada para freelancers, software factories, estudios, SaaS y startups que venden servicios al exterior y necesitan ordenar:

- el análisis del contrato;
- la emisión correcta de **factura E**;
- la matriz fiscal básica;
- y el circuito cambiario posterior.

## ¿Qué hace esta Skill?

La skill ayuda a:

1. **Leer el contrato o resumen comercial** para detectar país, moneda, forma de pago, servicio y aceptación.
2. **Clasificar el servicio exportado** y su nivel de riesgo fiscal/cambiario.
3. **Preparar una guía de factura E** con campos y validaciones operativas.
4. **Armar una matriz impositiva orientativa** con impuestos y alertas.
5. **Armar un checklist cambiario** para cobro y liquidación de divisas.
6. **Consolidar un instructivo final** útil para el developer o contador.
7. **Calificar el canal de cobro** y marcar riesgos por banco, plataforma o cripto.

## Base conceptual

La skill separa cuatro planos:

- contrato;
- comprobante fiscal;
- impuestos;
- cambios.

Esa separación es obligatoria. Una factura E bien emitida no resuelve por sí sola:

- la correcta calificación del servicio;
- el tratamiento impositivo integral;
- ni el cumplimiento cambiario.

## Estructura

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── prompts/
│   ├── intake.md
│   ├── contract_review.md
│   ├── invoice_requirements.md
│   ├── tax_matrix.md
│   ├── fx_settlement.md
│   └── final_review.md
├── references/
│   ├── workflow_rules.md
│   ├── invoice_e_rules.md
│   ├── service_classification.md
│   ├── tax_rules.md
│   ├── fx_rules.md
│   └── payment_channels.md
└── tools/
    ├── parse_contract_signals.py
    ├── build_invoice_matrix.py
    ├── build_tax_matrix.py
    ├── build_fx_checklist.py
    └── build_export_invoice_guide.py
```

## Uso básico

Una vez instalada en tu entorno de IA, podés iniciar el flujo diciendo:

> *"Usá la skill de factura E para revisar este contrato y decirme cómo facturar la exportación de servicios."*

La skill trabaja sobre un directorio de salida llamado `FacturaExportacionAR/`.

## Alcance

Esta skill es especialmente útil para:

- desarrollo de software a medida;
- servicios de diseño o implementación técnica;
- mantenimiento y soporte remoto;
- consulting IT;
- SaaS con cobros B2B al exterior;
- exportación de servicios basados en conocimiento.

## Qué no hace sola

La skill no reemplaza:

- liquidación tributaria definitiva;
- análisis societario internacional;
- validación bancaria;
- ni revisión profesional cuando hay estructuras complejas, cripto, triangulación o PE en otro país.

## Qué suma la v2

La v2 endurece tres cosas:

- distingue mejor el canal de cobro;
- agrega un semáforo fiscal y cambiario más fino;
- y separa mejor `desarrollo`, `soporte`, `consulting` y `SaaS/licencia`.

## Fuentes oficiales base

La skill fue estructurada con fuentes oficiales vigentes al **21 de mayo de 2026**:

- ARCA / exportación de servicios: https://arca.gob.ar/monotributo/exportacion-servicios/
- ARCA / comprobantes clase E: https://www.afip.gob.ar/fe/emision-autorizacion/comprobantes-clase-e.asp
- BCRA / exterior y cambios - texto ordenado: https://www.bcra.gob.ar/Pdfs/Texord/t-excbio.pdf
- InfoLEG / Ley 27.541 (tope de derechos históricamente aplicados): https://servicios.infoleg.gob.ar/infolegInternet/verNorma.do?id=333564

## Aviso

La skill genera **guías operativas y borradores**. No promete determinación fiscal automática cerrada cuando:

- el servicio tiene componentes mixtos;
- intervienen establecimientos permanentes o nexo fiscal en otro país;
- el cobro no sigue el circuito bancario usual;
- hay criptoactivos;
- o el tratamiento cambiario depende de excepciones específicas.
