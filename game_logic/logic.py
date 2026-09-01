from .player import Player
from .obstacles import Block, Spike
from .constants import GROUND_Y


def load_level():
    return [
        Spike(600),
        Block(900),
        Spike(1200),
        Spike(1250),
        Block(1600),
        Block(1700),
        Spike(1700,GROUND_Y-50),
        Spike(1750,GROUND_Y-50),
        Block(1800),
        Block(1900),
        Spike(2000),
        Spike(2200),
        Block(2500),
        Block(2600),
        Block(2700),
        Block(2600,GROUND_Y-50),
        Block(2700,GROUND_Y-50),
        Block(2700,GROUND_Y-100),
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
            if obs.right < self.player.x or obs.left > self.player.x + 100: 
                continue
            
            if obs.check_collision(self.player):
                if obs.type == 'spike':
                    self.player.alive = False
                elif obs.type == 'block' and obs.get_collision_direction(self.player) == 'side':
                    self.player.alive = False
                else:
                    self.player.land_on(obs.top)
