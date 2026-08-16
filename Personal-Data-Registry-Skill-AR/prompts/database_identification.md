# Identificación de Bases

## Objetivo

Traducir el relevamiento y el escaneo a bases concretas, cada una con finalidad y responsables.

## Reglas

- Separar bases por finalidad.
- Separar bases internas y externas si el tratamiento cambia.
- Marcar si una base podría contener datos sensibles.
- Marcar si una base involucra terceros o transferencias internacionales.
- Si el caso es fintech, healthtech, HR o videovigilancia, contrastar con `references/sector_templates.md`.

## Formato de salida

- `RegistroDatosAAIP/Borradores/BasesDetectadas.json`
- `RegistroDatosAAIP/Borradores/BasesDetectadas.md`

## Cierre obligatorio

```text
STOP_FOR_USER
NEXT_ACTION: Confirme las bases detectadas y su finalidad antes de generar borradores por base.
```
