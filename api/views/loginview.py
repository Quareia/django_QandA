# -*- coding=utf-8 -*-
from rest_framework import permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import viewsets
from api.models import Topic, Question, Answer, Message, UserInfo
from rest_framework.decorators import detail_route, list_route
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
# Create your views here.
from api.serializers.user_serializer import UserInfoSerializer


class LogoutView(APIView):

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            logout(request)  # 传递request
            return Response({'msg': '已注销'})
        return Response({'msg': '异常'})


class LoginView(APIView):

    def post(self, request):
        print(type(request.data))
        name = request.data['name']
        pwd = request.data['password']
        try:
            isregist = request.data['checkPwd']
            try:
                user = User.objects.get(username=name)
                return Response({"status": '0', 'msg': '用户名已存在'})
            except User.DoesNotExist:
                user = User.objects.create_user(username=name, password=pwd)
                user.save()

                userinfo = UserInfo.objects.create(owner=user)
                serializer = UserInfoSerializer(data=userinfo)
                login(request, user)
                authenticate(username=name, password=pwd)
                return Response({"status": '1', 'name': user.username, 'id': user.id})
        except KeyError:
            user = authenticate(username=name, password=pwd)
            if user is not None:
                if user.is_authenticated:
                    login(request, user)
                    return Response({"status": '1', 'name': user.username, 'id': user.id})
                else:
                    return Response({"status": '0', 'msg': '用户已被禁用'})
            else:
                return Response({"status": '0', 'msg': '用户名或密码错误'})