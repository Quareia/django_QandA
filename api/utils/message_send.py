from threading import Thread
from api.models import Message


class MessageSender(Thread):

    def __init__(self, followers, resource):
        super(MessageSender, self).__init__()
        self.followers = followers
        self.resource = resource

    def run(self):
        for item in self.followers:
            message = Message.objects.create(destination=item.id,
                                             content=self.resource + ' 有新的回答',
                                             type=1)
            message.save()
