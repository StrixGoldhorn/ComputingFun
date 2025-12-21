from InfiniteList import InfiniteList

def integrate(func, start, end, num_recs):
    return (
        InfiniteList
        .iterate(start, lambda x: x + ((end - start) / num_recs)) # dx = (end - start) / num_recs
        .limit(num_recs)
        .map(lambda val: func(val) * ((end - start) / num_recs))
        .reduce(0, lambda x, y: x + y)
    )
    
def main():    
    fn1 = lambda x: 1/x
    fn2 = lambda x: x*x + 2*x
    
    print(integrate(fn1, 1, 2, 10))
    print(integrate(fn1, 1, 2, 100))
    print(integrate(fn1, 1, 2, 250))
    print()
    print(integrate(fn2, 3, 12, 10))
    print(integrate(fn2, 3, 12, 100))
    print(integrate(fn2, 3, 12, 250))
    
if __name__ == "__main__":
    main()