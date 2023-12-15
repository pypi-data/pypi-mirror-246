
from checkout_page_sdk.signature_handler import SignatureHandler
from checkout_page_sdk.checkout_page import CheckoutPage
from checkout_page_sdk.callback import Callback
from checkout_page_sdk.payment import Payment


class Gate(object):
    """Class Gate

    Attributes:
        CURRENCY_USD - Currency USD
        CURRENCY_EUR - Currency EUR

        __checkoutPageUrlBuilder - Builder for Checkout page
        __signatureHandler - Signature Handler (check, sign)
    """
    CURRENCY_USD = 'USD'
    CURRENCY_EUR = 'EUR'

    __checkoutPageUrlBuilder = None
    __signatureHandler = None

    def __init__(self, secret: str, base_url: str = ''):
        """
        Gate constructor

        :param str secret: Secret key
        """
        self.__signatureHandler = SignatureHandler(secret)
        self.__checkoutPageUrlBuilder = CheckoutPage(self.__signatureHandler, base_url)

    def get_purchase_checkout_page_url(self, payment: Payment) -> str:
        """
        Get URL for purchase checkout page

        :param Payment payment:
        :return:
        """
        return self.__checkoutPageUrlBuilder.get_url(payment)

    def handle_callback(self, data):
        """
        Callback handler

        :param data:
        :return:
        """
        return Callback(data, self.__signatureHandler)
