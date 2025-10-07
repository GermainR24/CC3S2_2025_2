import random
from faker import Faker
from src.factories import ProductoFactory
from src.carrito import Carrito, ItemCarrito
import pytest

@pytest.mark.stability
def test_estabilidad_semillas(capsys):
    # 1- corrida
    random.seed(123)
    faker = Faker()
    faker.seed_instance(123)
    p = ProductoFactory()
    c = Carrito()
    c.agregar_producto(p, 2)
    total1 = c.calcular_total()
    print(total1)
    out1 = capsys.readouterr().out.strip()

    # 2- corrida (reutilizar mismo producto)
    random.seed(123)
    faker.seed_instance(123)
    p2 = p  # reutilizamos exactamente el mismo producto
    c2 = Carrito()
    c2.agregar_producto(p2, 2)
    total2 = c2.calcular_total()
    print(total2)
    out2 = capsys.readouterr().out.strip()

    assert out1 == out2, f"Totales diferentes: {out1} vs {out2}"
