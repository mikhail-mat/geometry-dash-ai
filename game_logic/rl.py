import random
import pickle
import numpy as np
from .logic import GameLogic
from .constants import GROUND_Y
from collections import defaultdict


class Environment(GameLogic):
    def reset(self):
        super().reset()
        self.env_obstacles = self.build_env_obstacles()
        self.valid_spawns = self.get_valid_spawns()

    def step(self, action):
        if action == 1:
            self.player.jump()

        self.player.in_air = True
        while self.player.in_air and self.player.alive:
            self.player.update()
            self.resolve_collisions()

        if not self.player.alive:
            return ('terminal', -1)

        next_state = self.convert_to_state()
        if next_state == 'terminal':
            return ('terminal', 0)

        return (next_state, 0)

    def convert_to_state(self):
        """
        Representing the state

        For the state to be Markov, it needs to contain all the information necessary 
        for the environment to transition to the next state and produce a reward.

        gap1  (0-30)     - gap between player and closest obstacle
        gap2  (0-5)      - gap between closest and 2nd closest obstacle
        gap3  (0-3)      - gap between 2nd closest and 3rd closest obstacle
        type1 (0-2)      - 1st obstacle type (pad / spike or block)
        type2 (0-2)      - 2nd obstacle type (pad / spike or block)
        type3 (0-2)      - 3rd obstacle type (pad / spike or block)
        obs_lvl1 (0-2)   - surface level of obstacle 1
        obs_lvl2 (0-2)   - surface level of obstacle 2
        obs_lvl2 (0-2)   - surface level of obstacle 3
        player_lvl (0-2) - surface level of the player
        """

        state = [0 for i in range(10)]
        closest_obs = self.get_closest_obstacles()

        if closest_obs == (None, None, None):
            return 'terminal'

        pad_vector = ((5, 3), 0, 0)

        state[0] = min(30, int((closest_obs[0][0]-self.player.x-80) // 6)) # 1st closest left - player right
        state[1] = max(0, min(5, (closest_obs[1][0]-closest_obs[0][1]) // 36)) \
            if closest_obs[1] is not None else pad_vector[0][0] # 2nd closest left - 1st closest right
        state[2] = max(0, min(3, (closest_obs[2][0]-closest_obs[1][1]) // 48)) \
            if closest_obs[2] is not None else pad_vector[0][1] # 3rd closest left - 2nd closest right

        for i in range(3, 6):
            state[i] = closest_obs[i-3][3] if closest_obs[i-3] is not None else pad_vector[1] # obstacle type

        for i in range(6, 9):
            state[i] = self.level_of(closest_obs[i-6][2]) \
                if closest_obs[i-6] is not None else pad_vector[2] # obstacle level

        state[9] = self.level_of(self.player.y-50)

        return tuple(state)

    def build_env_obstacles(self):
        spikes = []
        blocks = []

        for obs in self.obstacles:
            if obs.type == 'spike':
                spikes.append([obs.left, obs.right, obs.bottom-50])
            elif obs.type == 'block':
                blocks.append(obs)

        blocks = self.merge_blocks(blocks)
        TYPE_SPIKE, TYPE_BLOCK = 1, 2
        tagged = [(*s, TYPE_SPIKE) for s in spikes] + [(*b, TYPE_BLOCK) for b in blocks]
        return sorted(tagged, key=lambda obs: (obs[0], obs[3]))
        
    def get_closest_obstacles(self):
        cl1, cl2, cl3 = None, None, None
        n = len(self.env_obstacles)
        for i in range(n):
            if self.env_obstacles[i][0] >= self.player.x + 80:
                cl1 = self.env_obstacles[i]
                cl2 = self.env_obstacles[i+1] if i+1 < n else None
                cl3 = self.env_obstacles[i+2] if i+2 < n else None
                break
        return cl1, cl2, cl3

    def get_valid_spawns(self):
        occupied = set()
        for left, right, *_ in self.env_obstacles:
            occupied.update(range(int(left) - 100, int(right) + 1))
        return [x for x in range(200, 2400, 6) if x not in occupied]
 
    def level_of(self, top):
        return (GROUND_Y - top) // 50 - 1
        
    def merge_blocks(self, blocks):
        blocks = sorted(blocks, key=lambda b: b.left)

        if not blocks:
            return []

        platforms = []
        current_platform = [blocks[0].left, blocks[0].right, blocks[0].top]
        
        for i in range(1, len(blocks)):
            if blocks[i].top != current_platform[2]:
                if blocks[i].right == current_platform[1]:
                    current_platform[1] -= 100
                    if current_platform[0] != current_platform[1]:
                        platforms.append(current_platform)
                    highest = min(current_platform[2], blocks[i].top)
                    current_platform = [blocks[i].left, blocks[i].right, highest]
                else:
                    platforms.append(current_platform)
                    current_platform = [blocks[i].left, blocks[i].right, blocks[i].top]

            elif blocks[i].left == current_platform[1]:
                current_platform[1] = blocks[i].right

            else:
                platforms.append(current_platform)
                current_platform = [blocks[i].left, blocks[i].right, blocks[i].top]

        platforms.append(current_platform)
        return platforms


class TrainingLoop:
    def __init__(self):
        self.Q = defaultdict(lambda: [0.0, 0.0])
        self.gamma = 0.99
        self.alpha = 0.5
        self.eps = 0.2
        self.env = Environment()

    def policy(self, state):
        q = self.Q[state]
        if random.random() < self.eps:
            return random.randrange(2)
        best = max(q)
        return random.choice([a for a, v in enumerate(q) if v == best])

    def run_for_one_episode(self):
        self.env.reset()
        self.env.player.set_in_motion()

        exploring_start = random.choice(self.env.valid_spawns)
        self.env.player.x = exploring_start
        start = self.env.player.x
        state, reward = self.env.step(action=0)

        while state != 'terminal':
            action = self.policy(state)
            next_state, reward = self.env.step(action=action)
            TD_target = reward if next_state == 'terminal' else reward + self.gamma * max(self.Q[next_state])
            self.Q[state][action] += self.alpha * (TD_target - self.Q[state][action])
            state = next_state

        return self.env.player.x - start
    
    def train(self, episodes=20000):
        history = []
        for ep in range(episodes):
            history.append(self.run_for_one_episode())

            if ep % 500 == 0:
                recent = history[-500:]
                print(f"ep {ep:6d}  mean x progress {np.mean(recent):7.0f}  "
                      f"max x progress {max(recent):6.0f}  states {len(self.Q):6d}")

            if ep % 2000 == 0:
                print(f"ep {ep:6d}  x {self.evaluate()}")
                self.save()

    def evaluate(self, start_x=200, max_steps=2000):
        self.env.reset()
        self.env.player.set_in_motion()
        self.env.player.x = start_x
        state, _ = self.env.step(0)
        steps = 0
        while state != 'terminal' and steps < max_steps:
            action = max(range(2), key=lambda a: self.Q.get(state, [0.0, 0.0])[a])
            state, _ = self.env.step(action)
            steps += 1
        return self.env.player.x

    def save(self, path='q_table.pkl'):
        with open(path, 'wb') as f:
            pickle.dump(dict(self.Q), f)

    def load(self, path='q_table.pkl'):
        with open(path, 'rb') as f:
            self.Q = defaultdict(lambda: [0.0, 0.0], pickle.load(f))

    def trace(self, start_x=200):
        self.env.reset()
        self.env.player.set_in_motion()
        self.env.player.x = start_x
        s, _ = self.env.step(0)
        while s != 'terminal':
            q = self.Q.get(s, None)
            print(f"x={self.env.player.x:6.0f} q={q} state={s}")
            if q is None:
                print("  ^ never visited in training")
            a = max(range(2), key=lambda a: self.Q[s][a])
            s, _ = self.env.step(a)
        print("ended at", self.env.player.x)


if __name__ == '__main__':
    training_loop = TrainingLoop()
    training_loop.train()
    training_loop.save()

    training_loop.trace()

    print(training_loop.evaluate())

    print(sum(1 for v in training_loop.Q.values() if v != [0.0, 0.0]), "of", len(training_loop.Q))

    # env = Environment()
    # env.reset()
    # env.player.set_in_motion()
    # env.player.x = 400
    # s, r = env.step(0)
    # for i in range(20):
    #     print(f"x={env.player.x:6.0f} y={env.player.y:6.0f} state={s}")
    #     s, r = env.step(random.randrange(2))
    #     if s == 'terminal':
    #         print("died at", env.player.x)
    #         break
