

# LoovPay Python SDK

The LoovPay Python SDK allows you to integrate the LoovPay system into your Python applications. With this SDK, you can easily initiate and manage payments using mobile money or card payment methods. 

## Installation

You can install the LoovPay Python SDK using npm:

```bash
pip install python-loovpay
```


### `Requirements`

To use the LoovPay Python SDK, make sure you have the following required fields:

* amount: The payment amount in the specified currency.
* currency: The currency code of the payment amount.
* description: Description of the payment purpose.
* name: Customer name.
* email: Customer email.
* operator: The mobile operator code used for the payment (e.g., "orange-money-cm").
* phoneNumber: Customer phone number.
* return_url: URL to redirect after successful payment.
* cancel_url: URL to redirect if payment is canceled.
* callback_url: URL for payment notifications (webhook).
* payment_mode: The chosen payment mode. Values: ALL, CARD, MOBILE_MONEY.



## Usage

### `Pay In`

``` python
from python_loovpay import LoovPay

loov_pay = LoovPay()
loov_pay.set_keys('AppKey', 'MerchantKey')

pay_in_data = {
    'amount': 50000,
    'currency': 'XAF',
    'payment_mode': 'CARD',
    'return_url': 'https://google.com?state=return_url',
    'cancel_url': 'https://google.com?state=cancel',
    'callback_url': 'https://webhook.site/9c647add-6b43-4832-bd5d-db529c7c9b79',
    'description': 'test payment de service en ligne',
    'name': 'Arolle Fona',
    'email': 'arolle000@gmail.com',
    'phoneNumber': '237699009999'
}

response = loov_pay.pay_in(pay_in_data)
print(response)

```

#### `Success Response`

Upon successful payment initiation, the API will respond with a status code of 200 along with the following response body:

``` json
{
    "status": 200,
    "message": "Payment initiated",
    "payment_url": "https://api.secure.payment.loov-solutions.com/payinit/oa7DZzEd8gwJ5PYQ",
    "reference": "LOC8SXoZuDVEvu1ODxs"
}
```

### `Mobile SoftPay`

``` python

from python_loovpay import LoovPay

loov_pay = LoovPay()
loov_pay.set_keys('AppKey', 'MerchantKey')

mobile_pay_data = {
    'amount': 50000,
    'operator': 'XAF',
    'callback_url': 'https://webhook.site/9c647add-6b43-4832-bd5d-db529c7c9b79',
    'name': 'Arolle Fona',
    'email': 'arolle000@gmail.com',
    'phoneNumber': '237699009999'
}

response = loov_pay.mobile_soft_pay(mobile_pay_data)
print(response)

```

#### `Success Response`

Upon successfully initiating the mobile payment, the API will respond with a JSON object containing payment information.

``` json
{
    "error": false,
    "status": "success",
    "amount": "500",
    "fees": 10,
    "message": "Confirm the payment by entering your PIN code and you will receive an SMS. Thank you for using Orange Money services.",
    "reference": "LOMoac3hqZXuBHUHKy8"
}
```

### `Supported Operators`

| country | operator | operator_code | 
| ------- | -------- | ------------- |
| Benin | Mtn | mtn-benin | 
| Benin | Moov | moov-benin | 
| Cameroon | Orange | orange-money-cm | 
| Cameroon | Mtn  | mtn-cm | 
| Ivory Coast | Mtn | mtn-ci | 
| Ivory Coast | Moov | moov-ci | 
| Mali | Moov | moov-ml | 
| Mali | Orange | orange-money-ml | 
| Senegal | Orange | orange-money-senegal | 
| Senegal | Expresso | expresso-senegal |
| Senegal | Free | free-money-senegal | 
| Senegal | Wave Senegal  | wave-senegal | 
| Togo | T-money  | t-money-togo | 


### `Pay Out`

``` python

from python_loovpay import LoovPay

loov_pay = LoovPay()
loov_pay.set_keys('AppKey', 'MerchantKey')

payout_data = {
    'amount': 50000,
    'operator': 'orange-money-cm',
    'phoneNumber': '237699009999',
    'currency': 'XAF'
}

response = loov_pay.pay_out(payout_data)
print(response)


```

#### `Success Response`

Upon successfully initiating the mobile payment, the API will respond with a JSON object containing payment information.

``` json
{
    "error": false,
    "status": "success",
    "amount": "50000",
    "reference": "MOMAVzvTY7DLyiRCR38",
    "message": "Transfer of 500 XAF transferred to 237699009999"
}

```

### `Check Status`

``` python

from python_loovpay import LoovPay

loov_pay = LoovPay()
loov_pay.set_keys('AppKey', 'MerchantKey')

reference = 'MOMAVzvTY7DLyiRCR38'

response = loov_pay.check_status(reference)
print(response)


```

#### `Success Response`

Upon successfully retrieving the payment status, the API will respond with a JSON object containing the payment status information.

### `Check Status`

``` json
{
    "error": false,
    "reference": "your_reference",
    "amount": "500",
    "currency": "XAF",
    "status": "initiated",
    "date": "2023-08-08 09:08:17",
    "customer": null
}

```

### `Security Vulnerabilities`

If you discover a security vulnerability within the LoovPay Python SDK, please report it to `Leonardo Dada` via `dadaleonardo00@gmail.com`. We take security seriously and appreciate your help in disclosing any vulnerabilities responsibly.

### `License`

The LoovPay Python SDK is open-source software licensed under the MIT license. You can find the license details in the LICENSE file.

### `Credits`

This SDK was developed by `Leonardo Dada` with contributions from `Loov-Solutions`.

Special thanks to the `LoovPay` team for providing the necessary resources and support to create this Python SDK.

We hope this SDK simplifies the integration of `LoovPay Payment` into your Python applications and enables you to provide a seamless payment experience for your users. If you have any questions, issues, or suggestions, please feel free to open an issue on our GitHub repository. We appreciate your feedback and contributions to help make this SDK even better.

