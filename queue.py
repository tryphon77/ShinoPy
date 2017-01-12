QUEUE_MAX_SIZE = 32


class Queue():

    def __init__(self):
        self.data = [None] * QUEUE_MAX_SIZE
        self.cursor = 0

    def add(self, elt):
        self.data[self.cursor] = [elt]
        self.cursor += 1

    def remove(self, elt):
        self.data.remove(elt)
        self.cursor -= 1

    def clear(self):
        self.cursor = 0


