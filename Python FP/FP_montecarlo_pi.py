from InfiniteList import InfiniteList
from random import randint
import math

def main():
    TOTAL_POINTS = 100000
    
    class Pair:
        def __init__(self, fst, snd):
            self._fst = fst
            self._snd = snd

    print(4 * len(InfiniteList.generate(lambda: Pair(randint(0, 999)/1000,  randint(0, 999)/1000)) # generate points
                              .limit(TOTAL_POINTS) # limit to total points
                              .filter(lambda p: math.sqrt(p._fst**2 + p._snd**2) < 1)
                              .toList() \
                ) / TOTAL_POINTS)
    
if __name__ == "__main__":
    main()