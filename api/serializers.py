from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import Topic, Question, Answer, Message, UserInfo, AnswerImage


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


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('id', 'origin', 'destination', 'content', 'type', 'created', 'isread')


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


class QuestionSerializer(serializers.ModelSerializer):
    # 关联回答的方式: 保存问题的回答的主键 id
    answers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # 问题的提出者，保存 name
    owner = serializers.ReadOnlyField(source='owner.username')
    # 问题所属话题(如果设置为只读就会出错，因为还没有，所以不能只读)
    # topic = serializers.PrimaryKeyRelatedField(queryset=Topic.objects.all())
    topic = SimTopicSerializer()
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


class AnswerSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    ansto = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    # 设置required属性允许为空, 返回的图片url是根据请求的url再加上/media/...
    # ansimage = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='image'
    # )
    # 使用slug时image是图片无法用utf-8解码
    ansimage = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='answerimage-detail'
    )

    class Meta:
        model = Answer
        fields = ('id', 'ansto', 'owner', 'description', 'ansimage', 'created',
                  'ansagree', 'ansagainst', 'keep')


class AnswerImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    image_url = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source='owner.username')

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        else:
            return None

    class Meta:
        model = AnswerImage
        fields = ('id', 'image', 'owner', 'image_url')
