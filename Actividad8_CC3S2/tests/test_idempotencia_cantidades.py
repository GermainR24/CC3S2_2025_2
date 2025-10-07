from src.carrito import Carrito, Producto

def test_actualizacion_idempotente():
    # Arrange
    c = Carrito()
    p = Producto("x", 3.25)
    c.agregar_producto(p, 2)
    total1 = c.calcular_total()

    # Act
    for _ in range(5):
        c.actualizar_cantidad(p, 2)  

    total2 = c.calcular_total()

    # Assert
    assert total1 == total2
    assert sum(i.cantidad for i in c.items) == 2
