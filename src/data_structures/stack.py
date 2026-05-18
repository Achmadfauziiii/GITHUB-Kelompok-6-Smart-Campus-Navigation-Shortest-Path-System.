from typing import Optional
from data_structures.linked_list import _LLNode

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
