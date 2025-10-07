import pytest
from src.shopping_cart import ShoppingCart
from src.carrito import Carrito, Producto

def test_mre_precision_binaria_simple():
    """MRE: Problema de precision binaria en suma de precios decimales"""
    carrito = ShoppingCart()
    carrito.add_item("producto_a", 1, 0.1)
    carrito.add_item("producto_b", 1, 0.2)
    total_crudo = carrito.calculate_total()
    # Expectativa: 0.3 exacto
    # Realidad: 0.30000000000000004 por representacion binaria
    assert abs(total_crudo - 0.3) < 1e-9 or round(total_crudo, 2) == 0.30

def test_mre_precision_acumulada():
    """MRE: Error de precision acumulada en multiples adiciones"""
    carrito = ShoppingCart()
    for i in range(5):
        carrito.add_item(f"item_{i}", 1, 0.2)
    # Expectativa: 5 * 0.2 = 1.0
    # Realidad: error minimo acumulado
    assert round(carrito.calculate_total(), 2) == 1.00

def test_mre_precio_cero():
    """MRE: Manejo de precio cero en Carrito"""
    carrito = Carrito()
    producto = Producto("gratis", 0.0)
    carrito.agregar_producto(producto, 2)
    assert carrito.calcular_total() == 0.0

def test_mre_consistencia_carrito_shoppingcart():
    """MRE: Comparar precision entre Carrito y ShoppingCart"""
    carrito_clase = Carrito()
    carrito_clase.agregar_producto(Producto("x", 0.1), 5)

    carrito_funcional = ShoppingCart()
    carrito_funcional.add_item("x", 5, 0.1)

    assert round(carrito_clase.calcular_total(), 2) == round(carrito_funcional.calculate_total(), 2)