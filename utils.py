from random import randint as rand, choice
import os


def randbool(probability: int, max_probability: int) -> bool:
    """
    Генерирует случайное булево значение с заданной вероятностью

    Args:
        probability (int): Вероятность возврата True (должна быть <= max_probability)
        max_probability (int): Максимальное значение вероятности

    Returns:
        bool: True с вероятностью probability/max_probability
    """
    # Генерируем случайное число и проверяем его вхождение в диапазон
    return rand(0, max_probability) <= probability


def randcell(width: int, height: int) -> tuple[int, int]:
    """
    Генерирует случайные координаты в пределах игрового поля

    Args:
        width (int): Ширина игрового поля
        height (int): Высота игрового поля

    Returns:
        tuple: (y, x) координаты случайной клетки
    """
    # Генерируем случайные координаты в границах поля
    return (rand(0, height - 1), rand(0, width - 1))


def randcell2(x: int, y: int) -> tuple[int, int]:
    """
    Возвращает случайную соседнюю клетку относительно текущей позиции

    Args:
        x (int): Текущая координата X
        y (int): Текущая координата Y

    Returns:
        tuple: Новые координаты (x, y)
    """
    # Возможные направления движения: вверх, вправо, вниз, влево
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    # Выбираем случайное направление и вычисляем новую позицию
    dx, dy = choice(directions)
    return (x + dx, y + dy)

def clear_screen():
    """Очищает экран консоли кроссплатформенным способом"""
    # Для Windows
    if os.name == 'nt':
        os.system('cls')
    # Для Linux/MacOS
    else:
        os.system('clear')
