class Maybe:
    def __init__(self, val = None):
        if val is not None:
            return Maybe.Some(val)
        else:
            return Maybe.Noth()

    @staticmethod        
    def of(val = None):
        if val is not None:
            return Maybe.Some(val)
        else:
            return Maybe.Noth()
        
    def map(self, func) -> 'Maybe':
        if not callable(func):
            raise TypeError
        pass

    def filter(self, pred) -> 'Maybe':
        if not callable(pred):
            raise TypeError
        pass
        
    def flatMap(self, func) -> 'Maybe':
        if not callable(func):
            raise TypeError
        pass

    def ifPresent(self, cons):
        if not callable(cons):
            raise TypeError
        pass

    def isPresent(self) -> bool:
        pass

    def orElse(self, elseval):
        pass

    def orElseGet(self, prod):
        if not callable(prod):
            raise TypeError
        pass
    
    class Some:
        def __init__(self, val):
            self._val = val
        
        def get(self):
            return self._val

        def __eq__(self, other):
            if isinstance(other, Maybe.Some):
                return other._val == self._val
            return False

        def __ne__(self, other):
            return not (self == other)
        
        def filter(self, pred):
            if not callable(pred):
                raise TypeError
            if pred(self._val):
                return self
            else:
                return Maybe.Noth()
        
        def flatMap(self, func):
            if not callable(func):
                raise TypeError
            return func(self._val)
        
        def ifPresent(self, cons):
            if not callable(cons):
                raise TypeError
            cons(self._val)
        
        def isPresent(self):
            return True
        
        def map(self, func):
            if not callable(func):
                raise TypeError
            newval = func(self._val)
            if newval is not None:
                return Maybe.Some(newval)
            else:
                return Maybe.Noth()
            
        def orElse(self, elseval):
            return self._val
        
        def orElseGet(self, prod):
            if not callable(prod):
                raise TypeError
            return self._val
        
        def __str__(self):
            return f"{self._val}"
            # return f"Maybe (Some): {self._val}"
            
    class Noth:
        def __init__(self):
            pass
            
        def get(self):
            raise AttributeError
        
        def __eq__(self, other):
            return isinstance(other, Maybe.Noth)

        def __ne__(self, other):
            return not isinstance(other, Maybe.Noth)
        
        def filter(self, pred):
            if not callable(pred):
                raise TypeError
            return self
        
        def flatMap(self, func):
            if not callable(func):
                raise TypeError
            return self
        
        def ifPresent(self, cons):
            if not callable(cons):
                raise TypeError
            pass

        def isPresent(self):
            return False
        
        def orElse(self, elseval):
            return elseval

        def orElseGet(self, prod):
            if not callable(prod):
                raise TypeError
            return prod()

        def map(self, func):
            if not callable(func):
                raise TypeError
            return self
        
        def __str__(self):
            return f"-NOTH-"
            # return f"Maybe (None): -NONE-"
