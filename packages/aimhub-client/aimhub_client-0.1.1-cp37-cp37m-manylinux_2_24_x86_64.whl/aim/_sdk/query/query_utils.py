import json
import itertools

from typing import Dict, Any, Union, Optional

from .proxy import AimObjectProxy

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from aim._core.storage.treeview import TreeView


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args,
                                                                 **kwargs)
        return cls._instances[cls]


class SafeNone(metaclass=Singleton):
    def get(self, item):
        return self

    def __repr__(self):
        return 'None'

    def __call__(self, *args, **kwargs):
        return self

    def __getattr__(self, item):
        return self

    def __getitem__(self, item):
        return self

    def __bool__(self):
        return False

    def __eq__(self, other):
        return other is None or isinstance(other, SafeNone)

    def __iter__(self):
        return self

    def __next__(self):
        raise StopIteration


class ContextDictView:
    def __init__(self, context_dict: Dict):
        self.context_dict = context_dict

    def __getattr__(self, item):
        return self[item]  # fallback to __getitem__

    def __getitem__(self, item):
        return self.context_dict.get(item, SafeNone())

    def get(self, item, default: Any = None):
        try:
            return self.__getitem__(item)
        except KeyError:
            return default

    def view(self, key: Union[int, str]):
        return ContextDictView(self.context_dict.get(key, SafeNone()))


class ContainerQueryProxy:
    def __init__(self, cont_hash: str, cont_tree: 'TreeView', cache: Dict):
        self._hash = cont_hash
        self._cache = cache
        self._cont_tree = cont_tree
        self._attrs_tree = cont_tree.subtree('attrs')

    @property
    def hash(self):
        return self._hash

    @property
    def type(self):
        return self._cont_tree['info_', 'cont_type']

    def __getattr__(self, item):
        return self[item]  # fallback to __getitem__

    def __getitem__(self, item):
        def _collect():
            if item not in self._cache:
                try:
                    res = self._attrs_tree.collect(item)
                except Exception:
                    res = SafeNone()
                self._cache[item] = res
                return res
            else:
                return self._cache[item]

        return AimObjectProxy(_collect, view=self._attrs_tree.subtree(item), cache=self._cache)


class SequenceQueryProxy:
    def __init__(self, name: str, get_context_fn, ctx_idx: int, seq_meta_tree: 'TreeView', cache: Dict):
        self._name = name
        self._context = None
        self._get_context_fn = get_context_fn
        self._ctx_idx = ctx_idx
        self._cache = cache
        self._tree = seq_meta_tree

    @property
    def name(self):
        return self._name

    @property
    def context(self):
        if self._context is None:
            self._context = self._get_context_fn(ctx_idx=self._ctx_idx).to_dict()
        return AimObjectProxy(lambda: self._context, view=ContextDictView(self._context))

    def __getattr__(self, item):
        def safe_collect():
            try:
                return self._tree.collect(item)
            except Exception:
                return SafeNone()

        return AimObjectProxy(safe_collect, view=self._tree.subtree(item))


def construct_query_expression(var_prefix: str, query_: Optional[str] = None, **kwargs) -> str:
    query_exprs = (f'({var_prefix}.{var_} == {json.dumps(value)})' for var_, value in kwargs.items())
    if query_ is not None:
        q = ' and '.join(itertools.chain((query_,), query_exprs))
    else:
        q = ' and '.join(query_exprs)
    return q
