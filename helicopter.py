import os
from utils import randcell


class Helicopter:
    """Класс, представляющий вертолет в игре"""

    def __init__(self, width: int, height: int):
        """
        Инициализация вертолета со случайной позицией на карте

        Args:
            width (int): Ширина игрового поля
            height (int): Высота игрового поля
        """
        # Устанавливаем начальные параметры
        self.x, self.y = randcell(width, height)  # Позиция вертолета
        self.width = width                        # Ширина карты
        self.height = height                     # Высота карты
        self.water_tank = 0                      # Текущий запас воды
        self.max_water = 1                       # Максимальная емкость бака
        self.score = 0                           # Счет игрока
        self.lives = 20                          # Количество жизней
        # Счетчик перемещений (для статистики)
        self.moves_count = 0

    def move(self, dx: int, dy: int) -> None:
        """
        Перемещает вертолет на заданное смещение

        Args:
            dx (int): Смещение по вертикали
            dy (int): Смещение по горизонтали
        """
        # Рассчитываем новую позицию
        new_x, new_y = self.x + dx, self.y + dy

        # Проверяем, находится ли новая позиция в пределах карты
        if 0 <= new_x < self.height and 0 <= new_y < self.width:
            self.x, self.y = new_x, new_y
            self.moves_count += 1

    def print_stats(self) -> None:
        """Выводит текущую статистику вертолета"""
        print(f'🛢️ {self.water_tank}/{self.max_water}', end=' | ')
        print(f'🏆 {self.score}', end=' | ')
        print(f'💗 {self.lives}')

    def game_over(self) -> None:
        """Обрабатывает завершение игры"""
        os.system('cls' if os.name == 'nt' else 'clear')  # Очищаем консоль
        print('╔═══════════════════════╗')
        print('║                       ║')
        print(f'║  GAME OVER! SCORE: {self.score:<4} ║')
        print('║                       ║')
        print('╚═══════════════════════╝')
        exit(0)

    def export_data(self) -> dict:
        """Экспортирует данные вертолета для сохранения"""
        return {
            'score': self.score,
            'lives': self.lives,
            'x': self.x,
            'y': self.y,
            'water_tank': self.water_tank,
            'max_water': self.max_water,
            'moves_count': self.moves_count
        }

    def import_data(self, data: dict) -> None:
        """Импортирует данные вертолета из сохранения"""
        # Устанавливаем значения по умолчанию, если данные отсутствуют
        self.x = data.get('x', 0)
        self.y = data.get('y', 0)
        self.water_tank = data.get('water_tank', 0)
        self.max_water = data.get('max_water', 1)
        self.lives = data.get('lives', 3)
        self.score = data.get('score', 0)
        self.moves_count = data.get('moves_count', 0)
