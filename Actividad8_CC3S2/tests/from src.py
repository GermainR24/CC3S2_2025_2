from src.carrito import Carrito, Producto

def test_redondeo_acumulado_vs_final():
    # Arrange
    c = Carrito()
    c.agregar_producto(Producto("a", 0.3333), 3)
    c.agregar_producto(Producto("b", 0.6667), 3)
    # Act
    total = c.calcular_total()
    suma_por_item = sum(i.producto.precio * i.cantidad for i in c.items)
    # Assert
    assert round(total, 2) == round(suma_por_item, 2)


@pytest.mark.parametrize("precio1, precio2", [(0.335, 0.665), (0.334, 0.666)])
def test_redondeo_acumulado_vs_final(precio1, precio2):
    c = Carrito()
    c.agregar_producto(Producto("a", precio1), 3)
    c.agregar_producto(Producto("b", precio2), 3)
    total = c.calcular_total()
    suma_por_item = sum(i.producto.precio * i.cantidad for i in c.items)

    assert round(tatal, 2) == round(suma_por_item, 2)