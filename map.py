from utils import randbool, randcell, randcell2
import config


class Map:
    """Класс игрового поля с различными объектами"""

    # Константы для типов клеток
    EMPTY = 0      # ❎ Пустое поле
    TREE = 1       # 🌲 Дерево
    RIVER = 2      # 🌊 Река
    HOSPITAL = 3   # 🏥 Госпиталь
    SHOP = 4       # 🏪 Магазин улучшений
    FIRE = 5       # 🔥 Огонь🏥🏪🔥🌲

    # Символы для отображения клеток
    CELL_SYMBOLS = '🟩💟❎🔲🔳🌊❎❎❎❎'

    def __init__(self, width: int, height: int):
        """
        Инициализация игрового поля

        Args:
            width (int): Ширина поля
            height (int): Высота поля
        """
        self.width = width
        self.height = height
        self.cells = [[self.EMPTY] * width for _ in range(height)]

        # Генерация игровых объектов
        self.generate_forest(config.FOREST_DENSITY, config.MAX_PROBABILITY)
        for _ in range(config.RIVER_COUNT):
            self.generate_river(config.RIVER_LENGTH)
        self.generate_building(self.SHOP)
        self.generate_building(self.HOSPITAL)

    def check_bounds(self, x: int, y: int) -> bool:
        """
        Проверяет, находятся ли координаты в пределах поля

        Args:
            x (int): Координата X
            y (int): Координата Y

        Returns:
            bool: True если координаты в пределах поля
        """
        return 0 <= x < self.height and 0 <= y < self.width

    def print_map(self, helicopter, clouds) -> None:
        """
        Выводит текущее состояние карты в консоль

        Args:
            helicopter (Helicopter): Объект вертолета
            clouds (Clouds): Объект облаков
        """
        # Верхняя граница карты
        print('❎' * (self.width + 2))

        for row_idx in range(self.height):
            print('❎', end='')  # Левая граница

            for col_idx in range(self.width):
                cell_type = self.cells[row_idx][col_idx]

                # Обработка облаков (имеют приоритет отображения)⛈️☁️
                cloud_type = clouds.cells[row_idx][col_idx]
                if cloud_type == 1:
                    print('❎', end='')
                elif cloud_type == 2:
                    print('❎', end='')

                # Отображение вертолета
                elif helicopter.x == row_idx and helicopter.y == col_idx:
                    print('🚁', end='')

                # Отображение объектов карты
                elif 0 <= cell_type < len(self.CELL_SYMBOLS):
                    print(self.CELL_SYMBOLS[cell_type], end='')

            print('❎')  # Правая граница

        # Нижняя граница карты
        print('❎' * (self.width + 2))

    def generate_forest(self, probability: int, max_probability: int) -> None:
        """
        Генерирует лес на карте

        Args:
            probability (int): Вероятность появления дерева
            max_probability (int): Максимальное значение вероятности
        """
        for row in range(self.height):
            for col in range(self.width):
                if randbool(probability, max_probability):
                    self.cells[row][col] = self.TREE

    def generate_river(self, length: int) -> None:
        """
        Генерирует реку заданной длины

        Args:
            length (int): Длина реки в клетках
        """
        x, y = randcell(self.width, self.height)
        self.cells[x][y] = self.RIVER

        # Продолжаем реку, пока не достигнем нужной длины
        while length > 0:
            x, y = randcell2(x, y)
            if self.check_bounds(x, y):
                self.cells[x][y] = self.RIVER
                length -= 1

    def generate_building(self, building_type: int) -> None:
        """
        Генерирует здание заданного типа на свободной клетке

        Args:
            building_type (int): Тип здания (SHOP или HOSPITAL)
        """
        x, y = randcell(self.width, self.height)

        # Ищем свободную клетку
        while self.cells[x][y] != self.EMPTY:
            x, y = randcell(self.width, self.height)

        self.cells[x][y] = building_type

    def add_tree(self) -> None:
        """Добавляет новое дерево на случайную свободную клетку"""
        x, y = randcell(self.width, self.height)
        if self.cells[x][y] == self.EMPTY:
            self.cells[x][y] = self.TREE

    def add_fire(self) -> None:
        """Добавляет огонь на случайное дерево"""
        x, y = randcell(self.width, self.height)
        if self.cells[x][y] == self.TREE:
            self.cells[x][y] = self.FIRE

    def update_fires(self) -> None:
        """Обновляет состояние пожаров на карте"""
        # Гасим все текущие пожары
        for row in range(self.height):
            for col in range(self.width):
                if self.cells[row][col] == self.FIRE:
                    self.cells[row][col] = self.EMPTY

        # Добавляем новые пожары
        for _ in range(config.NEW_FIRES_COUNT):
            self.add_fire()

    def process_helicopter(self, helicopter) -> None:
        """
        Обрабатывает взаимодействие вертолета с клеткой

        Args:
            helicopter (Helicopter): Объект вертолета
        """
        cell_type = self.cells[helicopter.x][helicopter.y]

        # Взаимодействие с рекой - пополнение бака
        if cell_type == self.RIVER:
            helicopter.water_tank = helicopter.max_water

        # Тушение пожара
        elif cell_type == self.FIRE and helicopter.water_tank > 0:
            helicopter.water_tank -= 1
            helicopter.score += config.TREE_BONUS
            self.cells[helicopter.x][helicopter.y] = self.TREE

        # Посещение госпиталя
        elif cell_type == self.HOSPITAL and helicopter.score >= config.LIFE_COST:
            helicopter.lives += 1
            helicopter.score -= config.LIFE_COST

        # Посещение магазина
        elif cell_type == self.SHOP and helicopter.score >= config.UPGRADE_COST:
            helicopter.max_water += 1
            helicopter.score -= config.UPGRADE_COST

    def export_data(self) -> dict:
        """Экспортирует данные карты для сохранения"""
        return {'cells': self.cells}

    def import_data(self, data: dict) -> None:
        """Импортирует данные карты из сохранения"""
        self.cells = data.get(
            'cells', [[self.EMPTY] * self.width for _ in range(self.height)])
