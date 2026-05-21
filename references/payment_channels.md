# Canales de cobro

La skill debe distinguir al menos estos canales:

- `banco_local`: transferencia directa a cuenta bancaria local del exportador;
- `plataforma_cobro`: pasarela o plataforma intermediaria con liquidacion posterior;
- `wallet_cripto`: cobro en criptoactivos o equivalente;
- `mixto`: combinacion de mas de un canal;
- `Pendiente`: no definido.

## Regla de trabajo

El canal de cobro cambia el riesgo operativo.

- `banco_local` suele ser el camino mas claro para soporte documental;
- `plataforma_cobro` requiere revisar mejor el circuito de ingreso y respaldo;
- `wallet_cripto` debe tratarse como alto riesgo;
- `Pendiente` no permite cerrar el analisis cambiario.
