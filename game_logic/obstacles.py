from .constants import GROUND_Y, LAND_TOLERANCE


class Obstacle:
    def __init__(self, x, y=GROUND_Y, width=100, height=50):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def left(self): return self.x

    @property
    def right(self): return self.x + self.width
    
    @property
    def top(self): return self.y - self.height

    @property
    def bottom(self): return self.y

    def check_collision(self, player):
        pass

    def get_collision_direction(self, player):
        if player.prev_y <= self.top + LAND_TOLERANCE and player.vy >= 0:
            return 'top'
        return 'side'


class Block(Obstacle):
    type='block'
    def __init__(self, x, y=GROUND_Y, width=100, height=50):
        super().__init__(x, y, width, height)

    def check_collision(self, player):
        return (player.x < self.right and
                player.x + player.width > self.left and
                player.y > self.top and
                player.y - player.height < self.bottom)


class Spike(Obstacle):
    type='spike'
    def __init__(self, x, y=GROUND_Y, side_length=50):
        height = side_length * (3 ** 0.5) / 2
        super().__init__(x, y, side_length, height)

    @property
    def apex(self): return (self.x + self.width*0.5, self.top)

    def check_collision(self, player):
        if player.y < self.top or player.y > self.bottom:
            return False

        pass_x_left = self.left + ((self.bottom - player.y) / 3**0.5)
        pass_x_right = self.right - ((self.bottom - player.y) / 3**0.5)

        return player.x + player.width > pass_x_left and player.x < pass_x_right
