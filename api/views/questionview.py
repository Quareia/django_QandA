from rest_framework import permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import viewsets
from api.serializers import UserSerializer, TopicSerializer, QuestionSerializer, AnswerSerializer, MessageSerializer, UserInfoSerializer
from api.models import Topic, Question, Answer, Message, UserInfo
from rest_framework.decorators import detail_route, list_route
# Create your views here.


class QuestionViewSet(viewsets.ModelViewSet):
    """
        提供问题的展示，创建，更新，检索，删除操作
    """
    # 需要确保只有问题的提出者才能修改删除
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @detail_route()
    def add_search_times(self, request, pk=None):
        try:
            question = Question.objects.get(pk=pk)
            question.searchtimes = question.searchtimes + 1
            question.save()
            return Response({'msg': 'add search time successful'})
        except Question.DoesNotExist:
            return Response({'msg': 'question does not exist'})

    # 增加方法获取自己提出的问题,如何使用默认的分页?
    @list_route()
    def my_questions(self, request):
        # 使用序列化类序列化时，将对象当作data传入，而获取时，直接将对象传入
        # 可以控制返回的顺序
        questions = Question.objects.filter(owner=request.user.id).order_by('created',)
        page = self.paginate_queryset(questions)
        if page is not None:
            serializer = QuestionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    # 获取当前问题的所有回答
    @detail_route()
    def get_answers(self, request, pk=None):
        answers = Answer.objects.filter(ansto=pk)
        page = self.paginate_queryset(answers)
        if page is not None:
            serializer = AnswerSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data)

    @detail_route()
    def follow_question(self, request, pk=None):
        try:
            question = Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            return Response({"msg": '问题不存在'})
        question.followers.add(request.user.id)

        userinfo = UserInfo.objects.filter(owner=request.user)[0]
        userinfo.followquestions.add(question.id)
        userinfo.save()

        serializer = QuestionSerializer(data=question)
        if serializer.is_valid():
            serializer.save()
        return Response({"msg": '关注成功'})

    @detail_route()
    def cancel_follow(self, request, pk=None):
        pass

    # 在问题发生改变时，应该通知关注此问题的用户，
    # 通过消息来传送
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        try:
            # js传递时使用不同的函数得到的结果不同
            topic = Topic.objects.get(pk=self.request.data['topic'])
            followers = topic.followers.all()
            for item in followers:
                message = Message.objects.create(destination=item.id,
                                                 content='topic ' + str(topic.id) + ' update',
                                                 type=1)
                message.save()
        except Topic.DoesNotExist:
            return Response({'status': 'topic does not exist'})

    # 定义更新的操作
    # def perform_update(self, serializer):
    #     serializer.save()
    #     # 通知所有此问题的关注者，问题发生了更新，在消息中添加
    #     # 系统消息，目的地为关注者，内容是您关注的问题更新了
    #     return Response({"status": 'update ok'})

    @list_route()
    def search(self, request):
        # 搜索问题可以根据标题
        title = request.query_params.get('title', None)
        if title is not None:
            questions = Question.objects.all()
            lists = []
            for item in questions:
                if title in item.title:
                    lists.append(item)
            serializer = QuestionSerializer(lists, many=True)
            return Response(serializer.data)
        return Response({'msg': 'no data'})
