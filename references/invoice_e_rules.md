# Factura E

Reglas base que la skill debe reflejar:

- la exportación de servicios se documenta con comprobantes clase `E`;
- se puede emitir en moneda extranjera;
- el comprobante debe identificar país de destino y cliente exterior;
- el flujo requiere datos específicos del servicio y de la fecha o condición de pago;
- el punto de venta y la habilitación del comprobante deben estar dados de alta en ARCA.

## Validaciones operativas

- confirmar régimen del emisor;
- confirmar si la emisión será por Comprobantes en Línea, WebService o facturador externo;
- confirmar descripción suficiente del servicio;
- confirmar si la operación surge de contrato, propuesta o orden de compra;
- confirmar datos del cliente exterior.

## Nota sobre moneda

La skill debe dejar asentado que ARCA publica reglas específicas de emisión en moneda extranjera y que deben verificarse al momento de facturar dentro del circuito aplicable.
