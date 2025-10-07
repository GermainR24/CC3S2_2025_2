# tests/test_invariantes_inventario.py
from src.carrito import Carrito, Producto

def test_invariante_agregar_remover_y_actualizar():
    # Arrange
    c = Carrito()
    producto = Producto("x", 5.0)

    # Agregar N
    c.agregar_producto(producto, 3)  # N = 3
    total_inicial = c.calcular_total()

    # Act: remover N
    c.remover_producto(producto, 3)

    # Agregar N otra vez
    c.agregar_producto(producto, 3)

    # Actualizar cantidad a 0
    c.actualizar_cantidad(producto, 0)

    # Assert: invariantes
    assert c.calcular_total() == 0.0, "Total debe ser 0 después de agregar/remover y actualizar"
    assert sum(item.cantidad for item in c.items) == 0, "Cantidad total debe ser 0"
    assert total_inicial == 15.0, "Total inicial debe ser consistente (3 * 5.0 = 15.0)"
