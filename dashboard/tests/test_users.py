from django.test import TestCase, Client
from rest_framework.authtoken.models import Token

from dashboard.models import User
from mvp_task.constants import SELLER_ROLE, BUYER_ROLE


class TestUser(TestCase):
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

    def test_create_buyer(self):
        buyer_data = {
            "username": "buyer",
            "password": "allow.me",
            "role": BUYER_ROLE
        }
        resp = self.client.post('/user', buyer_data)
        resp_data = resp.data
        self.assertTrue(resp_data['succeeded'])
        self.assertTrue(resp.status_code, 200)

    def test_create_seller(self):
        seller_data = {
            "username": "seller",
            "password": "allow.me",
            "role": SELLER_ROLE
        }
        resp = self.client.post('/user', seller_data)
        resp_data = resp.data
        self.assertTrue(resp_data['succeeded'])
        self.assertTrue(resp.status_code, 200)

    def test_get_user(self):
        user, _ = User.objects.get_or_create(username='buyer', defaults={
            "deposit": 5, "role": BUYER_ROLE
        })
        token, _ = Token.objects.get_or_create(user=user)
        resp = self.client.get(
            '/user', HTTP_AUTHORIZATION=f'Token {token.key}'
        )
        resp_data = resp.data
        self.assertTrue(resp_data['succeeded'])
        self.assertTrue(resp.status_code, 200)
        self.assertTrue(resp_data['data']['username'], user.username)
        self.assertTrue(resp_data['data']['deposit'], user.deposit)

    def test_update_user(self):
        user, _ = User.objects.get_or_create(username='buyer', defaults={
            "deposit": 5, "role": BUYER_ROLE
        })
        token, _ = Token.objects.get_or_create(user=user)
        resp = self.client.put(
            '/user',
            {"username": "buyer_mod", "role": BUYER_ROLE},
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Token {token.key}'
        )
        resp_data = resp.data
        print(resp_data)
        self.assertTrue(resp_data['succeeded'])
        self.assertTrue(resp.status_code, 200)
        self.assertTrue(User.objects.filter(username='buyer_mod').exists())

    def test_delete_user(self):
        user, _ = User.objects.get_or_create(username='buyer', defaults={
            "deposit": 5, "role": BUYER_ROLE
        })
        token, _ = Token.objects.get_or_create(user=user)
        resp = self.client.delete(
            '/user', HTTP_AUTHORIZATION=f'Token {token.key}'
        )
        resp_data = resp.data
        self.assertTrue(resp_data['succeeded'])
        self.assertTrue(resp.status_code, 200)
        self.assertFalse(User.objects.filter(username='buyer').exists())
