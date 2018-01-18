from api.models import Question, Topic
import heapq


class HotResourcesCache(object):
    def __init__(self):
        self.hot_cache = []
        self.cache_size = 100
        self.now_num = 0

    def add_item(self, item):
        if item not in self.get_all():
            if self.now_num < self.cache_size:
                heapq.heappush(self.hot_cache, (item.searchtimes, self.now_num, item))
            else:
                heapq.heappop(self.hot_cache)
                self.now_num -= 1
                heapq.heappush(self.hot_cache, (item.searchtimes, self.now_num, item))
            self.now_num += 1

    def get_all(self):
        return [item[2] for item in self.hot_cache]


cache = HotResourcesCache()
