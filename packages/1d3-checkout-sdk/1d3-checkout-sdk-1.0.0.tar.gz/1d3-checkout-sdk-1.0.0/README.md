# 1D3 checkout page SDK

This is a set of libraries in the Python language to ease integration of your service
with the 1D3 Checkout Page.

Please note that for correct SDK operating you must have at least Python 3.5.  

## Payment flow

![Payment flow](flow.png)

## Installation

Install with pip
```bash
pip install 1d3-sdk
```

### Get URL for payment

```python
from checkout_page_sdk.gate import Gate
from checkout_page_sdk.payment import Payment

gate = Gate('secret')
payment = Payment('402')
payment.payment_id = 'some payment id'
payment.payment_amount = 1001
payment.payment_currency = 'USD'
payment_url = gate.get_purchase_checkout_page_url(payment)
``` 

`payment_url` here is the signed URL.

### Handle callback from 1D3

You'll need to autoload this code in order to handle notifications:

```python
from checkout_page_sdk.gate import Gate

gate = Gate('secret')
callback = gate.handle_callback(data)
```

`data` is the JSON data received from payment system;

`callback` is the Callback object describing properties received from payment system;
`callback` implements these methods: 
1. `callback.get_payment_status()`
    Get payment status.
2. `callback.get_payment()`
    Get all payment data.
3. `callback.get_payment_id()`
    Get payment ID in your system.
