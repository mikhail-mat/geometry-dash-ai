# GeometryDash AI

A simple Geometry Dash-inspired platformer built with Pygame, and a reinforcement learning agent that learns to beat a custom level using one-step Q-learning.

I built it as the practical part of an extended project on the foundations of reinforcement learning, supervised by and presented to my school's head of maths.

## Agent gameplay

https://github.com/user-attachments/assets/883c175d-9284-4a9a-8ded-474facda6c18

The greedy policy after 10,000 training episodes.

## Human gameplay

https://github.com/user-attachments/assets/f5ea2b92-e49e-463a-b122-0bee0cc21070

## Running it

Tested on Python 3.11.15.

```bash
git clone https://github.com/mikhail-mat/geometry-dash-ai.git
cd geometry-dash-ai
pip install -r requirements.txt
```

**Play the game or watch the agent**

```bash
python main.py
```

To switch between playing yourself and watching the agent, set `self.mode` in `states/gameplay.py` to `'human'` or `'agent'`.

**Train the agent from scratch**

```bash
python -m game_logic.rl
```

Run this from the repo root. `rl.py` uses relative imports, so `python rl.py` on its own won't work. Training runs without any graphics, prints progress every 500 episodes and saves the Q-table to `q_table.pkl` every 2,000 episodes.

A trained `q_table.pkl` is included, so you can watch the agent without training it first.

## How it's built

I knew that for training to be effective, I'd have to separate the core game logic from the graphics, the UI and the rendering, so that training can run headless at full speed.
 
```
main.py, game.py   startup and the main game loop
ui.py              custom Pygame UI classes
states/            menu screens and the gameplay state
game_logic/        game physics and RL (no Pygame)
    logic.py       game physics
    rl.py          RL environment and Q-learning training loop
```
 
- `main.py` and `game.py` act as the conductor. `game.py` contains a state machine that runs the game loop and switches between game states, while the states themselves aren't aware of each other.
- `states/` holds the game states, from menu screens built with custom Pygame UI classes (text boxes, buttons, input fields) to the gameplay state itself.
- `game_logic/` is plain Python with no Pygame. It contains the game physics and `rl.py`, which trains the agent when run on its own and gives `gameplay.py` what it needs to show the agent's policy on screen.

## How the agent works

### Why Q-learning

In Monte Carlo methods, the value function can only be updated once a whole episode has finished. MC could have worked here, but it would probably have taken longer to train. TD methods update after every step by bootstrapping from the current estimate of the next state, so I went with Q-learning, a well-known off-policy TD method.

Being off-policy matters here. The agent explores with an ε-greedy policy, but Q-learning's update target uses the best next action, so it learns the values of the greedy policy even while it is still exploring.

### Steps and actions

The agent has two actions: do nothing (0) or jump (1).

One step is not one frame. After the action, the environment keeps running the physics until the player is back on a surface. There's nothing to decide mid-air, so the agent only makes decisions while grounded. This keeps episodes short and means the state doesn't need to include the player's vertical velocity.

### State representation

I didn't want the agent to simply memorise the level by choosing actions from its x and y coordinates. Instead, the state describes what is ahead of the player, similar to what a human player sees, just more precise. A coordinate is unique to one spot on one level, while this representation can be true at many different positions.

| Feature | Range | Meaning |
|---|---|---|
| `gap1` | 0–30 | Gap from the player to the nearest obstacle, in 6 px units |
| `gap2` | 0–5 | Gap between the 1st and 2nd obstacles, in 36 px units |
| `gap3` | 0–3 | Gap between the 2nd and 3rd obstacles, in 48 px units |
| `type1`–`type3` | 0–2 | Obstacle type: 0 = none, 1 = spike, 2 = block (adjacent blocks are merged into platforms) |
| `obs_lvl1`–`obs_lvl3` | 0–2 | Surface level of each obstacle, in 50 px tiers |
| `player_lvl` | 0–2 | Surface level the player is on |

When a gap is at its maximum value, nothing is within range and that slot is marked as empty (type 0). This gives at most 1,627,128 possible states, most of which can never occur. Training visited [TODO: N] of them.

The representation is designed to be close to Markov, meaning the next state and reward depend only on the current state and action. It isn't perfectly Markov: gaps are rounded into buckets and the agent can only see three obstacles ahead, so two positions in the same bucket can play out slightly differently. In practice it is close enough for the agent to learn a policy that beats the level.

Because the state describes the player's surroundings rather than its position, the same policy could in principle work on other levels with similar obstacle patterns. I haven't tested this yet.

### Rewards

- −1 for dying
- 0 for every other step, including reaching the end of the level

An episode ends when the player dies or when there are no obstacles left ahead.

There's no bonus for finishing. With γ = 0.99, a state's value depends on how soon death follows it, so the best policy is simply the one that never dies.

Q-values start at 0. That is optimistic, since no real return is above 0, so untried actions look at least as good as tried ones and the agent is pushed to explore.

### Training

| Hyperparameter | Value |
|---|---|
| Learning rate α | 0.5 |
| Discount γ | 0.99 |
| Exploration ε | 0.2 (constant) |
| Episodes | 10,000 |

- **Exploring starts:** each episode begins at a random position on the level, away from obstacles, so the agent practises later sections without first having to master the earlier ones.
- **High learning rate:** α = 0.5 is high, but the game is deterministic, so there's no noise to average out.
- **Evaluation:** every 2,000 episodes, the greedy policy is run from the start of the level to measure how far it gets.

## What I learned

The biggest challenge was definitely the RL part. It was difficult to apply concepts I'd mostly learned in theory (MDPs, TD learning) to a practical problem. I had to design the environment, which moves from one state to the next and produces rewards, and frame the problem so that a tabular method could actually solve it.

I'll be taking a lot from this into future projects: practical skills like Pygame, better OOP and software architecture, and especially designing state representations and framing problems so they can be solved with RL.

## Next steps

- Test whether the policy generalises, using procedurally generated levels

## Credits

Not affiliated with or endorsed by RobTop Games. Geometry Dash is a trademark of RobTop Games.

## Licence

MIT. See [LICENSE](LICENSE).
