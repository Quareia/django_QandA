from threading import Thread

import time

from api.models import Message


class MessageSender(Thread):

    def __init__(self, followers, resource):
        super(MessageSender, self).__init__()
        self.followers = followers
        self.resource = resource

    def run(self):
        for item in self.followers:
            time.sleep(0.2)
            message = Message.objects.create(destination=item.id,
                                             content=self.resource + ' update',
                                             type=1)
            message.save()
