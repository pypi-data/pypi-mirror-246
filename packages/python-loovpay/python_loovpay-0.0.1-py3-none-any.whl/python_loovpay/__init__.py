
"""LoovPay

LoovPay Python client library.
Modules implemented: LoovPay
"""

# __version__ = '0.0.1'
# __author__ = "LOOV-SOLUTIONS <dadaleonardo00@gmail.com>"


# import sys

# moved here so the modules that depend on the 'Payment' class will work
from .src.python_loovpay import LoovPay


__all__ = [
    LoovPay.__name__,
]