# -*- coding=utf-8 -*-
from rest_framework.test import APITestCase
from api.models import Topic, UserInfo, Message
from django.contrib.auth.models import User


class MessageTests(APITestCase):
    # 测试之前执行的操作
    def setUp(self):
        user = User.objects.create_user(username='zyx', password='qwer1234')
        user2 = User.objects.create_user(username='xudong', password='qwer1234')
        userinfo = UserInfo.objects.create(owner=user)
        self.client.force_login(user=user)

    def test_add(self):
        url = '/messages/'
        data = {'origin': 2,
                'destination': 1,
                'content': 'aaa',
                'type': 0
                }
        reponse = self.client.post(url, data, format='json')
        self.assertEqual(reponse.data['content'], 'aaa')
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.get().content, 'aaa')

    def test_del(self):
        self.test_add()
        url = '/messages/1/'
        self.client.delete(url)
        self.assertEqual(Topic.objects.count(), 0)

    def test_my_receive(self):
        self.test_add()
        url = '/messages/my_receive_messages/'
        response = self.client.get(url)
        self.assertEqual(response.data['results'][0]['content'], 'aaa')

    def test_my_send(self):
        self.test_add()
        url = '/messages/my_send_messages/'
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 0)
