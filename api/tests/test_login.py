from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class LoginTests(APITestCase):
    def test_regist(self):
        url = '/login/'
        data = {'name': 'shepi',
                'password': 'qwer1234',
                'checkPwd': 'qwer1234'}
        reponse = self.client.post(url, data, format='json')
        self.assertEqual(reponse.data, {"status": '1', 'name': 'shepi', 'id': 1})
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'shepi')

    def test_login(self):
        self.test_regist()
        url = '/login/'
        data = {'name':'shepi',
                'password': 'qwer1234'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data, {"status": '1', 'name': 'shepi', 'id': 1})
