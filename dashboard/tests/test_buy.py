from django.test import TestCase, Client
from rest_framework.authtoken.models import Token

from dashboard.models import User, Product
from mvp_task import errors
from mvp_task.constants import BUYER_ROLE, SELLER_ROLE


class TestBuy(TestCase):
    buyer_data = {
        "username": "buyer",
        "password": "allow.me",
    }
    seller_data = {
        "username": "seller",
        "password": "allow.me",
    }

    def setUp(self):
        self.client = Client()
        user = User(username='buyer', role=BUYER_ROLE, deposit=10)
        user.set_password('allow.me')
        user.save()
        self.buyer = user

        user = User(username='seller', role=SELLER_ROLE, deposit=0)
        user.set_password('allow.me')
        user.save()
        self.seller = user

        token = Token(user=self.buyer)
        token.save()
        self.token = token.key

        seller_token = Token(user=self.seller)
        seller_token.save()
        self.seller_token = seller_token.key

        product = Product(productName='Test product', amountAvailable=5,
                          cost=5, seller=self.seller)
        product.save()
        self.product = product

        product2 = Product(productName='Unavailable product',
                           amountAvailable=0, cost=5, seller=self.seller)
        product2.save()
        self.bad_product = product2

    # def get_header(self):
    #     return {
    #         'Content-Type': 'application/json',
    #         'Authorization': f'Token {self.token}'
    #     }
    #
    # def register_buyer(self):
    #     resp = self.client.post('/user', self.buyer_data)
    #     return resp.data
    #
    # def register_seller(self):
    #     resp = self.client.post('/user', self.seller_data)
    #     return resp.data
    #
    # def login_buyer(self):
    #     resp = self.client.post('/login', self.buyer_data)
    #     return resp.data
    #
    # def login_seller(self):
    #     resp = self.client.post('/login', self.seller_data)
    #     return resp.data
    #
    # def deposit(self):
    #     data = {"amount": "100"}
    #     resp = self.client.post('/deposit', data, headers=self.get_header())
    #     return resp.data

    @property
    def headers(self):
        return {
            'content_type': 'application/json',
            'HTTP_AUTHORIZATION': f'Token {self.token}'
        }

    # def buy(self):
    #     seller_register_response = self.register_seller()
    #     buyer_register_response = self.register_buyer()
    #     if register_response['succeeded']:
    #         login_response = self.login()
    #         print(login_response)
    #         if login_response['succeeded']:
    #             self.token = login_response["data"]["token"]
    #             data = {
    #                 "productId": 1,
    #                 "quantity": 1
    #             }
    #             resp = self.client.post(
    #                 '/buy', data, headers=self.get_header()
    #             )
    #             print(resp.data)
    #         self.assertTrue(login_response['succeeded'])
    #     self.assertTrue(register_response['succeeded'])

    def test_valid_buy(self):
        qty_before = self.product.amountAvailable
        deposit_before = self.buyer.deposit
        qty = 1
        data = {
            "productId": self.product.pk,
            "quantity": qty
        }
        resp = self.client.post('/buy', data, **self.headers)
        self.buyer = User.objects.get(pk=self.buyer.pk)
        self.product = Product.objects.get(pk=self.product.pk)
        qty_after = self.product.amountAvailable
        deposit_after = self.buyer.deposit
        resp_data = resp.data

        total = self.product.get_total_for_qty(qty)
        self.assertTrue(resp_data['succeeded'])
        self.assertEqual(
            resp_data['data']['total'],
            self.product.get_total_for_qty(qty)
        )
        self.assertEqual(
            resp_data['data']['change'],
            self.buyer.deposit_breakdown
        )
        self.assertEqual(resp_data['data']['product']['id'], self.product.id)
        self.assertEqual(qty_after, qty_before - qty)
        self.assertEqual(deposit_after, deposit_before - total)
        self.assertEqual(resp.status_code, 200)

    def test_insuff_bal_buy(self):
        qty_before = self.product.amountAvailable
        deposit_before = self.buyer.deposit

        data = {
            "productId": self.product.pk,
            "quantity": 5
        }
        resp = self.client.post('/buy', data, **self.headers)
        self.buyer = User.objects.get(pk=self.buyer.pk)
        self.product = Product.objects.get(pk=self.product.pk)
        qty_after = self.product.amountAvailable
        deposit_after = self.buyer.deposit
        resp_data = resp.data

        self.assertFalse(resp_data['succeeded'])
        self.assertEqual(
            str(resp_data['data']['non_field_errors'][0]),
            errors.QTY_EXCEEDED_ERROR
        )
        self.assertEqual(qty_after, qty_before)
        self.assertEqual(deposit_after, deposit_before)
        self.assertEqual(resp.status_code, 400)

    def test_invalid_product_buy(self):
        qty_before = self.product.amountAvailable
        deposit_before = self.buyer.deposit
        data = {
            "productId": 11,
            "quantity": 3
        }

        resp = self.client.post('/buy', data, **self.headers)

        self.buyer = User.objects.get(pk=self.buyer.pk)
        self.product = Product.objects.get(pk=self.product.pk)
        qty_after = self.product.amountAvailable
        deposit_after = self.buyer.deposit
        resp_data = resp.data

        self.assertFalse(resp_data['succeeded'])
        self.assertEqual(
            str(resp_data['data']['non_field_errors'][0]),
            errors.INVALID_PRODUCT_ID_ERROR
        )
        self.assertEqual(qty_after, qty_before)
        self.assertEqual(deposit_after, deposit_before)
        self.assertEqual(resp.status_code, 400)

    def test_qty_exceeded_buy(self):

        qty_before = self.bad_product.amountAvailable
        deposit_before = self.buyer.deposit

        data = {
            "productId": self.bad_product.pk,
            "quantity": 3
        }
        resp = self.client.post('/buy', data, **self.headers)
        self.buyer = User.objects.get(pk=self.buyer.pk)
        self.bad_product = Product.objects.get(pk=self.bad_product.pk)
        qty_after = self.bad_product.amountAvailable
        deposit_after = self.buyer.deposit
        resp_data = resp.data

        self.assertFalse(resp_data['succeeded'])
        self.assertEqual(
            str(resp_data['data']['non_field_errors'][0]),
            errors.QTY_EXCEEDED_ERROR
        )
        self.assertEqual(qty_after, qty_before)
        self.assertEqual(deposit_after, deposit_before)
        self.assertEqual(resp.status_code, 400)

    def test_unauthorized_access_buy(self):
        qty_before = self.product.amountAvailable
        deposit_before = self.buyer.deposit

        data = {
            "productId": self.product.pk,
            "quantity": 3
        }
        headers = {
            'content_type': 'application/json',
        }

        resp = self.client.post('/buy', data, **headers)

        self.product = Product.objects.get(pk=self.product.pk)
        qty_after = self.product.amountAvailable
        deposit_after = self.buyer.deposit

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(qty_after, qty_before)
        self.assertEqual(deposit_after, deposit_before)

    def test_seller_buy(self):
        qty_before = self.product.amountAvailable
        deposit_before = self.buyer.deposit

        data = {
            "productId": self.product.pk,
            "quantity": 3
        }
        headers = {
            'content_type': 'application/json',
            'HTTP_AUTHORIZATION': f'Token {self.seller_token}'
        }
        resp = self.client.post('/buy', data, **headers)

        self.product = Product.objects.get(pk=self.product.pk)
        qty_after = self.product.amountAvailable
        deposit_after = self.buyer.deposit

        self.assertEqual(resp.status_code, 403)
        self.assertEqual(qty_after, qty_before)
        self.assertEqual(deposit_after, deposit_before)
