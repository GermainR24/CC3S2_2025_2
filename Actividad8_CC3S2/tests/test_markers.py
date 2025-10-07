import pytest
from src.carrito import Carrito, Producto

@pytest.mark.smoke
def test_smoke_agregar_y_total():
    c = Carrito()
    c.agregar_producto(Producto("x", 1.0), 1)
    assert c.calcular_total() == 1.0

@pytest.mark.smoke
def test_smoke_descuento_basico():
    c = Carrito()
    c.agregar_producto(Producto("y", 100.0), 1)
    assert round(c.aplicar_descuento(10), 2) == 90.00

@pytest.mark.smoke
def test_smoke_vacio_no_falla():
    c = Carrito()
    assert c.calcular_total() == 0.0

@pytest.mark.regression
def test_regression_descuento_redondeo():
    c = Carrito()
    c.agregar_producto(Producto("x", 10.0), 1)
    assert round(c.aplicar_descuento(15), 2) == 8.50

@pytest.mark.regression
def test_regression_multiples_items_y_descuentos():
    c = Carrito()
    c.agregar_producto(Producto("a", 2.33), 3)
    c.agregar_producto(Producto("b", 1.20), 2)
    total_con_descuento = c.aplicar_descuento(10)  # 10% de descuento
    esperado = round((2.33*3 + 1.20*2) * 0.9, 2)
    assert round(total_con_descuento, 2) == esperado
