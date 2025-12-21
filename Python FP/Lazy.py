class Lazy:
    def __init__(self, prod):
        if not callable(prod):
            raise TypeError
        self._isComputed = False
        self._val = None
        self._prod = prod
        
    @staticmethod    
    def of(prodOrVal) -> 'Lazy':
        # if is producer
        if callable(prodOrVal):
            return Lazy(prodOrVal)
        # if is value
        else:
            temp = Lazy(lambda: prodOrVal)
            temp.get()
            return temp
        
    def get(self):
        if not self._isComputed:
            self._val = self._prod()
            self._isComputed = True
        return self._val
    
    def map(self, func) -> 'Lazy':
        if not callable(func):
            raise TypeError
        return Lazy(lambda: func(self.get()))
    
    def flatMap(self, func) -> 'Lazy':
        if not callable(func):
            raise TypeError
        return Lazy(lambda: (func(self.get())).get())
    
    def filter(self, pred) -> 'Lazy':
        if not callable(pred):
            raise TypeError
        return Lazy.of(lambda: pred(self.get()))
    
    def combine(self, other: 'Lazy', combiner) -> 'Lazy':
        if not callable(combiner):
            raise TypeError
        return Lazy.of(lambda: combiner(self.get(), other.get()))
    
    def __eq__(self, other: 'Lazy') -> bool:
        if isinstance(other, Lazy):
            return other.get() == self.get()
        return False

    def __ne__(self, other: 'Lazy') -> bool:
        return not (self == other)
        
    def __str__(self) -> str:
        if self._isComputed:
            return f"{self._val}"
            # return f"Lazy (Computed): {self._val}"
        else:
            return f"?"
            # return f"Lazy (NOT computed): ?"