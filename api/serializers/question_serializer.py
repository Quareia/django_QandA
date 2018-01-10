from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import Topic, Question, Answer, Message, UserInfo, AnswerImage
from api.serializers.topic_serializer import SimTopicSerializer
from api.serializers.user_serializer import SimUserSerializer


class QuestionSerializer(serializers.ModelSerializer):
    # 关联回答的方式: 保存问题的回答的主键 id
    answers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # 问题的提出者，保存 name
    owner = serializers.ReadOnlyField(source='owner.username')
    # 问题所属话题(如果设置为只读就会出错，因为还没有，所以不能只读)
    topic = serializers.PrimaryKeyRelatedField(queryset=Topic.objects.all())
    # 问题的关注者
    followers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'owner', 'title', 'description', 'topic', 'searchtimes',
                  'answers', 'followers', 'created')


class SimQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'title')


class ReturnQuestionSerializer(serializers.ModelSerializer):
    # 关联回答的方式: 保存问题的回答的主键 id
    answers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # 问题的提出者，保存 name
    owner = SimUserSerializer()
    # 问题所属话题(如果设置为只读就会出错，因为还没有，所以不能只读)
    # topic = serializers.PrimaryKeyRelatedField(queryset=Topic.objects.all())
    topic = SimTopicSerializer()
    # 问题的关注者
    followers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'owner', 'title', 'description', 'topic', 'searchtimes',
                  'answers', 'followers', 'created')
