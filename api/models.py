from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Topic(models.Model):
    # 话题创建时间
    created = models.DateTimeField(auto_now_add=True)
    # 话题创建者
    owner = models.ForeignKey(to=User, related_name='topics', on_delete=models.CASCADE)
    # 话题标题
    title = models.CharField(blank=True, default='', max_length=50)
    # 话题搜索次数
    searchtimes = models.IntegerField()
    # 话题关键字
    keywords = models.CharField(blank=True, default='', max_length=50)
    # 话题的关注者,一个用户可以关注多个话题，一个话题可以被多个用户关注
    followers = models.ManyToManyField('UserInfo')

    class Meta:
        ordering = ('created',)


class Message(models.Model):
    # 消息发送时间
    created = models.DateTimeField(auto_now_add=True)
    # 消息的发送者姓名
    origin = models.CharField(max_length=20)
    # 消息的接收者姓名
    destination = models.CharField(max_length=20)
    # 消息的内容
    content = models.TextField()
    # 消息的类型(发送的消息或者回复的消息)
    type = models.CharField(max_length=20)
    # 消息是否阅读
    isread = models.IntegerField(default=0)

    class Meta:
        ordering = ('created',)


class Question(models.Model):
    # 问题提出时间
    created = models.DateTimeField(auto_now_add=True)
    # 设置related-name在user的序列化时找到user拥有的question
    owner = models.ForeignKey(to=User, related_name='questions', on_delete=models.CASCADE)
    # 问题的标题
    title = models.CharField(blank=True, default='', max_length=50)
    # 问题的内容
    description = models.TextField()
    # 所属话题
    topic = models.ForeignKey(to=Topic, related_name='questions', on_delete=models.CASCADE)
    # 问题的搜索次数
    searchtimes = models.IntegerField()
    # 问题的关注者,一个用户可以关注多个问题，一个问题可以被多个用户关注
    followers = models.ManyToManyField('UserInfo')

    class Meta:
        ordering = ('created',)


class Answer(models.Model):
    # 回答时间
    created = models.DateTimeField(auto_now_add=True)
    # 回答所针对的问题
    ansto = models.ForeignKey(to=Question, related_name='answers', on_delete=models.CASCADE)
    # 问题的回答者
    owner = models.ForeignKey(to=User, related_name='answers', on_delete=models.CASCADE)
    # 回答的内容
    description = models.TextField()
    # 回答的图片
    ansimage = models.ImageField(default='', upload_to='images', blank=True, null=True)
    # 回答点赞
    ansagree = models.IntegerField(default=0)
    # 回答反对
    ansagainst = models.IntegerField(default=0)

    class Meta:
        ordering = ('created',)


class UserInfo(models.Model):
    """
        对django自带的user进行拓展，同时又不需要
        重写原有user的认证，登陆，登出
    """
    something = models.CharField(max_length=20, blank=True, default='')
    # 用户头像
    userimg = models.ImageField(default='', upload_to='userimages', blank=True)
    # 用户信息对应的User
    owner = models.OneToOneField(to=User, related_name='info')
    # 用户所关注的问题
    followquestions = models.ManyToManyField(to=Question)
    # 用户关注的话题
    followtopics = models.ManyToManyField(to=Topic)


