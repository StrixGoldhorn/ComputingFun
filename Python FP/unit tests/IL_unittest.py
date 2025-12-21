import unittest
from InfiniteList import InfiniteList
from Maybe import Maybe
from Lazy import Lazy
import random

class TestInfiniteListMethods(unittest.TestCase):
    # Test laziness
    def test_laziness(self):
        random.seed(1) # 0-999: 137, 582, 867, 821, 782
        il = InfiniteList.generate(lambda: random.randint(0,999))
        self.assertEqual(il.tail().head(), 582)
        self.assertEqual(il.head(), 137)
        self.assertEqual(il.tail().tail().head(), 867)
        self.assertEqual(il.head(), 137)
        self.assertEqual(il.tail().head(), 582)
    
    # Test generate
    def test_generate(self):
        il = InfiniteList.generate(lambda: 2)
        self.assertEqual(il.head(), 2)
        self.assertEqual(il.tail().head(), 2)
        self.assertEqual(il.tail().tail().head(), 2)
        self.assertEqual(il.head(), 2)

    # Test iterate
    def test_iterate(self):
        il1 = InfiniteList.iterate(0, lambda x: x+1)
        self.assertEqual(il1.head(), 0)
        self.assertEqual(il1.tail().head(), 1)
        self.assertEqual(il1.tail().tail().head(), 2)
        self.assertEqual(il1.tail().tail().tail().head(), 3)
        self.assertEqual(il1.head(), 0)
        
        il2 = InfiniteList.iterate(1, lambda x: x*2)
        self.assertEqual(il2.head(), 1)
        self.assertEqual(il2.tail().head(), 2)
        self.assertEqual(il2.tail().tail().head(), 4)
        self.assertEqual(il2.tail().tail().tail().head(), 8)
        self.assertEqual(il2.head(), 1)
    
    # Test map
    def test_map(self):
        il1 = InfiniteList.iterate(0, lambda x: x+1).map(lambda x: x*3)
        self.assertEqual(il1.head(), 0)
        self.assertEqual(il1.tail().head(), 3)
        self.assertEqual(il1.tail().tail().head(), 6)
        self.assertEqual(il1.tail().tail().tail().head(), 9)
        self.assertEqual(il1.head(), 0)
        
        il2 = InfiniteList.iterate(1, lambda x: x*2).map(lambda x: x+2)
        self.assertEqual(il2.head(), 3)
        self.assertEqual(il2.tail().head(), 4)
        self.assertEqual(il2.tail().tail().head(), 6)
        self.assertEqual(il2.tail().tail().tail().head(), 10)
        self.assertEqual(il2.head(), 3)
        
    # Test filter
    def test_filter(self):
        nums = InfiniteList.iterate(0, lambda x: x+1) # [0, 1, 2, 3, 4, 5, 6, ...]
        evens = nums.filter(lambda x: x % 2 == 0) # [0, 2, 4, 6, 8 ...]
        moreThanFive = lambda x: x > 5
        il1 = nums.filter(moreThanFive).filter(lambda x: x % 2 == 0)
        self.assertEqual(nums.head(), 0)
        self.assertEqual(nums.tail().head(), 1)
        self.assertEqual(nums.tail().tail().head(), 2)
        self.assertEqual(nums.tail().tail().tail().head(), 3)
        self.assertEqual(nums.tail().tail().tail().tail().head(), 4)
        self.assertEqual(nums.tail().tail().tail().tail().tail().head(), 5)
        
        self.assertEqual(evens.head(), 0)
        self.assertEqual(evens.tail().head(), 2)
        self.assertEqual(evens.tail().tail().head(), 4)
        self.assertEqual(evens.tail().tail().tail().head(), 6)
        self.assertEqual(evens.tail().tail().tail().tail().head(), 8)
        self.assertEqual(evens.tail().tail().tail().tail().tail().head(), 10)
        
        self.assertEqual(il1.head(), 6)
        self.assertEqual(il1.tail().head(), 8)
        
    # Test sentinel and isSentinel
    def test_sentinel(self):
        self.assertTrue(InfiniteList.sentinel().isSentinel())
        self.assertFalse(InfiniteList.generate(lambda: 2).isSentinel())
        self.assertFalse(InfiniteList.iterate(1, lambda x: x * 2).isSentinel())
        
        self.assertTrue(InfiniteList.sentinel().map(lambda x: x + 1).isSentinel())
        self.assertTrue(InfiniteList.sentinel().filter(lambda x: x % 2 == 0).isSentinel())
        
    # Test limit
    def test_limit(self):
        self.assertTrue(InfiniteList.iterate(1, lambda x: x * 2).limit(0).isSentinel())
        self.assertFalse(InfiniteList.iterate(1, lambda x: x * 2).limit(1).isSentinel())
        self.assertTrue(InfiniteList.iterate(1, lambda x: x * 2).limit(1).tail().isSentinel())
        self.assertTrue(InfiniteList.iterate(1, lambda x: x * 2).tail().limit(1).tail().isSentinel())
        self.assertFalse(InfiniteList.generate(lambda: 2).filter(lambda x: x % 3 == 0).isSentinel())
        
    # Test toList
    def test_toList(self):
        self.assertEqual(InfiniteList.generate(lambda: 2).tail().limit(6).filter(lambda x: x % 2 != 0).toList(), [])
        self.assertEqual(InfiniteList.iterate(1, lambda x: x + 1).limit(2).toList(), [1, 2])
        self.assertEqual(InfiniteList.generate(lambda: 1).limit(4).toList(), [1, 1, 1, 1])
        self.assertEqual(InfiniteList.iterate(1, lambda x: x + 1).filter(lambda x: x > 3).limit(3).toList(), [4, 5, 6])
        self.assertEqual(InfiniteList.iterate(1, lambda x: x + 1).limit(3).filter(lambda x: x > 3).toList(), [])
        
    # Test takeWhile
    def test_takeWhile(self):
        lessThanThree = lambda x: x < 3
        lessThanTen = lambda x: x < 10
        moreThanFive = lambda x: x > 5
        isEven = lambda x: x % 2 == 0
        self.assertEqual(InfiniteList.iterate(1, lambda x: x + 1).takeWhile(lessThanTen).toList(), [1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(InfiniteList.iterate(1, lambda x: x + 1).takeWhile(lessThanThree).limit(5).toList(), [1, 2])
        self.assertEqual(InfiniteList.iterate(1, lambda x: x + 1).filter(moreThanFive).filter(isEven).takeWhile(lessThanTen).toList(), [6, 8])
        
    # Test reduce
    def test_reduce(self):
        lessThanThree = lambda x: x < 3
        self.assertEqual(InfiniteList.generate(lambda: 1).limit(3).reduce(0, lambda x, y: x+ y), 3)
        self.assertEqual(InfiniteList.iterate(1, lambda x: x + 1).takeWhile(lessThanThree).reduce(0, lambda x, y: x+ y), 3)
        
if __name__ == '__main__':
    unittest.main(verbosity=2)