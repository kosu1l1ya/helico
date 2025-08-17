from utils import randbool
import config


class Clouds:
    """Класс для управления облаками и погодными условиями"""

    CLEAR = 0       # Ясное небо
    CLOUD = 1       # Облако
    THUNDERSTORM = 2  # Гроза

    def __init__(self, width: int, height: int):
        """
        Инициализация облачного покрова

        Args:
            width (int): Ширина поля
            height (int): Высота поля
        """
        self.width = width
        self.height = height
        self.cells = [[self.CLEAR] * width for _ in range(height)]

    def update(self) -> None:
        """Обновляет состояние облаков на карте"""
        for row in range(self.height):
            for col in range(self.width):
                # С вероятностью генерируем облака
                if randbool(config.CLOUD_PROBABILITY, config.MAX_PROBABILITY):
                    self.cells[row][col] = self.CLOUD

                    # С меньшей вероятностью превращаем в грозу
                    if randbool(config.STORM_PROBABILITY, config.MAX_PROBABILITY):
                        self.cells[row][col] = self.THUNDERSTORM
                else:
                    self.cells[row][col] = self.CLEAR

    def export_data(self) -> dict:
        """Экспортирует данные облаков для сохранения"""
        return {'cells': self.cells}

    def import_data(self, data: dict) -> None:
        """Импортирует данные облаков из сохранения"""
        self.cells = data.get(
            'cells', [[self.CLEAR] * self.width for _ in range(self.height)])
