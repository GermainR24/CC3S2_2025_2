**Resumen de Cobertura y Plan de Mejora**

**Fecha:** 2025-10-07

**Cobertura total actual:** 94%

**Detalle de cobertura incompleta:**

- **src/carrito.py:** líneas 9, 21, 50, 52, 91 no cubiertas (manejo de errores y casos borde).
- **src/shopping_cart.py:** líneas 27, 31 no cubiertas (casos de descuentos y cálculos extremos).
- **tests/from src.py:** cobertura 0% (falta de tests o implementación pendiente).
- **tests/test_rgr_precision_verde.py:** cobertura 44%, líneas 11-16 no cubiertas (casos de precisión numérica).

**Plan para aumentar cobertura:**

1. **Casos borde y excepciones en carrito.py** — Añadir tests para remover cantidades parcialmente, actualizar cantidades a cero o negativas, validar mensajes de error.
2. **Tests adicionales en shopping_cart.py** — Cubrir casos de cálculo con descuentos, precios límites y validación de redondeo.
3. **Completar tests en tests/from src.py** — Implementar pruebas para módulos pendientes.
4. **Mejorar test_rgr_precision_verde.py** — Añadir casos de precisión binaria y acumulación de errores para robustez.

**Meta:** Alcanzar ≥95% de cobertura en próximas iteraciones.