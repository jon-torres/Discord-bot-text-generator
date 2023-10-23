class CacheManager:
    def __init__(
        self, max_size=10
    ):  # Setting default max cache size to 10; you can adjust this.
        self._cache = {}
        self._order = []
        self._max_size = max_size

    def get(self, filename):
        if filename in self._cache:
            self._order.remove(filename)
            self._order.append(filename)
            return self._cache[filename]
        return None

    def set(self, filename, value):
        if filename not in self._cache and len(self._cache) >= self._max_size:
            self._evict()
        self._cache[filename] = value
        if filename not in self._order:
            self._order.append(filename)

    def _evict(self):
        oldest_key = self._order.pop(0)
        del self._cache[oldest_key]
