# Простой калькулятор
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
        return x1 / x2

    # Метод возведения в степень – принимает число и степень
    def power(self, base, exp):
        return base ** exp

    # Метод вычисления остатка от деления
    def modulus(self, x1, x2):
        return x1 % x2

    # Метод извлечения квадратного корня
    def sqrt(self, x):
        return math.sqrt(x)

    # Метод вычисления процента от числа
    def percent(self, number, percent):
        return (number * percent) / 100

    # Метод факториала числа
    def factorial(self, n):
        return math.factorial(n)

    # Метод выбора оптимальной стратегии по принципу максимакса (оптимистичный сценарий)
    def maximax_choice(self, payoff_matrix):
        # для каждой стратегии берём её лучший исход (максимум)
        row_max = [max(row) for row in payoff_matrix]
        # игрок выбирает стратегию, у которой лучший исход максимален
        best_value = max(row_max)
        best_index = row_max.index(best_value)
        return best_index, int(best_value)


