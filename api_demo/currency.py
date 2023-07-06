from abc import abstractmethod
from numbers import Real
from decimal import Decimal

def force_same(cls):
    from inspect import signature
    def __getattribute__(self, name):
        first_param_called_other = lambda a: list(signature(a).parameters.keys())[0] == "other"
        
        is_abstract_method = lambda name: name in cls.__abstractmethods__
        
        attr = object.__getattribute__(self, name)
        
        if hasattr(attr, '__call__') and is_abstract_method(name) and first_param_called_other(attr):
            def _(*args, **kwargs):
                if not isinstance(args[0], type(self)): raise ValueError
                return attr(*args, **kwargs)
            return _
        else:
            return attr
    
    cls.__getattribute__ = __getattribute__
    return cls


@force_same
class Currency(Real):
    def __repr__(self, places=2, sep=',', dp='.'):
        q = Decimal(10) ** -places
        sign, digits, exp = self._quantity.quantize(q).as_tuple()
        result = []
        digits = list(map(str, digits))
        build, next = result.append, digits.pop
        for i in range(places):
            build(next() if digits else '0')
        if places: build(dp)
        if not digits: build('0')
        i = 0
        while digits:
            build(next())
            i += 1
            if i == 3 and digits:
                i = 0
                build(sep)
        build(self.curr)
        return ''.join(reversed(result))
        
class Dollar(Decimal, Currency):
    curr = "$"
