from collections import deque, Counter

class PerceptionTracker:
    def __init__(self, history_size=5):
        self.history = deque(maxlen=history_size)

    def update(self, value):
        self.history.append(value)

    def most_common(self, min_count=3):
        """
        返回出现频率最高且出现次数不低于 min_count 的值
        """
        counter = Counter(self.history)
        if not counter:
            return None
        value, count = counter.most_common(1)[0]
        if value and count >= min_count:
            return value
        return None

    def recently_true(self, min_count=3):
        """判断 True 是否在历史中出现次数达到阈值"""
        return sum(1 for v in self.history if v) >= min_count
