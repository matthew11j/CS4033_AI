class PriorityQueue(object):
    # PriorityQueue constructor
    def __init__(self):
        self.queue = []

    def length(self): # Gets length of queue
        return len(self.queue)

    def is_empty(self): # Checks to see if queue is empty
        return len(self.queue) == []

    def enqueue(self, data): # Enqueue data into queue
        self.queue.append(data)

    def get(self): # Dequeue data from queue based on priority
        try:
            min = 0
            for i in range(len(self.queue)):
                if self.queue[i].priority < self.queue[min].priority and self.queue[i].depth <= self.queue[min].depth:
                    min = i
            item = self.queue[min]
            del self.queue[min]
            return item
        except:
            pass