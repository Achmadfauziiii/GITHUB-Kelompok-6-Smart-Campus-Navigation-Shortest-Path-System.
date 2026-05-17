# — Node Linked List internal —
class _LLNode:
    def __init__(self, data):
        self.data = data
        self.next: Optional['_LLNode'] = None


# — Queue berbasis Linked List (FIFO) —
class Queue:
    def __init__(self):
        self._head: Optional[_LLNode] = None
        self._tail: Optional[_LLNode] = None

    def enqueue(self, data) -> None:
        node = _LLNode(data)
        if self._tail:
            self._tail.next = node
        self._tail = node
        if self._head is None:
            self._head = node

    def dequeue(self):
        if self._head is None:
            raise IndexError("dequeue dari Queue kosong")
        data = self._head.data
        self._head = self._head.next
        if self._head is None:
            self._tail = None
        return data

    def is_empty(self) -> bool:
        return self._head is None


# — Stack berbasis Linked List (LIFO) —
class Stack:
    def __init__(self):
        self._top: Optional[_LLNode] = None

    def push(self, data) -> None:
        node = _LLNode(data)
        node.next = self._top
        self._top = node

    def pop(self):
        if self._top is None:
            raise IndexError("pop dari Stack kosong")
        data = self._top.data
        self._top = self._top.next
        return data

    def is_empty(self) -> bool:
        return self._top is None

# — BFS (implementasikan dari sini) —
def bfs(graph: Graph, source: str) -> List[str]:
    """BFS berbasis Queue Linked List. Big-O: O(V + E)."""
    # TODO: gunakan Queue berbasis Linked List (BUKAN collections.deque)
    visited = set()
    traversal =[]
    queue = Queue()

    queue.enqueue(source)
    visited.add(source)

    while not queue.is_empty():
        current = queue.dequeue()
        traversal.append(current)

        for neighbor, _ in graph.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.enqueue(neighbor)

    return traversal
    pass

# — DFS (implementasikan dari sini) —
def dfs(graph: Graph, source: str) -> List[str]:
    """DFS berbasis Stack Linked List. Big-O: O(V + E)."""
    # TODO: gunakan Stack berbasis Linked List (BUKAN list Python)
    visited = set()
    traversal = []
    stack = Stack()

    stack.push(source)

    while not stack.is_empty():
        current = stack.pop()
        if current in visited:
            continue

        visited.add(current)
        traversal.append(current)
        
        neighbors = graph.neighbors(current)
        for neighbor, _ in reversed(neighbors):
                if neighbor not in visited:
                    stack.push(neighbor)

    return traversal
    pass
