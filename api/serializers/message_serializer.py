from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import Topic, Question, Answer, Message, UserInfo, AnswerImage


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('id', 'origin', 'destination', 'content', 'type', 'created', 'isread')



