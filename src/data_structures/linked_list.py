from typing import Optional

class _LLNode:
    def __init__(self, data):
        self.data = data
        self.next: Optional['_LLNode'] = None
