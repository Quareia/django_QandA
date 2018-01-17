# -*- coding=utf-8 -*-
from rest_framework.test import APITestCase
from api.models import Question, UserInfo, Answer, Topic
from django.contrib.auth.models import User


class AnswerTests(APITestCase):
    # 测试之前执行的操作
    def setUp(self):
        user = User.objects.create_user(username='zyx', password='qwer1234')
        userinfo = UserInfo.objects.create(owner=user)
        self.client.force_login(user=user)
        self.topic = Topic.objects.create(title='123', owner=user)
        self.question = Question.objects.create(title='456', owner=user, topic=self.topic)

    def test_add(self):
        url = '/answers/'

        data = {
                'description': 'qwer1234',
                'ansto': 1
                }
        reponse = self.client.post(url, data, format='json')
        self.assertEqual(reponse.data['description'], 'qwer1234')
        self.assertEqual(Answer.objects.count(), 1)
        self.assertEqual(Answer.objects.get().description, 'qwer1234')

    def test_del(self):
        self.test_add()
        url = '/answers/1/'
        self.client.delete(url)
        self.assertEqual(Answer.objects.count(), 0)

    def test_agree(self):
        self.test_add()
        url = '/answers/1/agree_answer/'
        response = self.client.get(url)
        self.assertEqual(response.data['msg'], 'agree answer successful')

    def test_against(self):
        self.test_add()
        url = '/answers/1/against_answer/'
        response = self.client.get(url)
        self.assertEqual(response.data['msg'], 'against answer successful')
