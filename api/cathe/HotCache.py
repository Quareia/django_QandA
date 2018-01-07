from api.models import Question, Topic
import heapq


class HotResourcesCache(object):
    def __init__(self):
        self.topic_cache = []
        self.question_cache = []
        self.cache_size = 100
        self.now_topic = 0
        self.now_question = 0

    def add_question(self, question):
        if self.now_question < self.cache_size:
            heapq.heappush(self.question_cache, (question.searchtimes, self.now_question, question.id))
        else:
            heapq.heappop(self.question_cache[-1])
            self.now_question -= 1
            heapq.heappush(self.question_cache, (question.searchtimes, self.now_question, question.id))
        self.now_question += 1

    def add_topic(self, topic):
        if self.now_question < self.cache_size:
            heapq.heappush(self.topic_cache, (topic.searchtimes, self.now_topic, topic.id))
        else:
            heapq.heappop(self.topic_cache[-1])
            self.now_topic -= 1
            heapq.heappush(self.topic_cache, (topic.searchtimes, self.now_topic, topic.id))
        self.now_topic += 1

    def hot_topic(self):
        return self.topic_cache[:10]

    def hot_question(self):
        return self.question_cache[:10]


cache = HotResourcesCache()
