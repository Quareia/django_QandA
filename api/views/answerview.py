import time
from rest_framework import permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import viewsets
from api.models import Topic, Question, Answer, Message, UserInfo, AnswerImage
from rest_framework.decorators import detail_route, list_route

from api.serializers.answer_serializer import AnswerSerializer, AnswerImageSerializer, ReturnAnswerSerializer
from api.utils.message_send import MessageSender
# Create your views here.


class AnswerViewSet(viewsets.ModelViewSet):
    """
        提供回答的展示，创建，更新，检索，删除操作
    """
    # 需要确保只有问题的回答者才能修改删除回答
    queryset = Answer.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ReturnAnswerSerializer
        else:
            return AnswerSerializer

    #  点赞
    @detail_route()
    def agree_answer(self, request, pk=None):
        try:
            answer = Answer.objects.get(pk=pk)
            answer.ansagree = answer.ansagree + 1
            answer.save()
            return Response({'msg': 'agree answer successful'})
        except Answer.DoesNotExist:
            return Response({'msg': 'answer does not exist'})

    # 反对
    @detail_route()
    def against_answer(self, request, pk=None):
        try:
            answer = Answer.objects.get(pk=pk)
            answer.ansagainst = answer.ansagainst + 1
            answer.save()
            return Response({'msg': 'against answer successful'})
        except Answer.DoesNotExist:
            return Response({'msg': 'answer does not exist'})

    # 增加方法获取自己的回答
    @list_route()
    def my_answers(self, request):
        answers = Answer.objects.filter(owner=request.user)
        page = self.paginate_queryset(answers)
        if page is not None:
            serializer = ReturnAnswerSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ReturnAnswerSerializer(answers, many=True)
        return Response(serializer.data)

    # 模型的外键需要自己添加
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        try:
            question = Question.objects.get(pk=self.request.data['ansto'])
            info = UserInfo.objects.filter(owner=self.request.user)[0]
            followers = question.followers.all()
            # sender = MessageSender(followers, '问题 ' + str(question.title))
            # sender.start()
            for item in followers:
                message = Message.objects.create(destination=item.id,
                                                 content='问题' + str(question.title) + ' 已更新',
                                                 type=1)
                message.save()
            question.followers.add(self.request.user.info)
            info.followquestions.add(question)
            question.save()
            info.save()
        except Question.DoesNotExist:
            return Response({'status': 'question does not exist'})



