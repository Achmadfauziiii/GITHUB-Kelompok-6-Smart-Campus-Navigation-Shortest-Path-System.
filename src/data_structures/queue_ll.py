from typing import Optional
from data_structures.linked_list import _LLNode

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
