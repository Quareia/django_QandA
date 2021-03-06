# -*- coding=utf-8 -*-
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import viewsets
from api.models import Topic, UserInfo
from rest_framework.decorators import detail_route, list_route
from api.serializers.question_serializer import ReturnQuestionSerializer
from api.serializers.topic_serializer import ReturnTopicSerializer, TopicSerializer, SimTopicSerializer


class TopicViewSet(viewsets.ModelViewSet):
    """
        话题的展示，创建，更新，检索，删除操作
    """
    queryset = Topic.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ReturnTopicSerializer
        else:
            return TopicSerializer

    # 修改特定信息时用detail_route修饰,访问时使用[@]/[pk]/[function_name]/来使用
    @detail_route()
    def follow_topic(self, request, pk=None):
        try:
            topic = Topic.objects.get(pk=pk)
        except Topic.DoesNotExist:
            return Response({"msg": '话题不存在'})
        topic.followers.add(request.user.info)

        userinfo = UserInfo.objects.filter(owner=request.user)[0]
        userinfo.followtopics.add(topic)
        userinfo.save()
        topic.save()
        return Response({"msg": '关注成功'})

    @detail_route()
    def cancel_follow(self, request, pk=None):
        try:
            topic = Topic.objects.get(pk=pk)
        except Topic.DoesNotExist:
            return Response({'msg': '话题不存在'})
        topic.followers.remove(request.user.info)
        try:
            userinfo = UserInfo.objects.get(owner=request.user)
            userinfo.followtopics.remove(topic)
            userinfo.save()
            topic.save()
        except UserInfo.DoesNotExist:
            return Response({'msg': '用户不存在'})
        return Response({'msg': '取消关注成功'})

    # 获取特定信息列表时用list_route修饰,访问时使用[@]/[function_name]/来使用,可在装饰器中添加允许的方法
    @list_route()
    def my_topics(self, request):
        topics = self.request.user.topics.all()
        page = self.paginate_queryset(topics)
        if page is not None:
            serializer = ReturnTopicSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ReturnTopicSerializer(topics, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # 获取话题下所有问题
    @detail_route()
    def get_questions(self, request, pk=None):
        topic = Topic.objects.get(pk=pk)
        questions = topic.questions.all()
        page = self.paginate_queryset(questions)
        if page is not None:
            serializer = ReturnQuestionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response({'msg': 'no data'})

    @list_route()
    def search(self, request):
        # 搜索话题可以根据关键字或者标题
        title = request.query_params.get('title', None)
        if title is not None:
            # 不区分大小写的查询
            lists1 = Topic.objects.filter(title__icontains=title)
            lists2 = Topic.objects.filter(keywords__icontains=title)
            page = self.paginate_queryset(lists1.union(lists2))
            if page is not None:
                serializer = ReturnTopicSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        return Response({'msg': 'no data'})

    @list_route()
    def get_sel_topic(self, request):
        topics = Topic.objects.all()
        serializer = SimTopicSerializer(topics, many=True)
        return Response(serializer.data)

    @list_route()
    # 根据搜索次数添加热门话题
    def get_hot_topic(self, request):
        topics = Topic.objects.order_by('searchtimes')[:10]
        serializer = ReturnTopicSerializer(topics, many=True)
        return Response(serializer.data)
