"""Minimal numpy/pandas stubs for Android APK without native wheels."""
from __future__ import annotations
import math, sys, types

def _install() -> None:
    try:
        import numpy  # noqa: F401
        import pandas  # noqa: F401
        return
    except Exception:
        pass

    np = types.ModuleType("numpy")

    class ndarray(list):
        def __init__(self, data=None, dtype=None):
            super().__init__(list(data) if data is not None else [])
            self.dtype = dtype
        @property
        def shape(self):
            return (len(self),)
        def astype(self, *a, **k):
            return self
        def tolist(self):
            return list(self)
        def mean(self):
            return sum(self) / len(self) if self else 0.0
        def std(self):
            if len(self) < 2:
                return 0.0
            m = self.mean()
            return math.sqrt(sum((x - m) ** 2 for x in self) / len(self))
        def min(self):
            return min(self) if self else 0.0
        def max(self):
            return max(self) if self else 0.0
        def sum(self):
            return sum(list.__iter__(self))
        def argmax(self):
            return max(range(len(self)), key=lambda i: self[i]) if self else 0
        def any(self):
            return any(self)
        def all(self):
            return all(self)
        def copy(self):
            return ndarray(self)
        def __getitem__(self, key):
            if isinstance(key, slice):
                return ndarray(list.__getitem__(self, key))
            return list.__getitem__(self, key)

    def array(data, dtype=None):
        try:
            return ndarray([float(x) for x in data], dtype=dtype)
        except Exception:
            return ndarray(list(data) if data is not None else [], dtype=dtype)

    def asarray(data, dtype=None):
        return array(data, dtype=dtype)

    def zeros(n, dtype=None):
        n = int(n) if not isinstance(n, tuple) else int(n[0])
        return ndarray([0.0] * n, dtype=dtype)

    def ones(n, dtype=None):
        n = int(n) if not isinstance(n, tuple) else int(n[0])
        return ndarray([1.0] * n, dtype=dtype)

    def full(n, fill, dtype=None):
        n = int(n) if not isinstance(n, tuple) else int(n[0])
        return ndarray([fill] * n, dtype=dtype)

    def where(cond, a=None, b=None):
        if a is None and b is None:
            return [i for i, c in enumerate(cond) if c]
        return ndarray([(a[i] if c else b[i]) for i, c in enumerate(cond)])

    def clip(x, lo, hi):
        try:
            return max(lo, min(hi, float(x)))
        except Exception:
            return x

    def isfinite(x):
        try:
            return math.isfinite(float(x))
        except Exception:
            return False

    def isnan(x):
        try:
            return math.isnan(float(x))
        except Exception:
            return False

    def corrcoef(a, b):
        a, b = list(a), list(b)
        n = min(len(a), len(b))
        if n < 2:
            return [[1.0, 0.0], [0.0, 1.0]]
        a, b = a[:n], b[:n]
        ma, mb = sum(a) / n, sum(b) / n
        cov = sum((a[i] - ma) * (b[i] - mb) for i in range(n)) / n
        sa = math.sqrt(sum((x - ma) ** 2 for x in a) / n) or 1e-12
        sb = math.sqrt(sum((x - mb) ** 2 for x in b) / n) or 1e-12
        c = cov / (sa * sb)
        return [[1.0, c], [c, 1.0]]

    np.ndarray = ndarray
    np.array = array
    np.asarray = asarray
    np.zeros = zeros
    np.ones = ones
    np.full = full
    np.where = where
    np.clip = clip
    np.isfinite = isfinite
    np.isnan = isnan
    np.corrcoef = corrcoef
    np.nan = float("nan")
    np.inf = float("inf")
    np.float64 = float
    np.int64 = int
    np.bool_ = bool
    np.sum = lambda x: sum(x)
    np.mean = lambda x: (sum(x) / len(x)) if len(x) else 0.0
    np.std = lambda x: ndarray(x).std()
    np.min = lambda x: min(x) if len(x) else 0.0
    np.max = lambda x: max(x) if len(x) else 0.0
    np.abs = abs
    np.sqrt = math.sqrt
    np.log = math.log
    np.exp = math.exp
    np.maximum = lambda a, b: max(a, b)
    np.minimum = lambda a, b: min(a, b)
    sys.modules["numpy"] = np

    pd = types.ModuleType("pandas")

    class Series(list):
        def __init__(self, data=None, index=None, dtype=None, name=None):
            data = list(data) if data is not None else []
            super().__init__(data)
            self.index = list(index) if index is not None else list(range(len(data)))
            self.dtype = dtype
            self.name = name
        def astype(self, *a, **k):
            try:
                return Series([float(x) for x in self], index=self.index, name=self.name)
            except Exception:
                return Series(self, index=self.index, name=self.name)
        def tolist(self):
            return list(self)
        def to_numpy(self, dtype=None, na_value=None):
            out = []
            for x in self:
                try:
                    if x is None or (isinstance(x, float) and math.isnan(x)):
                        out.append(na_value if na_value is not None else float("nan"))
                    else:
                        out.append(float(x))
                except Exception:
                    out.append(na_value if na_value is not None else x)
            return out
        def dropna(self):
            return Series([x for x in self if x is not None and not (isinstance(x, float) and math.isnan(x))], name=self.name)
        def fillna(self, v):
            return Series([v if (x is None or (isinstance(x, float) and math.isnan(x))) else x for x in self], name=self.name)
        def tail(self, n=5):
            return Series(self[-n:], name=self.name)
        def mean(self):
            xs = [float(x) for x in self if x is not None]
            return sum(xs) / len(xs) if xs else 0.0
        def std(self, ddof=0):
            xs = [float(x) for x in self if x is not None]
            if len(xs) < 2:
                return 0.0
            m = sum(xs) / len(xs)
            return math.sqrt(sum((x - m) ** 2 for x in xs) / max(1, len(xs) - ddof))
        def min(self):
            xs = [float(x) for x in self if x is not None]
            return min(xs) if xs else 0.0
        def max(self):
            xs = [float(x) for x in self if x is not None]
            return max(xs) if xs else 0.0
        def sum(self):
            return sum(float(x) for x in self if x is not None)
        def ewm(self, span=None, adjust=False):
            parent = self
            class _EWM:
                def mean(self_inner):
                    if not parent:
                        return Series([])
                    alpha = 2 / ((span or 10) + 1)
                    out = []; prev = float(parent[0]); out.append(prev)
                    for x in parent[1:]:
                        prev = alpha * float(x) + (1 - alpha) * prev
                        out.append(prev)
                    return Series(out, name=parent.name)
            return _EWM()
        def rolling(self, window, min_periods=None):
            parent = self
            mp = min_periods if min_periods is not None else window
            class _Roll:
                def mean(self_inner):
                    out = []
                    for i in range(len(parent)):
                        sl = parent[max(0, i + 1 - window): i + 1]
                        out.append(sum(float(x) for x in sl) / len(sl) if len(sl) >= mp else float("nan"))
                    return Series(out, name=parent.name)
                def std(self_inner, ddof=0):
                    out = []
                    for i in range(len(parent)):
                        sl = [float(x) for x in parent[max(0, i + 1 - window): i + 1]]
                        if len(sl) < mp:
                            out.append(float("nan"))
                        else:
                            m = sum(sl) / len(sl)
                            out.append(math.sqrt(sum((x - m) ** 2 for x in sl) / max(1, len(sl) - ddof)))
                    return Series(out, name=parent.name)
                def min(self_inner):
                    out = []
                    for i in range(len(parent)):
                        sl = parent[max(0, i + 1 - window): i + 1]
                        out.append(min(sl) if len(sl) >= mp else float("nan"))
                    return Series(out, name=parent.name)
                def max(self_inner):
                    out = []
                    for i in range(len(parent)):
                        sl = parent[max(0, i + 1 - window): i + 1]
                        out.append(max(sl) if len(sl) >= mp else float("nan"))
                    return Series(out, name=parent.name)
            return _Roll()
        def pct_change(self):
            out = [float("nan")]
            for i in range(1, len(self)):
                try:
                    prev = float(self[i - 1])
                    out.append((float(self[i]) - prev) / prev if prev else float("nan"))
                except Exception:
                    out.append(float("nan"))
            return Series(out, name=self.name)
        def diff(self):
            out = [float("nan")]
            for i in range(1, len(self)):
                try:
                    out.append(float(self[i]) - float(self[i - 1]))
                except Exception:
                    out.append(float("nan"))
            return Series(out, name=self.name)
        def replace(self, to_replace, value):
            return Series([value if x == to_replace else x for x in self], name=self.name)
        @property
        def iloc(self):
            parent = self
            class _ILoc:
                def __getitem__(self_inner, idx):
                    if isinstance(idx, slice):
                        return Series(list.__getitem__(parent, idx), name=parent.name)
                    return list.__getitem__(parent, idx)
            return _ILoc()
        def __getitem__(self, key):
            if isinstance(key, slice):
                return Series(list.__getitem__(self, key), name=self.name)
            return list.__getitem__(self, key)

    class DataFrame:
        def __init__(self, data=None, columns=None):
            self._data = {}
            if isinstance(data, dict):
                for k, v in data.items():
                    self._data[k] = Series(v)
            elif data is not None:
                try:
                    keys = columns or (list(data[0].keys()) if data else [])
                    for k in keys:
                        self._data[k] = Series([row.get(k) for row in data])
                except Exception:
                    pass
            self.columns = list(self._data.keys())
        def __len__(self):
            return len(next(iter(self._data.values()))) if self._data else 0
        def __getitem__(self, key):
            if isinstance(key, list):
                return DataFrame({k: self._data[k] for k in key if k in self._data})
            return self._data[key]
        def __setitem__(self, key, value):
            self._data[key] = value if isinstance(value, Series) else Series(value)
            if key not in self.columns:
                self.columns.append(key)
        def get(self, key, default=None):
            return self._data.get(key, default)
        @property
        def empty(self):
            return len(self) == 0
        def copy(self, deep=True):
            return DataFrame({k: Series(list(v)) for k, v in self._data.items()})
        def tail(self, n=5):
            return DataFrame({k: Series(list(v)[-n:]) for k, v in self._data.items()})
        @property
        def iloc(self):
            parent = self
            class _ILoc:
                def __getitem__(self_inner, idx):
                    if isinstance(idx, int):
                        return {k: v[idx] for k, v in parent._data.items()}
                    if isinstance(idx, slice):
                        return DataFrame({k: Series(list(v)[idx]) for k, v in parent._data.items()})
                    return parent
            return _ILoc()

    def to_numeric(series, errors="coerce"):
        out = []
        for x in series:
            try:
                out.append(float(x))
            except Exception:
                out.append(float("nan") if errors == "coerce" else x)
        return Series(out)

    pd.Series = Series
    pd.DataFrame = DataFrame
    pd.to_numeric = to_numeric
    pd.isna = lambda x: x is None or (isinstance(x, float) and math.isnan(x))
    sys.modules["pandas"] = pd

_install()
