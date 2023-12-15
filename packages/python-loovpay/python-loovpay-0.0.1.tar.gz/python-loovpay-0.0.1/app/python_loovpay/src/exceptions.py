
class LoovPayException(Exception):
    """Base exception class for LoovPay SDK."""

class AmountTooSmallError(LoovPayException):
    """Raised when the payment amount is less than the minimum required."""

class MissingFieldError(LoovPayException):
    """Raised when a required field is missing in the payment data."""

class InvalidPaymentModeError(LoovPayException):
    """Raised when an invalid payment mode is provided."""
