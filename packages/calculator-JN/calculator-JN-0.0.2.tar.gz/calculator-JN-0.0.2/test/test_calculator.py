import unittest
from calculator import Calculator

class TestCalculator(unittest.TestCase):

    def setUp(self):
        """
        Set up step to create a Calculator instance that runs before 
        each test method. 

        """
        self.calc = Calculator()

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            self.calc.add('a')

    def test_add(self):
        self.calc.add(2)
        self.assertEqual(self.calc.res, 2)

    def test_subtract(self):
        self.calc.subtract(1)
        self.assertEqual(self.calc.res, -1)  
    
    def test_multiply(self):
        self.calc.add(2)
        self.calc.multiply(3)
        self.assertEqual(self.calc.res, 6)  

    def test_divide(self):
        self.calc.add(2)
        self.calc.divide(1)
        self.assertEqual(self.calc.res, 2)  
    
    def test_divide_by_zero(self):
        """zero division error should be raised and bubbled up to downstream developers"""
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(0)
    
    def test_nroot(self):
        self.calc.add(9)
        self.calc.n_root(2)
        self.assertEqual(self.calc.res, 3)
    
    def test_even_root_for_negative_number(self):
        self.calc.subtract(9)
        with self.assertRaises(ValueError):
            self.calc.n_root(2)

    def test_zero_root(self):
        self.calc.add(2)
        with self.assertRaises(ZeroDivisionError):
            self.calc.n_root(0)
    
    def test_reset(self):
        self.calc.add(2)
        self.calc.reset()
        self.assertEqual(self.calc.res, 0)

if __name__ == '__main__':
    unittest.main()
