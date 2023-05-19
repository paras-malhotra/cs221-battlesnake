from typing import List, Optional, Tuple

class Queue:
    "A container with a first-in-first-out (FIFO) queuing policy."
    def __init__(self):
        self.list = []
    
    def push(self,item):
        "Enqueue the 'item' into the queue"
        self.list.insert(0,item)

    def pop(self):
        """
        Dequeue the earliest enqueued item still in the queue. This
        operation removes the item from the queue.
        """
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the queue is empty"
        return len(self.list) == 0

def minDistanceToFoodBfs(startX, startY, food: List[Tuple[int, int]], walls: List[Tuple[int, int]], width: int, height: int):
    visited = [[False for _ in range(height)] for _ in range(width)]
    queue = Queue()
    queue.push((startX, startY, 0))
    dpos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while not queue.isEmpty():
        x, y, dist = queue.pop()
        visited[x][y] = True

        if((x, y) in food):
            return dist
        
        for dx, dy in dpos:
            newx = x + dx
            newy = y + dy

            if newx >= 0 and newx < width and newy >= 0 and newy < height and (not visited[newx][newy]) and ((newx, newy) not in walls):
                queue.push((newx, newy, dist + 1))
    
    return -1