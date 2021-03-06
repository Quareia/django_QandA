# -*- coding=utf-8 -*-
from rest_framework import permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import viewsets
from api.models import UserInfo
from rest_framework.decorators import detail_route, list_route

from api.serializers.question_serializer import QuestionSerializer, ReturnQuestionSerializer
from api.serializers.topic_serializer import TopicSerializer
from api.serializers.user_serializer import UserSerializer, UserInfoSerializer, SimUserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
        提供展示用户信息列表
        以及展示用户详细信息，通过id查找
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )

    @detail_route()
    def my_info(self, request, pk=None):
        try:
            info = UserInfo.objects.get(pk=request.user.info.id)
        except UserInfo.DoesNotExist:
            return Response({'msg': '用户信息不存在'})
        serializer = UserInfoSerializer(info)
        return Response(serializer.data)

    @list_route()
    def get_sel_user(self, request):
        users = User.objects.all()
        serializer = SimUserSerializer(users, many=True)
        return Response(serializer.data)


class UserInfoViewSet(viewsets.ModelViewSet):
    """
        保存用户的一些信息，例如关注话题，关注问题等
    """
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @detail_route()
    def my_follow_topics(self, request, pk=None):
        try:
            info = UserInfo.objects.get(pk=pk)
        except UserInfo.DoesNotExist:
            return Response({'msg': 'user info does not exist'})
        topics = info.followtopics.all()
        page = self.paginate_queryset(topics)
        if page is not None:
            serializer = TopicSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)

    @detail_route()
    def my_follow_questions(self, request, pk=None):
        try:
            info = UserInfo.objects.get(pk=pk)
        except UserInfo.DoesNotExist:
            return Response({'msg': 'user info does not exist'})
        questions = info.followquestions.all()
        page = self.paginate_queryset(questions)
        if page is not None:
            serializer = ReturnQuestionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ReturnQuestionSerializer(questions, many=True)
        return Response(serializer.data)
