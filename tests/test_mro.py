import pytest
from c3linear.mro import (_merge, mro)


#
# Constants and auxiliary artifacts
#


class Simple(type):
    """Simplify class representation"""
    def __repr__(cls):
        return cls.__name__


class Root(object, metaclass=Simple):
    """Parent class"""
    pass


class A(Root):
    pass


class B(Root):
    pass


class C1(A, B):
    """Diamond inheritance"""
    pass


class C(Root):
    pass


class D(Root):
    pass


class E(Root):
    pass


class K1(A, B, C):
    pass


class K2(D, B, E):
    pass


class K3(D, A):
    pass


class Z(K1, K2, K3):
    pass


# Some wicked cool things

class U(Root):
    pass


class T(U):
    pass


class U(T):
    pass


#
# Tests
#

@pytest.mark.parametrize('cls, eq_or_exc', [
    (A, True),
    (C1, True),
    (Z, True),
    (U, True)
])
def test_mro(cls, eq_or_exc):
    if eq_or_exc is True:
        assert mro(cls) == cls.mro()
    else:
        with pytest.raises(eq_or_exc):
            mro(cls)
