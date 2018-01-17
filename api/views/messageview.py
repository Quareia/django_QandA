# -*- coding=utf-8 -*-
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import viewsets
from api.models import Message
from rest_framework.decorators import list_route, detail_route
from api.serializers.message_serializer import MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):
    """
        提供消息的展示，创建，更新，检索，删除操作
        消息的类型有用户消息0，系统消息1两种
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticated, )

    @detail_route()
    def is_read(self, request, pk=None):
        message = Message.objects.get(pk=pk)
        message.isread = 1
        message.save()
        return Response({'msg': 'read success!'})

    @list_route()
    def my_send_messages(self, request):
        messages = Message.objects.filter(origin=request.user.id)
        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = MessageSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    # 以及获取发出的消息的方法
    @list_route()
    def my_receive_messages(self, request):
        messages = Message.objects.filter(destination=request.user.id).filter(isread=0)
        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = MessageSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

