from collections import Counter, deque


class PerceptionTracker:
    def __init__(self, history_size=5):
        self.history = deque(maxlen=history_size)

    def update(self, value):
        self.history.append(value)

    def most_common(self, min_count=3):
        """
        Returns the most common value in the history that appears at least min_count times.
        """
        counter = Counter(self.history)
        if not counter:
            return None
        value, count = counter.most_common(1)[0]
        if value and count >= min_count:
            return value
        return None

    def recently_true(self, min_count=3):
        """Returns True if True appears at least min_count times in the history."""
        return sum(1 for v in self.history if v) >= min_count
