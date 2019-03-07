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
    def tail(self) -> islice:
        """
        Return islice object, which is suffice for iteration or calling `in`
        """
        try:
            return islice(self, 1, self.__len__() - 1)
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
        return any([item in l.tail for l in self._lists])

    def __len__(self):
        size = len(self._lists)
        return (size - 1) if size else 0

    @property
    def heads(self) -> List[type]:
        return [h.head for h in self._lists[:-1]]

    @property
    def tails(self) -> 'DependencyList':
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

    # TODO infinite loops check (e.g. the head is always found in the tails,
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
