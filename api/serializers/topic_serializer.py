from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import Topic, Question, Answer, Message, UserInfo, AnswerImage
from api.serializers.user_serializer import SimUserSerializer


class ReturnTopicSerializer(serializers.ModelSerializer):
    owner = SimUserSerializer()
    followers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    questions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = ('id', 'owner', 'title', 'keywords', 'searchtimes', 'created',
                  'followers', 'questions')


class TopicSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    followers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    questions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = ('id', 'owner', 'title', 'keywords', 'searchtimes', 'followers',
                  'questions', 'created')


class SimTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('id', 'title')
