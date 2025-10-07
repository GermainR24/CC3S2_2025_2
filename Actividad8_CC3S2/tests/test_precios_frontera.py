import pytest
from src.carrito import Carrito, Producto

@pytest.mark.parametrize("precio", [0.01, 0.005, 0.0049, 9999999.99])
def test_precios_frontera(precio):
    # Arrange
    c = Carrito()
    p = Producto("p", precio)
    # Act
    c.agregar_producto(p, 1)
    total = c.calcular_total()
    # Assert
    assert total >= 0  


@pytest.mark.xfail(reason="Contrato no definido para precio=0 o negativo")
@pytest.mark.parametrize("precio_invalido", [0.0, -1.0])
def test_precios_invalidos(precio_invalido):
    c = Carrito()
    p = Producto("p", precio_invalido)
    c.agregar_producto(p, 1)
