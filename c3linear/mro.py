from collections import deque


class BaseStack:
    def __init__(self, lst: list):
        self._head = lst[0] if lst else None
        self._tail = deque(lst[1:]) if lst else deque([])

    @property
    def head(self):
        return self._head

    @property
    def tail(self):
        return self._tail

    def popleft(self):
        head = self._head

        if self._tail:
            new_head = self._tail.popleft()
        else:
            new_head = None
        self._head = new_head

        return head

    def __contains__(self, item):
        """
        Return True if self._tail contains an item, False otherwise
        """
        return item in self._tail

    def __len__(self):
        head_size = 1 if self._head else 0
        return head_size + len(self._tail)

    def remove(self, item):
        """
        Remove and return value from the tail and head if present or None otherwise
        """
        if self._head == item:
            return self.popleft()

        try:
            self._tail.remove(item)
        except ValueError:
            return None
        else:
            return item

    def __repr__(self):
        return 'head({}) + {}'.format(self._head, self._tail)


def merge(*lsts) -> list:
    """
    >>> merge(*[['C', 'A', 'O'], ['D', 'B', 'O'], ['C', 'D']])
    ['C', 'A', 'D', 'B', 'O']
    """
    result = []
    items = [BaseStack(i) for i in lsts]

    # TODO optimize!
    while True:
        if all([len(i) == 0 for i in items]):
            return result

        for idx in range(len(items) - 1):
            head = items[idx].head
            not_in_tail = [head not in j for j in items]
            if all(not_in_tail):
                result.append(head)
                for jdx in range(len(items)):
                    if items[jdx].head == head:
                        items[jdx].popleft()
                break


def linearize(cls: type):
    result = [cls]
    bases = cls.__bases__

    if (not bases) or (bases == (object, )):
        return result
    else:
        # recursive call
        return result + merge(*[linearize(c) for c in bases], bases)
