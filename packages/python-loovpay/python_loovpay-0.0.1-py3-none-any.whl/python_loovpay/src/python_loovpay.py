import json
from .exceptions import AmountTooSmallError, MissingFieldError, InvalidPaymentModeError
import sys
import requests

API_VERSION = 'v1'

SERVER = "api.secure.payment.loov-solutions.com"

# Live Endpoint
LIVE_ENDPOINT = "https://%s/%s" % (SERVER, API_VERSION)

# fixme: find a better way of 'self' referencing
__MODULE__ = sys.modules[__name__]

class LoovPay:
    def __init__(self):
        self.url = LIVE_ENDPOINT
        self.headers = {}
        self.app_key = None
        self.merchant_key = None

    def set_keys(self, app_key, merchant_key):
        self.headers = {
            'Accept': 'application/json',
            'content-type': 'application/json',
            'app-key': app_key,
            'merchant-key': merchant_key
        }
        return self

    def pay_in(self, data):

        for key in ['amount', 'name', 'email', 'phoneNumber', 'callback_url', 'cancel_url', 'return_url']:
            if key not in data:
                raise MissingFieldError(f'{key} is not defined')

        body = {
            'amount': data['amount'],
            'currency': data['currency'],
            'payment_mode': data['payment_mode'],
            'callback_url': data['callback_url'],
            'return_url': data['return_url'],
            'cancel_url': data['cancel_url'],
            'description': data['description'],
            'customer': {
                'name': data['name'],
                'email': data['email'],
                'phoneNumber': data['phoneNumber']
            }
        }


        response = requests.post(f'{self.url}/payment/init', json=body, headers=self.headers)
        return json.loads(response.text)

    def mobile_soft_pay(self, data):
        body = {
            'amount': data['amount'],
            'operator': data['operator'],
            'phoneNumber': data['phoneNumber'],
            'customer': {
                'name': data['name'],
                'email': data['email'],
                'phoneNumber': '237' + data['phoneNumber']
            },
            'callback_url': data['callback_url']
        }

        for key in ['amount', 'name', 'operator', 'email', 'phoneNumber', 'callback_url']:
            if key not in data:
                raise MissingFieldError(f'{key} is not defined, hence missing field')
                # raise Exception(f'{key} is not defined')

        if data['amount'] <= 500:
            raise AmountTooSmallError('Amount must be greater than or equal to 500')
            # raise Exception('Amount must be greater than 100')

        response = requests.post(f'{self.url}/payment/payin/mobile', json=body, headers=self.headers)
        return json.loads(response.text)

    def pay_out(self, data):
        body = {
            'amount': data['amount'],
            'operator': data['operator'],
            'phoneNumber': '237' + data['phoneNumber'],
            'currency': data['currency']
        }

        response = requests.post(f'{self.url}/payment/payout/mobile', json=body, headers=self.headers)
        return json.loads(response.text)

    def check_status(self, reference):
        if not reference:
            raise MissingFieldError(f'reference is not defined, hence missing field')
        response = requests.get(f'{self.url}/payment/status/{reference}', headers=self.headers)
        return json.loads(response.text)

# Example usage:
# loov_pay = LoovPay()
# loov_pay.set_keys('your_app_key', 'your_merchant_key')

# pay_in_data = {
#     'amount': 200,
#     'currency': 'USD',
#     'payment_mode': 'credit_card',
#     'callback_url': 'https://example.com/callback',
#     'return_url': 'https://example.com/return',
#     'cancel_url': 'https://example.com/cancel',
#     'description': 'Payment for Order #123',
#     'name': 'John Doe',
#     'email': 'johndoe@example.com',
#     'phoneNumber': '1234567890'
# }

# result = loov_pay.pay_in(pay_in_data)
# print(result)
