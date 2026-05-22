# Reglas de localización argentina

## Objetivo

Detectar cuando un documento argentino parece haber quedado contaminado por plantillas o marcos de otros países.

## Señales impropias frecuentes

- `RGPD`
- `GDPR`
- `CNIPA`
- `Delaware law`
- `NIF`
- `CIF`
- `vosotros`
- `ordenador` cuando el resto del documento está en castellano rioplatense

## Señales argentinas útiles

- `AAIP`
- `INPI`
- `DNDA`
- `ARCA`
- `BCRA`
- `Ley 25.326`
- `Ley 25.506`
- `Ley 11.723`
- `Ley 24.481`
- `Ley 27.506`

## Criterio

Una señal extranjera no siempre invalida el documento. Puede aparecer en:

- comparaciones;
- contratos internacionales;
- antecedentes;
- exportación de servicios.

La skill debe diferenciar entre:

- `impropio`;
- `justificado`;
- `requiere revisión`.
