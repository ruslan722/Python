
import math

class Calculator:
    # Конструктор (в данном случае без параметров)
    def __init__(self):
        pass

    # Метод сложения – принимает два числа и возвращает их сумму
    def add(self, x1, x2):
        return x1 + x2

    # Метод умножения – принимает два числа и возвращает их произведение
    def multiply(self, x1, x2):
        return x1 * x2

    # Метод вычитания – принимает два числа и возвращает разность
    def subtract(self, x1, x2):
        return x1 - x2

    # Метод деления – принимает два числа и возвращает результат деления
    def divide(self, x1, x2):
        if x2 != 0:
            return x1 / x2
        else:
            raise ValueError("Деление на ноль невозможно")

    # Метод возведения в степень – принимает число и степень
    def power(self, base, exp):
        return base ** exp

    # Метод вычисления остатка от деления
    def modulus(self, x1, x2):
        if x2 != 0:
            return x1 % x2
        else:
            raise ValueError("Деление на ноль невозможно")

    # Метод извлечения квадратного корня
    def sqrt(self, x):
        if x >= 0:
            return math.sqrt(x)
        else:
            raise ValueError("Невозможно извлечь квадратный корень из отрицательного числа")

    # Метод вычисления процента от числа
    def percent(self, number, percent):
        return (number * percent) / 100

    # Метод факториала числа
    def factorial(self, n):
        if n < 0:
            raise ValueError("Факториал определён только для неотрицательных чисел")
        return math.factorial(n)

   
    def minimax_choice(self, payoff_matrix):
        
        row_max = [max(row) for row in payoff_matrix]
        # игрок выбирает стратегию, у которой худший исход максимален
        best_value = max(row_max)
        best_index = row_max.index(best_value)
        return best_index, best_value
