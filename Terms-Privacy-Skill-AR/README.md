# Términos y Condiciones + Política de Privacidad (Argentina)

Este repositorio contiene una **Skill** para agentes de IA diseñada para preparar borradores de **Términos y Condiciones** y **Política de Privacidad** para aplicaciones web, móviles y servicios digitales orientados a Argentina.

La skill está pensada para freelancers, startups, SaaS, apps móviles, marketplaces, productos con login y plataformas que necesitan documentación legal básica pero coherente con su operación real.

## ¿Qué hace esta Skill?

La skill ayuda a:

1. **Mapear el producto**: web, app móvil, SaaS, marketplace, comunidad, contenido, ecommerce.
2. **Mapear datos y tracking**: registro, analytics, cookies, geolocalización, biometría, cámara, pagos, soporte.
3. **Distinguir dos documentos distintos**:
   - Términos y Condiciones;
   - Política de Privacidad.
4. **Generar borradores coordinados** para que no se contradigan entre sí.
5. **Marcar riesgos** de consentimiento, menores, terceros, anuncios, transferencias internacionales y datos sensibles.

## Base conceptual

La skill parte de una regla simple:

- los **Términos y Condiciones** regulan el uso del servicio;
- la **Política de Privacidad** explica el tratamiento de datos personales.

No conviene mezclar ambas cosas en un solo texto improvisado.

## Estructura

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── prompts/
│   ├── intake.md
│   ├── product_rules.md
│   ├── data_mapping.md
│   ├── privacy_requirements.md
│   ├── terms_requirements.md
│   ├── cookies_ads.md
│   ├── mobile_permissions.md
│   └── final_review.md
├── references/
│   ├── workflow_rules.md
│   ├── privacy_rules_argentina.md
│   ├── terms_rules_argentina.md
│   ├── cookie_tracking_rules.md
│   ├── clause_matrix.md
│   └── specialization_paths.md
└── tools/
    ├── build_service_map.py
    ├── build_privacy_matrix.py
    ├── build_terms_matrix.py
    └── build_legal_docs.py
```

## Uso básico

Una vez instalada en tu entorno de IA, podés iniciar el flujo diciendo:

> *"Usá la skill legal de términos y privacidad para preparar los documentos de mi app."*

La skill trabaja sobre un directorio de salida llamado `LegalesAppAR/`.

## Alcance

Esta skill es especialmente útil para:

- apps móviles;
- SaaS;
- plataformas con cuentas de usuario;
- productos con analytics;
- soluciones con cookies;
- apps con geolocalización o cámara;
- servicios con anuncios o monetización.

## Posibilidad de especialización

Esta skill puede evolucionar de dos maneras:

- **v2**: más cobertura dentro del mismo repo;
- **v3**: especialización por vertical o tipo de producto.

### Qué sería una v2

Una v2 expande la misma skill.

Ejemplos:

- distinguir mejor cookies funcionales vs marketing;
- endurecer biometría, menores y datos sensibles;
- mejorar el tratamiento de geolocalización y permisos móviles;
- reforzar ads, remarketing y SDKs;
- generar matrices más precisas para cuentas, pagos y contenido.

### Qué sería una v3

Una v3 ya no es solo expansión: es **especialización**.

Eso significa adaptar la skill a un vertical concreto, por ejemplo:

- ecommerce;
- marketplace;
- healthtech;
- fintech;
- edtech;
- comunidad o red social.

### Cómo se haría

Hay dos opciones:

#### Opción 1: especializar este mismo repo

Se agregan ramas sectoriales dentro del mismo repo.

Eso implicaría tocar:

- [SKILL.md](/home/dev-flow/Terms-Privacy-Skill-AR/SKILL.md)
- [references/privacy_rules_argentina.md](/home/dev-flow/Terms-Privacy-Skill-AR/references/privacy_rules_argentina.md)
- [references/terms_rules_argentina.md](/home/dev-flow/Terms-Privacy-Skill-AR/references/terms_rules_argentina.md)
- [references/cookie_tracking_rules.md](/home/dev-flow/Terms-Privacy-Skill-AR/references/cookie_tracking_rules.md)
- [references/clause_matrix.md](/home/dev-flow/Terms-Privacy-Skill-AR/references/clause_matrix.md)
- [tools/build_privacy_matrix.py](/home/dev-flow/Terms-Privacy-Skill-AR/tools/build_privacy_matrix.py)
- [tools/build_terms_matrix.py](/home/dev-flow/Terms-Privacy-Skill-AR/tools/build_terms_matrix.py)
- [tools/build_legal_docs.py](/home/dev-flow/Terms-Privacy-Skill-AR/tools/build_legal_docs.py)

#### Opción 2: crear una skill derivada

Se usa este repo como base y se crea una variante especializada:

- `Terms-Privacy-Skill-AR-Ecommerce`
- `Terms-Privacy-Skill-AR-Healthtech`
- `Terms-Privacy-Skill-AR-Marketplace`

### Qué cambiaría una v3 real

Cambiarían estas piezas:

1. mapa de datos;
2. matriz de cláusulas;
3. advertencias legales;
4. terceros típicos;
5. riesgos regulatorios.

La explicación detallada queda también en:

- [specialization_paths.md](/home/dev-flow/Terms-Privacy-Skill-AR/references/specialization_paths.md)

## Aviso

La skill genera **borradores preparatorios**. No reemplaza revisión legal profesional cuando hay:

- datos sensibles;
- biometría;
- menores;
- salud;
- publicidad comportamental intensiva;
- marketplaces complejos;
- fintech o tratamientos regulados;
- transferencias internacionales relevantes.
