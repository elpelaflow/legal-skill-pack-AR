# Relevamiento Inicial

## Objetivo

Recolectar el contexto del producto y del tratamiento de datos.

## Preguntas mínimas

1. ¿Quién opera el servicio?
2. ¿Es web, móvil o ambos?
3. ¿Tiene cuentas de usuario?
4. ¿Recolecta datos personales? ¿Cuáles?
5. ¿Usa analytics, cookies o SDKs?
6. ¿Usa geolocalización, cámara, micrófono o biometría?
7. ¿Tiene pagos, suscripciones o anuncios?
8. ¿Hay menores o datos sensibles?

## Formato de salida

- `LegalesAppAR/Borradores/IntakeLegalApp.json`
- `LegalesAppAR/Borradores/IntakeLegalApp.md`

## JSON sugerido

```json
{
  "service_owner": "",
  "service_name": "",
  "platforms": [],
  "service_summary": "",
  "user_accounts": false,
  "personal_data_categories": [],
  "sensitive_data": false,
  "minor_data": false,
  "cookies_or_trackers": [],
  "mobile_permissions": [],
  "payments": false,
  "ads_monetization": false,
  "third_parties": [],
  "notes": ""
}
```

## Cierre obligatorio

```text
STOP_FOR_USER
NEXT_ACTION: Confirme el producto, los datos tratados y los terceros antes de seguir.
```
