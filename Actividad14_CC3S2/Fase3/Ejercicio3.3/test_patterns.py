"""
Tests automatizados para patrones de infraestructura
"""

import pytest
from singleton import ConfigSingleton
from factory import NullResourceFactory
from prototype import ResourcePrototype


def test_singleton_meta():
    """
    Verifica que ConfigSingleton siempre devuelva la misma instancia en memoria.
    """
    a = ConfigSingleton("Produccion")
    b = ConfigSingleton("Desarrollo")
    assert a is b, "Error: Singleton generó dos instancias diferentes."

    assert b.env_name == "Produccion"

def test_factory_structure():
    """
    Verifica que la Factory genere la estructura JSON correcta con triggers.
    """
    name = "test_app"
    block = NullResourceFactory.create(name)

    try:
        res_list = block["resource"][0]["null_resource"]
        res_dict = res_list[0]
        triggers = res_dict[name][0]["triggers"]
        assert "factory_uuid" in triggers
        assert "timestamp" in triggers
    except (KeyError, IndexError):
        pytest.fail("La Factory no generó la estructura anidada esperada.")

def test_prototype_clone_independent():
    """
    Verifica que modificar un clon no afecte a otro clon ni al original.
    """
    base_dict = NullResourceFactory.create("app")
    proto = ResourcePrototype(base_dict)

    c1 = proto.clone(lambda d: d.__setitem__("f1", 1))

    c2 = proto.clone(lambda d: d.__setitem__("b1", 2))


    assert "f1" in c1.data
    assert "f1" not in c2.data

    assert "b1" in c2.data
    assert "b1" not in c1.data

    assert "f1" not in proto.data
    assert "b1" not in proto.data