from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import Topic, Question, Answer, Message, UserInfo, AnswerImage
from api.serializers.user_serializer import SimUserSerializer


class ReturnAnswerSerializer(serializers.ModelSerializer):
    owner = SimUserSerializer()
    ansto = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    ansimage = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='answerimage-detail'
    )

    class Meta:
        model = Answer
        fields = ('id', 'ansto', 'owner', 'description', 'ansimage', 'created',
                  'ansagree', 'ansagainst', 'keep')


class AnswerSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    ansto = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())

    class Meta:
        model = Answer
        fields = ('id', 'ansto', 'owner', 'description', 'created',
                  'ansagree', 'ansagainst', 'keep')


class AnswerImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        else:
            return None

    class Meta:
        model = AnswerImage
        fields = ('id', 'image', 'image_url')
