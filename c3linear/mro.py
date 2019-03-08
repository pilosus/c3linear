from collections import deque
from itertools import islice
from typing import List, Tuple, Optional


class Dependency(deque):
    @property
    def head(self) -> Optional[type]:
        try:
            return self[0]
        except IndexError:
            return None

    @property
    def tail(self) -> islice:  # type: ignore
        """
        Return islice object, which is suffice for iteration or calling `in`
        """
        try:
            return islice(self, 1, self.__len__())
        except (ValueError, IndexError):
            return islice([], 0, 0)


class DependencyList:
    """
    A class represents list of linearizations (dependencies)

    The last element of DependencyList is a list of parents.
    It's needed  to the merge process preserves the local
    precedence order of direct parent classes.
    """
    def __init__(self, *lists: Tuple[List[type]]) -> None:
        self._lists = [Dependency(i) for i in lists]

    def __contains__(self, item: type) -> bool:
        """
        Return True if any linearization's tail contains an item
        """
        return any([item in l.tail for l in self._lists])  # type: ignore

    def __len__(self):
        size = len(self._lists)
        return (size - 1) if size else 0

    def __repr__(self):
        return self._lists.__repr__()

    @property
    def heads(self) -> List[Optional[type]]:
        return [h.head for h in self._lists]

    @property
    def tails(self) -> 'DependencyList':  # type: ignore
        """
        Return self so that __contains__ could be called

        Used for readability reasons only
        """
        return self

    @property
    def exhausted(self) -> bool:
        """
        Return True if all elements of the lists are exhausted
        """
        return all(map(lambda x: len(x) == 0, self._lists))

    def remove(self, item: Optional[type]) -> None:
        """
        Remove an item from the lists

        Once an item removed from heads, the leftmost elements of the tails
        get promoted to become the new heads.
        """
        for i in self._lists:
            if i and i.head == item:
                i.popleft()


def _merge(*lists) -> list:
    result: List[Optional[type]] = []
    linearizations = DependencyList(*lists)

    while True:
        if linearizations.exhausted:
            return result

        for head in linearizations.heads:
            if head and (head not in linearizations.tails):  # type: ignore
                result.append(head)
                linearizations.remove(head)

                # Once candidate is found, continue iteration
                # from the first element of the list
                break
        else:
            # Loop never broke, no linearization could possibly be found
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
