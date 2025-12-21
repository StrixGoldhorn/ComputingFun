import unittest
import random
from Lazy import Lazy

class TestLazyMethods(unittest.TestCase):
    # Test of with producer and value
    def test_ofProducer(self):
        m = Lazy.of(lambda: 2)
        self.assertEqual(m.__str__(), "?")
        self.assertEqual(m.get(), 2)
        self.assertEqual(m.__str__(), "2")
        
    def test_ofValue(self):
        m = Lazy.of(3)
        self.assertEqual(m.__str__(), "3")
        self.assertEqual(m.get(), 3)
        self.assertEqual(m.__str__(), "3")
    
    # Test get Laziness
    def test_getOnce(self):
        random.seed(1) # 0-999: 137, 582, 867, 821, 782
        m = Lazy.of(lambda: random.randint(0, 999))
        self.assertEqual(m.get(), 137)
        
    def test_getTwice(self):
        random.seed(1)
        m = Lazy.of(lambda: random.randint(0, 999))
        self.assertEqual(m.get(), 137)
        m.get()
        self.assertEqual(m.get(), 137)
        
    # Test __str__
    def test_strNone(self):
        random.seed(1) # 0-999: 137, 582, 867, 821, 782
        m = Lazy.of(lambda: random.randint(0, 999))
        self.assertEqual(m.__str__(), "?")
        
    def test_strOnce(self):
        random.seed(1) # 0-999: 137, 582, 867, 821, 782
        m = Lazy.of(lambda: random.randint(0, 999))
        m.get()
        self.assertEqual(m.__str__(), "137")
        
    # Test map Laziness
    def test_mapOnce(self):
        random.seed(1) # 0-999: 137, 582, 867, 821, 782
        self.assertEqual(Lazy.of(lambda: random.randint(0, 999)).map(lambda x: x+1).get(), 138)
        
    def test_mapTwice(self):
        random.seed(1)
        m = Lazy.of(lambda: random.randint(0, 999)).map(lambda x: x+2)
        self.assertEqual(m.__str__(), "?") # check that m is NOT evaluated yet
        self.assertEqual(m.get(), 139) # since m is evaluated as 137, 137+2=139
        
        m1 = Lazy.of(lambda: random.randint(0, 999))
        m2 = m1.map(lambda x: x+1)
        self.assertEqual(m1.get(), 582)
        self.assertEqual(m2.get(), 583)
    
    # Test flatMap Laziness
    def test_flatMapOnce(self):
        random.seed(1) # 0-999: 137, 582, 867, 821, 782
        self.assertEqual(Lazy.of(lambda: random.randint(0, 999)).flatMap(lambda x: Lazy.of(lambda: x+1)).get(), 138)
        
    def test_flatMapTwice(self):
        random.seed(1)
        m = Lazy.of(lambda: random.randint(0, 999)).flatMap(lambda x: Lazy.of(lambda: x+2))
        self.assertEqual(m.__str__(), "?") # check that m is NOT evaluated yet
        self.assertEqual(m.get(), 139) # since m is evaluated as 137, 137+2=139
        
        m1 = Lazy.of(lambda: random.randint(0, 999))
        m2 = m1.flatMap(lambda x: Lazy.of(lambda: x+1))
        self.assertEqual(m1.__str__(), "?") # check that m1 is NOT evaluated yet
        self.assertEqual(m2.__str__(), "?") # check that m2 is NOT evaluated yet
        self.assertEqual(m1.get(), 582)
        self.assertEqual(m2.get(), 583)
        
    # Test filter Laziness
    def test_filterOnce(self):
        random.seed(1) # 0-999: 137, 582, 867, 821, 782
        self.assertTrue(Lazy.of(lambda: random.randint(0, 999)).filter(lambda x: x % 137 == 0).get())
        
    def test_filterTwice(self):
        random.seed(1)
        m = Lazy.of(lambda: random.randint(0, 999)).filter(lambda x: x % 137 == 0)
        self.assertEqual(m.__str__(), "?") # check that m is NOT evaluated yet
        self.assertTrue(m.get())
        
        m1 = Lazy.of(lambda: random.randint(0, 999))
        m2 = m1.flatMap(lambda x: Lazy.of(lambda: x+1))
        self.assertEqual(m1.__str__(), "?") # check that m1 is NOT evaluated yet
        self.assertEqual(m2.__str__(), "?") # check that m2 is NOT evaluated yet
        self.assertTrue(m1.filter(lambda x: x % 582 == 0).get())
        self.assertTrue(m2.filter(lambda x: x % 583 == 0).get())
        
    
    # Test combiner Laziness
    def test_combineOnce(self):
        two = Lazy.of(2)
        three = Lazy.of(3)
        add = lambda x, y: x + y
        self.assertEqual(two.combine(three, add).get(), 5)
        
    def test_combineTwice(self):
        two = Lazy.of(2)
        three = Lazy.of(3)
        add = lambda x, y: x + y
        m1 = two.combine(three, add)
        m2 = m1.combine(two, add)
        self.assertEqual(m1.__str__(), "?") # check that m is NOT evaluated yet
        self.assertEqual(m2.__str__(), "?") # check that m is NOT evaluated yet
        self.assertEqual(m1.get(), 5)
        self.assertEqual(m2.get(), 7)
        
    # Test __eq__    
    def test_eqLazyTrue(self):
        self.assertTrue(Lazy.of(lambda: 1) == Lazy.of(lambda: 1))
        
    def test_eqLazyFalse(self):
        self.assertFalse(Lazy.of(lambda: 1) == Lazy.of(lambda: 2))
        
    # Test __ne__    
    def test_neLazyTrue(self):
        self.assertTrue(Lazy.of(lambda: 1) != Lazy.of(lambda: 2))
        
    def test_neLazyFalse(self):
        self.assertFalse(Lazy.of(lambda: 1) != Lazy.of(lambda: 1))
        
if __name__ == '__main__':
    unittest.main(verbosity=2)