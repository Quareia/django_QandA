from rest_framework import serializers
from api.models import Question, Answer, AnswerImage
from api.serializers.question_serializer import SimQuestionSerializer
from api.serializers.user_serializer import SimUserSerializer


class ReturnAnswerSerializer(serializers.ModelSerializer):
    owner = SimUserSerializer()
    ansto = SimQuestionSerializer()

    class Meta:
        model = Answer
        fields = ('id', 'ansto', 'owner', 'description', 'created',
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
