from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import viewsets
from api.models import Message
from rest_framework.decorators import list_route
from api.serializers.message_serializer import MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):
    """
        提供消息的展示，创建，更新，检索，删除操作
        消息的类型有用户消息0，系统消息1两种
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticated, )

    # 增加特殊的路由处理特殊的请求，获取收到的消息方法
    # 传递自己的用户名，返回所有发送者为此用户名的消息列表
    # 如果别人发给自己的消息自己删除掉，那么别人也无法看到，
    # 所以需要使用其他的删除方法
    @list_route()
    def my_send_messages(self, request):
        messages = Message.objects.filter(origin=request.user.id)
        # 可以进一步过滤自己没有删除的消息
        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = MessageSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    # 以及获取发出的消息的方法
    @list_route()
    def my_receive_messages(self, request):
        messages = Message.objects.filter(destination=request.user.id)
        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = MessageSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
