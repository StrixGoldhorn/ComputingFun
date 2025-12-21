from Lazy import Lazy
from Maybe import Maybe

class InfiniteList:
    
    def __init__(self, head, tail):
        self._head = head # Lazy<Maybe<T>>
        self._tail = tail # Lazy<IL<T>>
    
    def head(self):
        # If self._head evaluates to a Maybe.Noth, skip this node.
        return self._head.get().orElseGet(lambda: self._tail.get().head())
    
    def tail(self) -> 'InfiniteList':
        return self._head.get().map(lambda x: self._tail.get()).orElseGet(lambda: self._tail.get().tail())
    
    @staticmethod
    def generate(prod) -> 'InfiniteList':
        if not callable(prod):
            raise TypeError
        head = Lazy.of(lambda: Maybe.of(prod())) # Lazy<Maybe<T>>
        tail = Lazy.of(lambda: InfiniteList.generate(prod)) # Lazy<IL<T>>
        return InfiniteList(head, tail)
    
    @staticmethod
    def iterate(seed, trans) -> 'InfiniteList':
        if not callable(trans):
            raise TypeError
        head = Lazy.of(lambda: Maybe.of(seed)) # Lazy<Maybe<T>>
        tail = Lazy.of(lambda: InfiniteList.iterate(trans(seed), trans)) # Lazy<IL<T>>
        return InfiniteList(head, tail)
    
    def map(self, trans) -> 'InfiniteList':
        if not callable(trans):
            raise TypeError
        head = self._head.map(lambda m: m.map(trans))
        tail = self._tail.map(lambda il: il.map(trans))
        return InfiniteList(head, tail)
    
    def filter(self, pred) -> 'InfiniteList':
        if not callable(pred):
            raise TypeError
        head = Lazy.of(lambda: self._head.get().filter(pred))
        tail = Lazy.of(lambda: self._tail.get().filter(pred))
        return InfiniteList(head, tail)
    
    def limit(self, n: int) -> 'InfiniteList':
        # base case, n == 0, return sentinel
        if (n <= 0):
            return InfiniteList.SENTINEL
        else:
            head = self._head
            # if head is Maybe.Noth, no count
            tail = Lazy.of(lambda: self._head.get().map(lambda x: self._tail.get().limit(n-1)).orElseGet(lambda: self._tail.get().limit(n)))
            return InfiniteList(head, tail)
    
    def toList(self) -> list:
        out = []
        curr = self
        while not curr.isSentinel():
            curr._head.get().ifPresent(lambda x: out.append(x))
            curr = curr._tail.get()
        return out
    
    def takeWhile(self, pred) -> 'InfiniteList':
        if not callable(pred):
            raise TypeError
        lazybool = self._head.filter(lambda m: m.map(lambda val: pred(val)).orElse(True))
        # set head's Lazy<Maybe<T>> to either a Lazy<Maybe.Some<T>> or Lazy<Maybe.Noth<T>>,
        # depending on whether lazybool filters it out
        head = lazybool.map(lambda b: self._head.get().filter(lambda x: b))
        # set tail's Lazy<IL<T> to either a Lazy<IL<T>> or Lazy<IL.SENTINEL>,
        # depending on whether lazybool filters it out
        tail = lazybool.map(lambda b: self._tail.get().takeWhile(pred) if b else InfiniteList.SENTINEL)
        return InfiniteList(head, tail)
    
    def reduce(self, identity, accum):
        if not callable(accum):
            raise TypeError
        # if head is Lazy<Maybe.Some<T>>, include in result.
        # else skip this node
        return self._head.get()\
                    .map(lambda val: self._tail.get().reduce(accum(identity, val), accum))\
                    .orElseGet(lambda: self._tail.get().reduce(identity, accum))
        
    def isSentinel(self) -> bool:
        return self == InfiniteList.SENTINEL
    
    def __str__(self):
        return f"Head: {str(self._head)}\nTail: {str(self._tail)}"    
    
    class Sentinel:
        def __init__(self):
            self._head = None
            self._tail = None
        
        def head(self):
            raise NameError
        
        def tail(self):
            raise NameError
        
        def map(self, trans) -> 'InfiniteList':
            if not callable(trans):
                raise TypeError
            return self
        
        def filter(self, pred) -> 'InfiniteList':
            if not callable(pred):
                raise TypeError
            return self
        
        def limit(self, n: int) -> 'InfiniteList':
            return self
        
        def isSentinel(self) -> bool:
            return True
        
        def toList(self) -> list:
            return []
        
        def takeWhile(self, pred) -> 'InfiniteList':
            if not callable(pred):
                raise TypeError
            return self
        
        def reduce(self, identity, accum):
            if not callable(accum):
                raise TypeError
            return identity
        
        def __str__(self):
            "-"
    
    SENTINEL = Sentinel()
    
    @staticmethod
    def sentinel() -> 'InfiniteList':
        return InfiniteList.SENTINEL