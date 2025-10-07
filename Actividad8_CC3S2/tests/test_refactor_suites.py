import pytest
from unittest.mock import Mock
from src.shopping_cart import ShoppingCart


class TestPrecisionMonetaria:
    def test_suma_pequenas_cantidades(self):
        # Arrange
        cart = ShoppingCart()
        cart.add_item("x", 1, 0.05)
        cart.add_item("x", 1, 0.05)

        # Act
        total = cart.calculate_total()

        # Assert
        assert round(total, 2) == 0.10, f"Total esperado 0.10, obtenido {total}"


class TestPasarelaPagoContratos:
    def test_pago_exitoso(self):
        # Arrange
        mock_gateway = Mock()
        mock_gateway.process_payment.return_value = True

        cart = ShoppingCart(payment_gateway=mock_gateway)
        cart.add_item("x", 1, 10.0)

        # Act
        resultado = cart.process_payment(cart.calculate_total())

        # Assert
        assert resultado is True
        mock_gateway.process_payment.assert_called_once_with(10.0)

    def test_pago_falla(self):
        # Arrange
        mock_gateway = Mock()
        mock_gateway.process_payment.return_value = False

        cart = ShoppingCart(payment_gateway=mock_gateway)
        cart.add_item("x", 1, 20.0)

        # Act
        resultado = cart.process_payment(cart.calculate_total())

        # Assert
        assert resultado is False
        mock_gateway.process_payment.assert_called_once()
