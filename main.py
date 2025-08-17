import os
import sys

# Для старых версий Windows включаем поддержку ANSI escape codes
if os.name == 'nt':
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

# Для старых версий Windows включаем поддержку ANSI escape codes
if os.name == 'nt':
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

from pynput import keyboard
from map import Map
from helicopter import Helicopter
from clouds import Clouds
import time
import os
import json
import config


class Game:
    """Основной класс игры, управляющий игровым процессом"""

    def __init__(self):
        """Инициализация игровых объектов и параметров"""
        self.field = Map(config.MAP_WIDTH, config.MAP_HEIGHT)
        self.clouds = Clouds(config.MAP_WIDTH, config.MAP_HEIGHT)
        self.helicopter = Helicopter(config.MAP_WIDTH, config.MAP_HEIGHT)
        self.tick_counter = 1
        self.is_running = True

        # Настройки управления
        self.controls = {
            'w': (-1, 0),  # Вверх
            's': (1, 0),   # Вниз
            'a': (0, -1),  # Влево
            'd': (0, 1),   # Вправо
        }

        # Настройка обработчика клавиатуры
        self.keyboard_listener = keyboard.Listener(
            on_release=self.handle_key_release
        )
        self.keyboard_listener.start()

    def handle_key_release(self, key) -> None:
        """
        Обрабатывает нажатия клавиш

        Args:
            key: Нажатая клавиша
        """
        try:
            # Обработка движения вертолета
            if key.char in self.controls:
                dx, dy = self.controls[key.char]
                self.helicopter.move(dx, dy)

            # Сохранение игры (F)
            elif key.char == 'f':
                self.save_game()

            # Загрузка игры (G)
            elif key.char == 'g':
                self.load_game()

            # Выход из игры (Q)
            elif key.char == 'q':
                self.is_running = False

        except AttributeError:
            # Игнорируем специальные клавиши
            pass

    def save_game(self) -> None:
        """Сохраняет текущее состояние игры в файл"""
        game_data = {
            'helicopter': self.helicopter.export_data(),
            'clouds': self.clouds.export_data(),
            'field': self.field.export_data(),
            'tick': self.tick_counter
        }

        with open('savegame.json', 'w') as save_file:
            json.dump(game_data, save_file)

        print("Game saved successfully!")

    def load_game(self) -> None:
        """Загружает состояние игры из файла"""
        try:
            with open('savegame.json', 'r') as save_file:
                game_data = json.load(save_file)
            self.tick_counter = game_data.get('tick', 1)
            self.helicopter.import_data(game_data['helicopter'])
            self.field.import_data(game_data['field'])
            self.clouds.import_data(game_data['clouds'])
            print("Game loaded successfully!")
        except FileNotFoundError:
            print("No save file found!")

    def clear_display(self):
        """Очищает дисплей с помощью ANSI escape codes для избежания мерцания"""
        print("\033[H\033[J", end='')

    def run(self):
        """Основной игровой цикл"""
        try:
            while self.is_running:
                self.clear_display()

                # Обработка игровых событий
                self.field.process_helicopter(self.helicopter)
                self.helicopter.print_stats()
                self.field.print_map(self.helicopter, self.clouds)
                print(f"TICK: {self.tick_counter}")

                # Обновление игрового мира
                if self.tick_counter % config.TREE_UPDATE_INTERVAL == 0:
                    self.field.add_tree()

                if self.tick_counter % config.FIRE_UPDATE_INTERVAL == 0:
                    self.field.update_fires()

                if self.tick_counter % config.CLOUDS_UPDATE_INTERVAL == 0:
                    self.clouds.update()

                # Увеличиваем счетчик тиков и делаем паузу
                self.tick_counter += 1
                time.sleep(config.TICK_DURATION)

                # Проверка условий завершения игры
                if self.helicopter.lives <= 0:
                    self.helicopter.game_over()

        except KeyboardInterrupt:
            print("\nGame interrupted by user")
        finally:
            self.keyboard_listener.stop()


if __name__ == "__main__":
    # Создаем и запускаем игру
    game = Game()
    game.run()
