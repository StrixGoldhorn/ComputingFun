Python implementation of some Functional Programming monads

Source/idea is from CS2030S' InfiniteList, Lazy, and Maybe

**Warning** Python limits recursion depth, so functions like `InfiniteList::reduce` will throw `RecursionError` if there are too many items in InfiniteList