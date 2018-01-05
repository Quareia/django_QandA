from rest_framework import permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import viewsets
from api.serializers import UserSerializer, TopicSerializer, QuestionSerializer, AnswerSerializer, MessageSerializer, UserInfoSerializer
from api.models import Topic, Question, Answer, Message, UserInfo
from rest_framework.decorators import detail_route, list_route
from api.serializers import SelTopicSerializer


class TopicViewSet(viewsets.ModelViewSet):
    """
        话题的展示，创建，更新，检索，删除操作
    """
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # 修改特定信息时用detail_route修饰,访问时使用[@]/[pk]/[function_name]/来使用
    @detail_route()
    def follow_topic(self, request, pk=None):
        try:
            topic = Topic.objects.get(pk=pk)
        except Topic.DoesNotExist:
            return Response({"msg": '话题不存在'})
        topic.followers.add(request.user.id)

        userinfo = UserInfo.objects.filter(owner=request.user)[0]
        userinfo.followtopics.add(topic.id)
        userinfo.save()

        serializer = QuestionSerializer(data=topic)
        if serializer.is_valid():
            serializer.save()
        return Response({"msg": '关注成功'})

    @detail_route()
    def cancel_follow(self, request, pk=None):
        pass

    # 获取特定信息列表时用list_route修饰,访问时使用[@]/[function_name]/来使用,可在装饰器中添加允许的方法
    @list_route()
    def my_topics(self, request):
        topics = Topic.objects.filter(owner=request.user)
        page = self.paginate_queryset(topics)
        if page is not None:
            serializer = TopicSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # 获取话题下所有问题
    @detail_route()
    def get_questions(self, request, pk=None):
        questions = Question.objects.filter(topic=pk)
        page = self.paginate_queryset(questions)
        if page is not None:
            serializer = QuestionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    @list_route()
    def search(self, request):
        # 搜索话题可以根据关键字或者标题
        title = request.query_params.get('title', None)
        if title is not None:
            topics = Topic.objects.all()
            lists = []
            for item in topics:
                if title in item.title:
                    lists.append(item)
            serializer = TopicSerializer(lists, many=True)
            return Response(serializer.data)

    @list_route()
    def get_seltopic(self, request):
        topic = Topic.objects.all()
        seri = SelTopicSerializer(topic, many=True)
        return Response(seri.data)

