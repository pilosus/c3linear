from collections import deque
from typing import Any, List, Tuple, Optional


class DepTail(deque):
    def __repr__(self):
        return super().__repr__().replace('DepTail', 'tail')


class Dependency:
    """
    A class representing a single linearization of class' base
    """
    def __init__(self, lst: List[type]) -> None:
        self._head = lst[0] if lst else None
        self._tail = DepTail(lst[1:]) if lst else DepTail([])

    def __contains__(self, item) -> bool:
        return item in self._tail

    def __len__(self) -> int:
        head_size = 1 if self._head else 0
        return head_size + len(self._tail)

    @property
    def head(self) -> type:
        return self._head

    @property
    def tail(self) -> DepTail:
        return self._tail

    def popleft(self) -> type:
        """
        Promote the leftmost element of the tail to the new head
        """
        head = self._head

        if self._tail:
            new_head = self._tail.popleft()
        else:
            new_head = None
        self._head = new_head

        return head

    def remove(self, item) -> Optional[type]:
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


class DependencyList:
    """
    A class represents list of linearizations (dependencies)
    """
    def __init__(self, *lists: Tuple[List[type]]) -> None:
        self._lists = [Dependency(i) for i in lists]

    def __contains__(self, item: Any) -> bool:
        """
        Return True if any linearization's tail contains an item
        """
        return any([item in l.tail for l in self._lists])

    def __len__(self):
        # the last element is parents list
        size = len(self._lists)
        return (size - 1) if size else 0

    def __repr__(self):
        if self.__len__() == 0:
            return '<[]>'
        elif self.__len__() <= 10:
            short = '<[' + ', '.join(map(str, self._lists[:-1])) + \
                    ', ' + 'Parents({})'.format(self._lists[-1]) + ']>'
            return short
        else:
            long = '<[' + ', '.join(map(str, self._lists[0:3])) + \
                   ' ... ' + str(self._lists[-2]) + ' + ' + \
                   'Parents({})'.format(self._lists[-1]) + ']>'
            return long

    @property
    def heads(self) -> List[type]:
        return [h.head for h in self._lists[:-1]]

    @property
    def tails(self) -> 'DependencyList':
        """
        Return self so that __contains__ can be called

        Used for readability reasons only
        """
        return self

    @property
    def exhausted(self) -> bool:
        """
        Return True if all elements of the lists are exhausted
        """
        return all(map(lambda x: len(x) == 0, self._lists))

    def remove(self, item: type) -> None:
        """
        Remove an item from the lists

        Once an item removed from heads, the leftmost elements of the tails
        get promoted to become the new heads.
        """
        for i in self._lists:
            if i.head == item:
                i.popleft()


def _merge(*lists) -> list:
    """
    A naive implementation of C3 linearization algorithm

    See more:
    https://en.wikipedia.org/wiki/C3_linearization
    """
    result = []
    linearizations = DependencyList(*lists)

    # FIXME infinite loops check (e.g. the head is always found in the tails,
    #  no other candidates found)
    while True:
        if linearizations.exhausted:
            return result

        for head in linearizations.heads:
            if head not in linearizations.tails:
                result.append(head)
                linearizations.remove(head)

                # Once candidate is found, continue iteration
                # from the first element of the list
                break
        else:
            # the loop never broke, no linearization could possibly be found
            raise ValueError('Cannot compute linearization, a cycle found')


def mro(cls: type) -> List[type]:
    """
    Return a list of classes in order corresponding to Python's MRO.
    """
    result = [cls]

    if not cls.__bases__:
        return result
    else:
        return result + _merge(*[mro(kls) for kls in cls.__bases__], cls.__bases__)
