# analisis

---

### A4. Redondeos acumulados vs. final

El objetivo de esta prueba es analizar si el resultado total del carrito cambia dependiendo del momento en que se realiza el redondeo:

- **Redondeo por ítem (acumulado):** se redondea cada subtotal antes de sumarlos.
- **Redondeo final:** se suman los subtotales exactos y luego se redondea el total al final.

---

### Caso 1 – Valores que no generan diferencia

| Producto | Precio unitario | Cantidad | Subtotal exacto | Redondeo por ítem | Redondeo final |
| --- | --- | --- | --- | --- | --- |
| a | 0.3333 | 3 | 0.9999 | 1.00 |  |
| b | 0.6667 | 3 | 2.0001 | 2.00 |  |
| **Total** |  |  | **3.0000** | **3.00** | **3.00** |
| **Diferencia** |  |  |  |  | **0.00** |

En este caso, **ambos metodos coinciden** (test `test_redondeo_acumulado_vs_final` pasa).

---

### Caso 2 – Valores que si generan diferencia

| Producto | Precio unitario | Cantidad | Subtotal exacto | Redondeo por ítem | Redondeo final |
| --- | --- | --- | --- | --- | --- |
| a | 0.335 | 3 | 1.005 | 1.01 |  |
| b | 0.665 | 3 | 1.995 | 2.00 |  |
| **Total** |  |  | **3.000** | **3.01** | **3.00** |
| **Diferencia** |  |  |  |  | **+0.01** |

En este caso, hay una **diferencia de 0.01** entre ambos metodos debido al **acumulado de redondeos**.

El test `test_redondeo_acumulado_vs_final_difiere` **detecta correctamente esta diferencia**.

---

### B2. Verde — Exclusión documentada

Durante la etapa **Rojo (B1)**, se detectóo que hubo un error de precision en las operaciones con `float` (0.1 + 0.2 ≠ 0.3).

En esta version del sistema, se ha decidido no corregirlo por el momento, ya que no afecta casos reales dentro del alcance actual del carrito.

Por ello, el test se marco con:

```python
@pytest.mark.skip(reason="Contrato: precision binaria no se corrige en esta version")

```

### Motivo de exclusin

- El problema proviene de la representación binaria de los numeros flotantes.
- Cambiar la implementacion implicaría usar `Decimal`, lo cual sera evaluado en la siguiente iteracion.

### Impacto

- Calculos monetarios pueden presentar diferencias minimas (≈ 1e-16).
- No afecta pruebas funcionales actuales, pero puede ser critico en sistemas financieros.

---

en conclusion el etst fue **omitido correctamente** esta **documentado, pero no bloquea el pipeline**.

---

---

### B3. Refactor de suites

**Objetivo:**

Mejorar la legibilidad y la separacion de responsabilidades en las pruebas.

**Cambios realizados:**

- Se agruparon los tests en dos clases:
    - **`TestPrecisionMonetaria`**: pruebas sobre el calculo de totales y redondeo.
    - **`TestPasarelaPagoContratos`**: pruebas de interacción con la pasarela de pago (mockeada).
- No se modifica la lógica del **SUT (`ShoppingCart`)**.
- Se uso **`unittest.mock.Mock`** para validar el contrato de la pasarela.
- Esto facilita la comprension y el mantenimiento de las pruebas, siguiendo el principio **SRP (Single Responsibility Principle)** también en el nivel de testing.

---

**C1. Contratos de pasarela de pago con `mock`**

| Evento simulado | Comportamiento esperado del SUT (`ShoppingCart`) | Resultado del test | Observación |
| --- | --- | --- | --- |
| Pago exitoso (`process_payment` devuelve `True`) | El metodo retorna `True` y se llama exactamente una vez con el monto correcto. | `assert resultado is True` | Flujo normal de cobro. |
| Timeout o error transitorio (`process_payment` lanza `TimeoutError`) | El metodo lanza la excepcion sin reintentar automáticamente. | `pytest.raises(TimeoutError)` | Documenta que el reintento debe ser manual. |
| Rechazo definitivo (`process_payment` devuelve `False`) | El método retorna `False` sin reintentar el pago. | `assert resultado is False` | Caso de pago rechazado por la pasarela. |

