from django.views.decorators.csrf import csrf_exempt
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if(self.perform_create(serializer) == 1):
            return Response({'msg': '您已经回答过此问题', 'status': 0})
        else:
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=201, headers=headers)

    # 模型的外键需要自己添加
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        if Answer.objects.filter(keep=self.request.user.username +
                                 str(self.request.data['ansto'])).count() == 0:
            serializer.save(keep=self.request.user.username +
                                 str(self.request.data['ansto']))
        else:
            return 1
        try:
            # js append become list
            question = Question.objects.get(pk=self.request.data['ansto'])
            info = UserInfo.objects.filter(owner=self.request.user)[0]
            followers = question.followers.all()
            # sender = MessageSender(followers, 'question ' + str(question.id))
            # sender.start()
            question.followers.add(self.request.user.info)
            info.followquestions.add(question)
            question.save()
            info.save()
        except Question.DoesNotExist:
            return Response({'status': 'question does not exist'})



