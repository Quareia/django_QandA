from rest_framework import permissions
from rest_framework import viewsets
from api.serializers import AnswerImageSerializer
from api.models import AnswerImage


class AnswerImageViewSet(viewsets.ModelViewSet):
    """
        查询答案中的图片
    """
    queryset = AnswerImage.objects.all()
    serializer_class = AnswerImageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

