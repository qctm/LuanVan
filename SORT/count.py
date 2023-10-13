class Counter:
    def __init__(self):
        self.xelist = []
    def add(self, id, y):
        if self.xelist.count(id) == 0:
            self.xelist[id] = y
    def count(self):
        c = len(sorted(set(self.xelist),key=self.xelist.index))
        if c == 0:
            return 0
        return c