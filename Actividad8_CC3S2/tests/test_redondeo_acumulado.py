from src.carrito import Carrito, Producto

def test_redondeo_acumulado_vs_final():
    # Arrange
    c = Carrito()
    c.agregar_producto(Producto("a", 0.3333), 3)
    c.agregar_producto(Producto("b", 0.6667), 3)

    # Act
    # Redondear por item(acumulado)
    suma_por_item = sum(round(item.producto.precio * item.cantidad, 2) for item in c.items)
    # Redonde al final
    total_final = round(sum(item.producto.precio * item.cantidad for item in c.items), 2)

    # Assert
    assert round(suma_por_item, 2) == round(total_final, 2)




def test_redondeo_acumulado_vs_final_difiere():
    # Arrange
    c = Carrito()
    c.agregar_producto(Producto("a", 0.335), 3)  # subtotal = 1.005 → round = 1.01
    c.agregar_producto(Producto("b", 0.665), 3)  # subtotal = 1.995 → round = 2.00

    # Act
    suma_por_item = sum(round(item.producto.precio * item.cantidad, 2) for item in c.items)
    total_final = round(sum(item.producto.precio * item.cantidad for item in c.items), 2)

    # Asser
    assert suma_por_item != total_final, (
        f"No se detecto alguna diferencia: suma_por_item={suma_por_item}, total_final={total_final}"
    )
