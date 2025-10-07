import pytest
from src.carrito import Carrito, Producto

@pytest.mark.xfail(reason="Float binario puede introducir error en dinero")
def test_total_precision_decimal():
    # Arrange
    c = Carrito()
    c.agregar_producto(Producto("x", 0.1), 1)
    c.agregar_producto(Producto("y", 0.2), 1)

    # Act
    total = c.calcular_total()

    # Assert
    # Esperamos que 0.1 + 0.2 == 0.3, pero en binario float da 0.30000000000000004
    assert total == 0.3
