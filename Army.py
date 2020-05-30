import sys
from Ship import Ship

class Army:

    def __init__(self, small: int, medium: int, large: int, x_large: int, side: str):
        self.small = small
        self.medium = medium
        self.large = large
        self.x_large = x_large
        self.side = side
        self.army = self.set_army()

    def set_army(self):
        count = 0
        flag = [self.small, self.medium, self.large, self.x_large]
        army = [sys.getsizeof(Ship) for i in range(self.get_total_size())]
        for i in range(len(flag)):
            for j in range(flag[i]):
                army[count] = Ship(i + 1, self.side, "start")
                count += 1
        return army

    def get_total_size(self):
        return self.small + self.medium + self.large + self.x_large

    def get_ship_by_pos(self, pos: int) -> Ship:
        return self.army[pos]

    def get_army(self):
        return self.army
