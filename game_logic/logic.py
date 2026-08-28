from .constants import GROUND_Y, LAND_TOLERANCE
from .player import Player


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
    def __init__(self, x, y=GROUND_Y, width=80, height=50):
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

        for player_btm_edge_x in range(round(player.x), round(player.x + player.width) + 1):
            if pass_x_left < player_btm_edge_x < pass_x_right:
                return True

        return False


def load_level():
    return [
        Spike(600),
        Block(900),
        Spike(1200),
        Spike(1250),
        Block(1600),
        Block(1680),
        # Spike(1680,50),
        Block(1760),
    ]


class GameLogic:
    def __init__(self):
        self.reset()

    def reset(self):
        self.player = Player()
        self.obstacles = load_level()
        self.score = 0

    def step(self, action):
        if not self.player.alive:
            self.reset()
        
        if action == 1:
            if self.player.in_motion:
                self.player.jump()
            else:
                self.player.set_in_motion()
        
        self.player.in_air = True
        self.player.update()
        self.resolve_collisions()
        self.score = int(self.player.x / 10)

    def resolve_collisions(self):
        for obs in self.obstacles:
            if obs.check_collision(self.player):
                if obs.type == 'spike':
                    self.player.alive = False
                elif obs.type == 'block' and obs.get_collision_direction(self.player) == 'side':
                    self.player.alive = False
                else:
                    self.player.land_on(obs.top)
