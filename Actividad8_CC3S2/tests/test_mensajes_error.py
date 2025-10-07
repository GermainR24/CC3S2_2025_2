import pytest
from src.carrito import Carrito

@pytest.mark.xfail(reason="Esperamos mensaje con pista accionable")
def test_mensaje_error_contiene_contexto():
    c = Carrito()
    with pytest.raises(ValueError) as e:
        c.actualizar_cantidad("inexistente", 1)
    assert "inexistente" in str(e.value)

@pytest.mark.xfail(reason="Esperamos mensaje con cantidad inválida")
def test_mensaje_error_cantidad_negativa():
    c = Carrito()
    from src.carrito import Producto
    p = Producto("x", 10.0)
    c.agregar_producto(p, 1)
    with pytest.raises(ValueError) as e:
        c.actualizar_cantidad("x", -5)
    assert "cantidad negativa" in str(e.value).lower()
