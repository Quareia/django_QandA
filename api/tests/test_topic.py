# -*- coding=utf-8 -*-
from rest_framework.test import APITestCase
from api.models import Topic, UserInfo
from django.contrib.auth.models import User


class TopicTests(APITestCase):
    # 测试之前执行的操作
    def setUp(self):
        user = User.objects.create_user(username='zyx', password='qwer1234')
        userinfo = UserInfo.objects.create(owner=user)
        self.client.force_login(user=user)

    def test_add(self):
        url = '/topics/'
        data = {'title': 'shepi',
                'description': 'qwer1234'
                }
        reponse = self.client.post(url, data, format='json')
        self.assertEqual(reponse.data['title'], 'shepi')
        self.assertEqual(Topic.objects.count(), 1)
        self.assertEqual(Topic.objects.get().title, 'shepi')

    def test_del(self):
        self.test_add()
        url = '/topics/1/'
        self.client.delete(url)
        self.assertEqual(Topic.objects.count(), 0)

    def test_search(self):
        self.test_add()
        url = '/topics/search/'
        data = {'title': 's'}
        response = self.client.get(url, data)
        self.assertEqual(response.data['results'][0]['title'], 'shepi')

    def test_follow(self):
        self.test_add()
        url = '/topics/1/follow_topic/'
        response = self.client.get(url)
        self.assertEqual(response.data['msg'], '关注成功')

    def test_cancel_follow(self):
        self.test_follow()
        url = '/topics/1/cancel_follow/'
        response = self.client.get(url)
        self.assertEqual(response.data['msg'], '取消关注成功')
