# Reglas fiscales orientativas

La skill debe dejar claras estas capas:

- el comprobante clase `E` documenta la operación de exportación;
- en la factura no corresponde cargar IVA local como si fuera una venta interna;
- puede haber retenciones o impuestos en destino según contrato o país del cliente;
- la existencia de percepciones bancarias, provinciales o financieras no se deduce solo del contrato;
- los derechos de exportación sobre servicios tuvieron reglas específicas en años anteriores y cualquier revisión sobre ese punto debe dejar clara la vigencia aplicable al período analizado.
- SaaS, licencias, soporte o consulting pueden requerir descripciones contractuales mas finas para no mezclar prestaciones distintas.

## Salida esperada

La matriz fiscal debe marcar:

- `aplica_factura_e`;
- `no_cargar_iva_local_como_venta_interna`;
- `retencion_extranjera_visible`;
- `revisar_derechos_historicos_si_aplica`;
- `revisar_percepciones_locales_fuera_del_contrato`.
