# -*- coding=utf-8 -*-
from rest_framework.routers import DefaultRouter
from api.views.userview import UserViewSet, UserInfoViewSet
from api.views.topicview import TopicViewSet
from api.views.questionview import QuestionViewSet
from api.views.answerview import AnswerViewSet
from api.views.messageview import MessageViewSet
from api.views.loginview import LogoutView, LoginView
from django.conf.urls import url, include
from api.views.answerimageview import AnswerImageViewSet

router = DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'users', UserViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)
router.register(r'topics', TopicViewSet)
router.register(r'userinfos', UserInfoViewSet)
router.register(r'answerimages', AnswerImageViewSet)

urlpatterns = [
    url(r'login/', LoginView.as_view()),
    url(r'logout/', LogoutView.as_view()),
    url(r'^', include(router.urls))
]

"""
    创建了默认的方式
        messages/
"""