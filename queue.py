QUEUE_MAX_SIZE = 32


class Queue():

    def __init__(self):
        self.data = [None] * QUEUE_MAX_SIZE
        self.cursor = 0

    def add(self, elt):
        print 'add at pos %d' % self.cursor
        self.data[self.cursor] = elt
        self.cursor += 1

    def remove(self, elt):
        self.data.remove(elt)
        self.data += [None]
        self.cursor -= 1

    def clear(self):
        self.cursor = 0

    def index(self, elt):
        # only for debug purposes
        if elt in self.data:
            return self.data.index(elt)
        else:
            return -1

