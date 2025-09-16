import unittest
from calculator import Calculator

# Тесты для методов калькулятора
class TestCalculator(unittest.TestCase):
    # Подготовка объекта калькулятора
    def setUp(self):
        self.calculator = Calculator()

    def test_add(self):
        self.assertEqual(self.calculator.add(4, 7), 11)

    def test_subtract(self):
        self.assertEqual(self.calculator.subtract(10, 5), 5)

    def test_multiply(self):
        self.assertEqual(self.calculator.multiply(3, 7), 21)

    def test_divide(self):
        self.assertEqual(self.calculator.divide(10, 2), 5)
        with self.assertRaises(ValueError):
            self.calculator.divide(10, 0)

    def test_power(self):
        self.assertEqual(self.calculator.power(2, 3), 8)

    def test_modulus(self):
        self.assertEqual(self.calculator.modulus(10, 3), 1)
        with self.assertRaises(ValueError):
            self.calculator.modulus(5, 0)

    def test_sqrt(self):
        self.assertEqual(self.calculator.sqrt(16), 4)
        with self.assertRaises(ValueError):
            self.calculator.sqrt(-9)

    def test_percent(self):
        self.assertEqual(self.calculator.percent(200, 20), 40)

    def test_factorial(self):
        self.assertEqual(self.calculator.factorial(5), 120)
        with self.assertRaises(ValueError):
            self.calculator.factorial(-3)

    def test_minimax_choice(self):
        matrix = [
            [3, 5, 2],
            [4, 1, 6],
            [7, 8, 9]
        ]
        
        self.assertEqual(self.calculator.minimax_choice(matrix), (2, 7))

# Запуск тестов
if __name__ == "__main__":
    unittest.main()
