from decimal import Decimal

from django.test import TestCase, Client
from rest_framework.authtoken.models import Token

from dashboard.models import User
from mvp_task.constants import BUYER_ROLE, SELLER_ROLE


class TestDeposit(TestCase):
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

    @property
    def headers(self):
        return {
            'content_type': 'application/json',
            'HTTP_AUTHORIZATION': f'Token {self.token}'
        }

    def test_valid_deposit(self):
        deposit_before = self.buyer.deposit
        amount = 5
        data = {
            "amount": amount,
        }
        resp = self.client.post('/deposit', data, **self.headers)
        self.buyer = User.objects.get(pk=self.buyer.pk)
        balance_after = self.buyer.deposit
        resp_data = resp.data
        balance = Decimal(resp_data['data']['balance'])

        self.assertTrue(resp_data['succeeded'])
        self.assertEqual(balance, balance_after)
        self.assertEqual(balance, deposit_before + amount)

    def test_invalid_amount_deposit(self):

        deposit_before = self.buyer.deposit

        data = {
            "amount": 15
        }
        resp = self.client.post('/deposit', data, **self.headers)
        self.buyer = User.objects.get(pk=self.buyer.pk)
        deposit_after = self.buyer.deposit
        resp_data = resp.data

        self.assertFalse(resp_data['succeeded'])
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(deposit_after, deposit_before)

    def test_unauthorized_access_deposit(self):
        deposit_before = self.buyer.deposit

        data = {
            "amount": 5
        }
        headers = {
            'content_type': 'application/json',
        }

        resp = self.client.post('/deposit', data, **headers)

        deposit_after = self.buyer.deposit

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(deposit_after, deposit_before)

    def test_seller_deposit(self):
        deposit_before = self.buyer.deposit

        data = {
            "amount": 5
        }
        headers = {
            'content_type': 'application/json',
            'HTTP_AUTHORIZATION': f'Token {self.seller_token}'
        }
        resp = self.client.post('/deposit', data, **headers)

        deposit_after = self.buyer.deposit

        self.assertEqual(resp.status_code, 403)
        self.assertEqual(deposit_after, deposit_before)
