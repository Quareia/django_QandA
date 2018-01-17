# -*- coding=utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import Topic, Question, Answer, Message, UserInfo, AnswerImage


class UserSerializer(serializers.ModelSerializer):
    # 提出的问题: 保存提出的问题的主键id
    questions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # 提出的话题: 保存提出的话题的主键name
    topics = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # 做出的回答
    answers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # 暂时只保存对应user的主键，
    info = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'topics', 'questions',
                  'answers', 'info')


class UserInfoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    followquestions = serializers.PrimaryKeyRelatedField(many=True,
                                                         queryset=Question.objects.all())
    followtopics = serializers.PrimaryKeyRelatedField(many=True,
                                                      queryset=Topic.objects.all())
    userimg = serializers.ImageField(allow_empty_file=True, required=False)
    # 返回/media的路径
    userimg_url = serializers.SerializerMethodField()

    def get_userimg_url(self, obj):
        if obj.userimg:
            return obj.userimg.url
        else:
            return None

    class Meta:
        model = UserInfo
        fields = ('id', 'owner', 'followquestions', 'followtopics', 'something',
                  'userimg', 'userimg_url')


class SimUserInfoSerializer(serializers.ModelSerializer):
    userimg = serializers.ImageField(allow_empty_file=True, required=False)
    # 返回/media的路径
    userimg_url = serializers.SerializerMethodField()

    def get_userimg_url(self, obj):
        if obj.userimg:
            return obj.userimg.url
        else:
            return None

    class Meta:
        model = UserInfo
        fields = ('id', 'something', 'userimg_url', 'userimg')


class SimUserSerializer(serializers.ModelSerializer):
    info = SimUserInfoSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'info')
