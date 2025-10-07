# Diff Refactor

## Cambio: Creacion de tests nuevos

### Antes
No existian pruebas automatizadas para los criterios solicitados (marcadores smoke/regression, invariantes, estabilidad, MREs, mensajes de error).

### Despues
Se añadieron nuevos tests en la carpeta `tests/`:

- `tests/test_markers.py`: Pruebas con marcadores `@pytest.mark.smoke` y `@pytest.mark.regression`.
- `tests/test_estabilidad_semillas.py`: Validacion de estabilidad usando semillas fijas.
- `tests/test_invariantes_inventario.py`: Verificacion de invariantes de inventario.
- `tests/test_mensajes_error.py`: Validacion de contrato de mensajes de error.
- `tests/test_mre_precision.py`: MREs para errores identificados.

**Justificacion**: Se ampliaron las pruebas para cubrir nuevos criterios de calidad y asegurar estabilidad, observabilidad, invariantes e informacion util ante errores, facilitando deteccion temprana de regresiones.
