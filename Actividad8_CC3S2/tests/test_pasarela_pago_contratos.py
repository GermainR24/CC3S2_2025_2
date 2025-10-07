import pytest
from unittest.mock import Mock
from src.shopping_cart import ShoppingCart


def test_pago_exitoso():
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


def test_pago_timeout_sin_reintento_automatico():
    # Arrange
    mock_gateway = Mock()
    mock_gateway.process_payment.side_effect = TimeoutError("timeout")

    cart = ShoppingCart(payment_gateway=mock_gateway)
    cart.add_item("x", 1, 10.0)

    # Act / Assert
    with pytest.raises(TimeoutError):
        cart.process_payment(cart.calculate_total())

    # Verificamos que el SUT no haya reintentado automaticamente
    assert mock_gateway.process_payment.call_count == 1

    # Reintento manual (simulado por el test)
    mock_gateway.process_payment.side_effect = None
    mock_gateway.process_payment.return_value = True
    assert mock_gateway.process_payment(10.0) is True  # contrato documentado


def test_pago_rechazo_definitivo():
    # Arrange
    mock_gateway = Mock()
    mock_gateway.process_payment.return_value = False

    cart = ShoppingCart(payment_gateway=mock_gateway)
    cart.add_item("x", 1, 10.0)

    # Act
    resultado = cart.process_payment(cart.calculate_total())

    # Assert
    assert resultado is False
    mock_gateway.process_payment.assert_called_once_with(10.0)
