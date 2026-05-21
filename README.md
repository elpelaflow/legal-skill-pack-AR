# Acuerdos de Confidencialidad (NDA) - Argentina

Este repositorio contiene una **Skill** para agentes de IA diseñada para preparar borradores de **Acuerdos de Confidencialidad** en Argentina, tanto **unilaterales** como **mutuos**, listos para revisión y para su posterior firma electrónica o digital.

La skill está pensada para freelancers, startups, software factories, estudios y empresas que necesitan ordenar con rapidez y claridad:

- qué información se compartirá;
- quién la recibe;
- para qué fin se comparte;
- cuánto dura la obligación de confidencialidad;
- qué excepciones aplican;
- y cómo dejar el documento listo para su firma.

## ¿Qué hace esta Skill?

La skill ayuda a:

1. **Definir el tipo de NDA**:
   - unilateral;
   - mutuo.
2. **Delimitar la información confidencial** y sus exclusiones.
3. **Definir el propósito permitido** de la divulgación.
4. **Ordenar plazo, devolución/destrucción, remedios e incumplimiento**.
5. **Preparar un borrador listo para firma**, con observaciones sobre firma electrónica y firma digital en Argentina.

## Alcance reforzado de esta versión

La skill contempla especialmente escenarios típicos del sector software:

- acceso a repositorios;
- documentación técnica;
- pricing y propuestas;
- credenciales o accesos temporales;
- datasets o información de clientes;
- sharing con empleados, asesores o contratistas bajo necesidad de conocimiento.

## Base conceptual y jurídica

La skill parte de una regla práctica:

- un NDA útil no es un documento “agresivo” por sí mismo;
- es un documento claro sobre alcance, uso permitido, excepciones y duración.

También diferencia entre:

- **firma electrónica**;
- **firma digital** conforme Ley 25.506.

La skill no firma documentos por sí sola, pero puede dejar el texto y el paquete de firma preparados.

## Estructura

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── prompts/
│   ├── intake.md
│   ├── nda_type.md
│   ├── confidential_information.md
│   ├── exclusions_and_term.md
│   ├── return_destroy_remedies.md
│   ├── signature_mode.md
│   └── final_review.md
├── references/
│   ├── workflow_rules.md
│   ├── nda_clause_guide.md
│   ├── signature_rules_argentina.md
│   ├── confidentiality_scope_rules.md
│   └── specialization_paths.md
└── tools/
    ├── build_confidentiality_matrix.py
    ├── build_signature_packet.py
    └── build_nda_draft.py
```

## Uso básico

Una vez instalada en tu entorno de IA, podés iniciar el flujo diciendo:

> *"Usá la skill NDA para preparar un acuerdo de confidencialidad para esta negociación."*

La skill trabaja sobre un directorio de salida llamado `AcuerdoConfidencialidad/`.

## Alcance

Esta skill sirve especialmente para:

- discovery comercial;
- demos o pilotos;
- due diligence técnica;
- conversaciones precontratuales;
- acceso a repositorios o documentación;
- intercambio de pricing, arquitectura o roadmap;
- procesos de contratación o partnership.

## Aviso

La skill genera **borradores preparatorios**. No reemplaza revisión legal profesional cuando hay:

- jurisdicciones múltiples;
- secreto industrial crítico;
- multas elevadas o penalidades complejas;
- cesión o licencia vinculada al NDA;
- datos sensibles o regulados;
- negociación con grandes empresas o inversores institucionales.
