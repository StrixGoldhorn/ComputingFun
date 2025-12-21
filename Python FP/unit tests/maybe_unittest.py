import unittest
from Maybe import Maybe

class TestMaybeMethods(unittest.TestCase):
    def test_getSome(self):
        m = Maybe.of(1)
        self.assertEqual(m.get(), 1)

    def test_getNoth(self):
        m = Maybe.of()
        with self.assertRaises(AttributeError):
            m.get()
        
    # Test __eq__    
    def test_eqSomeTrue(self):
        self.assertTrue(Maybe.of(1) == Maybe.of(1))
        
    def test_eqSomeFalse(self):
        self.assertFalse(Maybe.of(1) == Maybe.of(2))
    
    def test_eqNothTrue(self):
        self.assertTrue(Maybe.of() == Maybe.of())
        
    def test_eqNothFalse(self):
        self.assertFalse(Maybe.of(1) == Maybe.of())
        
    # Test __ne__
    def test_neSomeTrue(self):
        self.assertTrue(Maybe.of(1) != Maybe.of(2))
        
    def test_neSomeFalse(self):
        self.assertFalse(Maybe.of(1) != Maybe.of(1))
    
    def test_neNothTrue(self):
        self.assertTrue(Maybe.of() != Maybe.of(1))
        
    def test_neNothFalse(self):
        self.assertFalse(Maybe.of() != Maybe.of())
        
    # Test filter
    def test_filterSomeFiltered(self):
        self.assertEqual(Maybe.of(2).filter(lambda x: x %2 == 0), Maybe.of(2))
        
    def test_filterSomeNotFiltered(self):
        self.assertEqual(Maybe.of(3).filter(lambda x: x %2 == 0), Maybe.of())
        
    def test_filterNoth(self):
        self.assertEqual(Maybe.of().filter(lambda x: x %2 == 0), Maybe.of())
        
    # Test isPresent
    def test_isPresentSome(self):
        self.assertTrue(Maybe.of(2).isPresent())
        
    def test_isPresentNoth(self):
        self.assertFalse(Maybe.of().isPresent())
        
    # Test flatMap
    def test_flatMapSome(self):
        self.assertEqual(Maybe.of(2).flatMap(lambda x: Maybe.of("Hello World")), Maybe.of("Hello World"))
        
    def test_flatMapNoth(self):
        self.assertEqual(Maybe.of().flatMap(lambda x: Maybe.of("Hello World")), Maybe.of())
        
    # Test ifPresent
    def test_ifPresentSome(self):
        class A:
            def __init__(self):
                self.q = 1
                self.s = 1
            
            def addQ(self):
                self.q += 1
                
        a = A()
        Maybe.of(a).ifPresent(lambda x: x.addQ())
        self.assertEqual(a.q, 2)
        
    def test_ifPresentNoth(self):
        class A:
            def __init__(self):
                self.q = 1
                self.s = 1
            
            def addQ(self):
                self.q += 1
                
        a = A()
        Maybe.of().ifPresent(lambda x: x.addQ())
        self.assertEqual(a.q, 1)
        
    # Test map
    def test_mapSome(self):
        self.assertEqual(Maybe.of(2).map(lambda x: "Hello World"), Maybe.of("Hello World"))
        
    def test_mapNoth(self):
        self.assertEqual(Maybe.of().map(lambda x: "Hello World"), Maybe.of())      
    
    # Test orElse
    def test_orElseSome(self):
        self.assertEqual(Maybe.of(2).orElse(5), 2)
        
    def test_orElseNoth(self):
        self.assertEqual(Maybe.of().orElse(5), 5)
        
    # Test orElseGet
    def test_orElseGetSome(self):
        self.assertEqual(Maybe.of(2).orElseGet(lambda: 5), 2)
        
    def test_orElseGetNoth(self):
        self.assertEqual(Maybe.of().orElseGet(lambda: 5), 5)


if __name__ == '__main__':
    unittest.main(verbosity=2)