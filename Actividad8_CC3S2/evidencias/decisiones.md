# Decisiones de Prueba

## Contratos verificados por cada prueba

- **test_mre_precision.py** → Garantiza precisión en cálculos monetarios y manejo correcto de errores de redondeo.
- **test_estabilidad_semillas.py** → Garantiza reproducibilidad de resultados bajo semillas fijas.
- **test_invariantes_inventario.py** → Verifica el invariante “agregar N, remover N → total=0 e items=0” y “agregar N, actualizar a 0 → estado equivalente”.
- **test_mensajes_error.py** → Verifica que mensajes de excepción contengan contexto accionable.
- **test_descuentos_parametrizados.py** → Garantiza que los descuentos se aplican correctamente.
- **test_rgr_precision_rojo.py / verde.py** → Validan regresiones en cálculos por precisión binaria.

---

## Variables y efecto observable

- **DISCOUNT_RATE** → Afecta directamente el total calculado; probado en `test_descuentos_parametrizados.py`.
- **TAX_RATE** → No implementada directamente, pero su existencia implicaría tests similares a los de descuento.
- **random.seed() / faker.seed_instance()** → Afectan reproducibilidad; probados en `test_estabilidad_semillas.py`.

---

## Casos borde considerados y donde se prueban

- **Precio cero** → `test_mre_precision.py` y `test_invariantes_inventario.py`.
- **Cantidad negativa** → `test_mensajes_error.py`.
- **Actualización de cantidad a cero** → `test_invariantes_inventario.py`.
- **Errores de precisión binaria** → `test_mre_precision.py` y `test_rgr_precision_rojo.py`.
- **Aplicación de descuento límite (0% y 100%)** → `test_descuentos_parametrizados.py`.