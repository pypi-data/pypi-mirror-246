from collections import (
    ChainMap,
    Counter,
    OrderedDict,
    UserDict,
    UserList,
    UserString,
    defaultdict,
    deque,
    namedtuple,
)

from .applier import smart_partial

ChainMap @= smart_partial
Counter @= smart_partial
OrderedDict @= smart_partial
UserDict @= smart_partial
UserList @= smart_partial
UserString @= smart_partial
defaultdict @= smart_partial
deque @= smart_partial
namedtuple @= smart_partial
