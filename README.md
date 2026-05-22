# Validación de Documentación Legal (Argentina)

Este repositorio contiene una **Skill complementaria** para agentes de IA diseñada para revisar documentos legales y regulatorios preparados para Argentina.

No reemplaza revisión profesional. Su función es hacer un **control de calidad transversal** sobre materiales generados por otras skills o por equipos internos.

## ¿Qué hace esta Skill?

La skill ayuda a:

1. **Inventariar documentos**: Markdown, texto, JSON y PDF.
2. **Detectar señales de localización incorrecta**: RGPD, CNIPA, Delaware, formatos impropios o terminología no argentina.
3. **Revisar referencias legales**: leyes, organismos y nomenclaturas argentinas.
4. **Controlar formato**: fechas, moneda, CUIT/CUIL, expedientes y tamaño A4 en PDF si el archivo está disponible.
5. **Emitir un reporte** con semáforo por dimensión: lenguaje, referencias, contexto, formato y PDF.

## Base conceptual

Esta skill no crea el documento principal. Funciona como una **meta-skill de QA legal/documental**.

Se puede usar al final de cualquiera de estas familias:

- marca;
- privacidad;
- AAIP;
- DNDA;
- INPI;
- contratos;
- exportación de servicios;
- economía del conocimiento.

## Estructura

```text
.
├── SKILL.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── agents/
│   └── openai.yaml
├── prompts/
│   ├── intake.md
│   ├── document_inventory.md
│   ├── language_review.md
│   ├── legal_references_check.md
│   ├── format_validation.md
│   └── final_review.md
├── references/
│   ├── official_sources.md
│   ├── argentina_localization_rules.md
│   ├── validation_rules.md
│   └── format_rules.md
└── tools/
    ├── scan_document_text.py
    ├── check_reference_signals.py
    ├── build_validation_matrix.py
    └── build_validation_report.py
```

## Uso básico

Una vez instalada en tu entorno de IA, podés iniciar el flujo diciendo:

> *"Usá la skill de validación legal para revisar la carpeta de borradores."*

La skill trabaja sobre un directorio de salida llamado `ValidacionLegalAR/`.

## Casos útiles

Esta skill es especialmente útil para:

- revisar salidas de otras skills legales;
- detectar arrastres de normas o terminología extranjeras;
- uniformar español y formato argentino;
- chequear si un PDF final quedó en A4;
- dejar una bitácora de QA antes de enviar o publicar.

## Alcance

La skill puede revisar:

- `.md`
- `.txt`
- `.json`
- `.pdf`

## Aviso

La skill genera **observaciones, semáforos y reportes preparatorios**. No certifica cumplimiento legal pleno ni reemplaza revisión profesional cuando el caso es sensible o regulado.
