QUEUE_MAX_SIZE = 32


class Queue():

    def __init__(self):
        self.data = [None] * QUEUE_MAX_SIZE
        self.cursor = 0


    def add(self, elt):
        # print 'add at pos %d' % self.cursor
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


    def __iter__(self):
        return iter(self.data[:self.cursor])


    def __str__(self):
        return 'Queue : [%s]' % (', '.join([str(x) for x in self.data[:self.cursor]]))


if __name__ == '__main__':
    test = Queue()
    for i in range(10):
        test.add(i)
    
    print(test.data)
    
    for x in test:
        print(x)
        if 3 <= x <= 5:
            test.remove(x)
    
    for x in test:
        print(x)
    
    print(test.data)
    
    # test.add(42)
    
    # for x in test:
        # print x
    
    # test.clear()
    
    # for x in test:
        # print x
