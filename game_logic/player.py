from .constants import GRAVITY, GROUND_Y, MOVE_VEL, JUMP_VEL

class Player:
    def __init__(self):
        self.width = 80
        self.height = 80
        self.reset()

    def reset(self):
        self.x = 200
        self.y = GROUND_Y
        self.prev_y = GROUND_Y
        self.vx = 0
        self.vy = 0
        self.in_motion = False
        self.in_air = False
        self.alive = True

    def set_in_motion(self):
        self.in_motion = True
        self.vx = MOVE_VEL

    def update(self):
        if self.in_motion:
            self.x += self.vx

            if self.in_air:
                self.vy += GRAVITY

            self.prev_y = self.y

            new_y = self.y + self.vy
            if new_y >= GROUND_Y:
                self.y = GROUND_Y
                self.vy = 0
                self.in_air = False
            else:
                self.y = new_y

    def jump(self):
        if not self.in_air:
            self.vy = JUMP_VEL
            self.in_air = True

    def land_on(self, surface_y):
        self.y = surface_y
        self.vy = 0.0
        self.in_air = False


if __name__ == '__main__':
    player = Player()
    player.set_in_motion()

    # frame = 0
    # while player.x < 2000:
    #     frame += 1
    #     player.update()
    #     if frame % 40 == 0:
    #         player.jump()
    #     print(f'frame {frame}: x={player.x:.1f}, y={player.y:.1f}, air={player.in_air}')

    start_x = player.x
    player.jump()
    while player.in_air:
        player.update()
    print(f'jump distance: {player.x - start_x:.0f}px')
