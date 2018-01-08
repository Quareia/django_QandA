import random
from api.models import UserInfo, Question, Answer, Message, Topic
from django.contrib.auth.models import User

user_name = ['xudong', 'sehpi', 'magua', 'jier']
question_title = ['wu', 'hehe', 'tt']
topic_title = ['sjdif', 'sdf', 'asdfji']
answer_content = ['sdjfia', 'cjicji', 'sdfs']


def create_user():
    for i in range(20):
        user = User.objects.create_user(username=random.choice(user_name) + str(i),
                                        password='qwer1234')
        info = UserInfo.objects.create(owner=user)
        user.save()
        info.save()


def create_topic():
    for title in topic_title:
        user = random.choice(User.objects.all())
        topic = Topic.objects.create(owner=user,
                                     title=title,
                                     keywords=title + str(random.randrange(10, 30)),)
        topic.save()


def create_question():
    for title in question_title:
        user = random.choice(User.objects.all())
        topic = random.choice(Topic.objects.all())

        question = Question.objects.create(topic=topic,
                                           owner=user,
                                           title=title,
                                           description=title + str(random.randrange(0, 20)))
        question.save()


def create_answer():
    for title in answer_content:
        user = random.choice(User.objects.all())
        question = random.choice(Question.objects.all())
        answer = Answer.objects.create(owner=user,
                                       ansto=question,
                                       description=title,
                                       keep=user.username + str(question.id))
        answer.save()


def create():
    create_user()
    create_topic()
    create_question()
    create_answer()
    print("Done!")