---

---

**C3. Umbral de cobertura como *quality gate***

- Se ejecutó:

```bash
pytest --cov=src --cov-report=term-missing --cov-fail-under=90 > out/coverage.txt

```

- Resultado: **Cobertura total = 90.11%**
    
    El umbral minimo del 90% fue alcanzado.
    

### Areas a fortalecer:

- `src/carrito.py`: lineas 9, 21, 50, 52, 60, 68, 91 (manejo de casos de error, validaciones adicionales).
- `src/shopping_cart.py`: líneas 27, 31 (validación y manejo de errores en el pago).

### coverage.txt (extracto):

```
Name                   Stmts   Miss  Cover   Missing
----------------------------------------------------
src/carrito.py            55      7    87%   9, 21, 50, 52, 60, 68, 91
src/shopping_cart.py      29      2    93%   27, 31
TOTAL                     91      9    90%

```

---

**C4. MREs para defectos**

| Test | Pasos | Expectativa | Realidad / Síntoma |
| --- | --- | --- | --- |
| `test_mre_precision_binaria_simple` | 1. Crear un carrito.2. Agregar producto A: precio 0.1.3. Agregar producto B: precio 0.2.4. Calcular total. | Total exacto = 0.3 | Resultado: 0.30000000000000004 debido a error de precision binaria. |
| `test_mre_precision_acumulada` | 1. Crear carrito.2. Agregar 5 productos a precio 0.2.3. Calcular total. | Total exacto = 1.0 | Resultado: ligero desfase por acumulacion de errores de precision. |
| `test_mre_precio_cero` | 1. Crear carrito.2. Agregar producto gratis con precio 0.3. Calcular total. | Total = 0.0 | Total correcto = 0.0, pero contrato no definido si es aceptable o no precio cero. |
| `test_mre_consistencia_carrito_shoppingcart` | 1. Crear un Carrito y un ShoppingCart.2. Agregar 5 items de precio 0.1 a cada uno.3. Comparar totales. | Ambos totales iguales | Puede haber diferencias menores en precision debido a distintas implementaciones. |

---

**D2. Invariantes de inventario**

**Objetivo:**

Verificar que operaciones reversibles no alteran el estado del carrito.

**Invariante testeada:**

"Agregar N, remover N → total=0 e items=0; agregar N, actualizar a 0 → estado equivalente".

**Beneficio:**

Este test asegura que el carrito maneja correctamente cambios repetidos de inventario y previene regresiones donde operaciones de agregar/remover no limpian correctamente el estado interno.

**Por qué previene regresiones:**

Al validar que ciertas secuencias de operaciones devuelven el carrito a un estado esperado, detectamos cambios inesperados en la lógica interna. Esto evita que futuras modificaciones rompan funcionalidades básicas, garantizando la estabilidad y consistencia del sistema a lo largo del tiempo.

---

**D3. Contrato de mensajes de error**

Este test valida que los mensajes de excepcion entregados por el sistema incluyan contexto util para facilitar la deteccion y solucion del problema.

Actualmente, la clase `Carrito` lanza excepciones con mensajes genericos que no indican cual producto o cantidad genero el error. Esto impide diagnosticar rapidamente el problema y puede aumentar el tiempo necesario para corregirlo.

El contrato deseado es que cada mensaje de error contenga informacion accionable: el nombre del producto afectado, la cantidad invalida y la razon del error.

Marcar este test como `xfail` permite identificar que el sistema no cumple este contrato actualmente y sirve como recordatorio de mejora.

Cumplir este contrato mejora la experiencia del usuario, facilita la depuracion y aumenta la calidad del codigo, reduciendo regresiones en futuras versiones.