---
name: terminos-privacidad-argentina
description: >
  Genera materiales preparatorios para Términos y Condiciones y Política de Privacidad
  para apps web y móviles en Argentina, incluyendo datos personales, cookies, tracking,
  anuncios, geolocalización, permisos móviles y coordinación entre ambos documentos.
metadata:
  short-description: Preparación guiada de T&C y Política de Privacidad para apps
---

# Términos y Condiciones + Política de Privacidad (Argentina)

Este skill organiza la preparación de documentación legal base para productos digitales.

- **Directorio de salida:** `LegalesAppAR/` en el directorio de trabajo actual.
- **Flujo:** Intake -> Producto -> Datos -> Privacidad -> Términos -> Cookies/Ads -> Permisos móviles -> Revisión final.
- **Objetivo:** Reducir contradicciones y omisiones frecuentes en documentos legales de apps y SaaS.
- **Regla operativa crítica:** No redactar la política de privacidad sin mapear antes qué datos se recolectan, para qué y con qué terceros.

## Puertas de Confirmación Obligatoria (STOP_FOR_USER)

El agente debe detenerse y esperar confirmación en estas etapas:

- `intake`: Confirmar producto, titular del servicio y público objetivo.
- `data-mapping`: Confirmar tipos de datos, tracking, terceros y permisos.
- `privacy`: Confirmar la matriz de privacidad antes del borrador final.
- `terms`: Confirmar reglas de uso, contenido, pagos o baja si aplica.
- `final-review`: Confirmar ambos documentos antes de publicarlos.

## Flujo de Trabajo

### 1. Relevamiento inicial

Lea `prompts/intake.md` y releve:

- titular del servicio;
- tipo de producto;
- modelo de negocio;
- usuarios;
- país objetivo;
- si hay cuentas, pagos, comunidad, anuncios o compras.

### 2. Mapa del servicio

Lea `prompts/product_rules.md`.

Para ordenar funciones y módulos:

```bash
python3 tools/build_service_map.py --input LegalesAppAR/Borradores/IntakeLegalApp.json --out-dir LegalesAppAR/Borradores
```

### 3. Mapeo de datos

Lea `prompts/data_mapping.md`, `prompts/cookies_ads.md` y `prompts/mobile_permissions.md`.

El agente debe distinguir:

- datos de cuenta;
- datos de uso;
- cookies y tracking;
- datos de pagos;
- geolocalización;
- cámara, micrófono, contactos o galería;
- datos sensibles o biométricos;
- terceros y vendors.

### 4. Matriz de privacidad

Lea `prompts/privacy_requirements.md` y `references/privacy_rules_argentina.md`.

Para consolidar la matriz:

```bash
python3 tools/build_privacy_matrix.py --input LegalesAppAR/Borradores/IntakeLegalApp.json --out-dir LegalesAppAR/Borradores
```

### 5. Matriz de términos

Lea `prompts/terms_requirements.md` y `references/terms_rules_argentina.md`.

Para ordenar reglas del servicio:

```bash
python3 tools/build_terms_matrix.py --input LegalesAppAR/Borradores/IntakeLegalApp.json --out-dir LegalesAppAR/Borradores
```

### 6. Borradores coordinados

Lea `references/clause_matrix.md`.

Para consolidar ambos documentos:

```bash
python3 tools/build_legal_docs.py \
  --intake LegalesAppAR/Borradores/IntakeLegalApp.json \
  --service-map LegalesAppAR/Borradores/MapaServicio.json \
  --privacy LegalesAppAR/Borradores/MatrizPrivacidad.json \
  --terms LegalesAppAR/Borradores/MatrizTerminos.json \
  --out-dir LegalesAppAR/Borradores
```

### 7. Revisión final

Lea `prompts/final_review.md`.

## Recursos

- Reglas generales: `references/workflow_rules.md`
- Privacidad en Argentina: `references/privacy_rules_argentina.md`
- Reglas de términos: `references/terms_rules_argentina.md`
- Cookies y tracking: `references/cookie_tracking_rules.md`
- Matriz de cláusulas: `references/clause_matrix.md`
- Especialización futura: `references/specialization_paths.md`

## Entregables esperados

Como mínimo, el skill debe producir:

- `LegalesAppAR/Borradores/IntakeLegalApp.json`
- `LegalesAppAR/Borradores/MapaServicio.md`
- `LegalesAppAR/Borradores/MatrizPrivacidad.md`
- `LegalesAppAR/Borradores/MatrizTerminos.md`
- `LegalesAppAR/Borradores/PoliticaPrivacidad.md`
- `LegalesAppAR/Borradores/TerminosYCondiciones.md`
