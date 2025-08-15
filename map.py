# 0 -поле
# 1 - дерево
# 2 - река
# 3 - госпиталь
# 4 - АПГРЕЙД-ШОП
# 🌲🌊🚁🔥🏥🏪⚡🏆☁️ 🔲❎🥀🟩

CELL_TYPES = '❎🌲🌊🏥🏪'


class Map:

    # def generate_rivers():

    # def generate_forest():

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.cells = [[0] * w for _ in range(h)]

    def print_map(self):
        print('🔲' * (self.w + 2))
        for row in self.cells:
            print('🔲', end='')
            for cell in row:
                if 0 <= cell <= len(CELL_TYPES):
                    print(CELL_TYPES[cell], end='')
                print('🔲', end='')
            print('🔲' * (self.w + 2))

    def check_bounds(self, x, y):
        if (x < 0 or y < 0 or self.h <= x or self.w <= y):
            return False
        else:
            return True


tmp = Map(20, 10)
tmp.cells[2][2] = 2
tmp.print_map()
