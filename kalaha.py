import sys

import pygame

from kalaha_agent import KalahaAgent
from kalaha_env import KalahaEnv


def play_game_with_render(env, agent=None):
    """
    while True:
        action = int(input("action: "))
        next_state, reward, done = env.step(action)
        print(next_state)
    """

    env.render()
    while True:
        if agent and env.current_player == agent_a.index:
            action = agent_a.act(env.current_state)
            env.step(action)
            env.render()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

                action = -1
                if event.key == pygame.K_1:
                    action = 1
                if event.key == pygame.K_2:
                    action = 2
                if event.key == pygame.K_3:
                    action = 3
                if event.key == pygame.K_4:
                    action = 4
                if event.key == pygame.K_5:
                    action = 5
                if event.key == pygame.K_6:
                    action = 6

                if action != -1:
                    next_state, reward, done = env.step(action)
                    # print(next_state)
                    env.render()

                    if done:
                        print("DONE")
                        env.reset()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass


def play_game(env, agent_a, agent_b):
    env.reset()
    print("\nNow playing Kalaha!!")
    print(agent_a)
    print(agent_b)

    while True:
        print(env)  # print environment
        action = agent_a.act(env.current_state) if env.current_player == agent_a.index \
            else agent_b.act(env.current_state)

        next_state, reward, done = env.step(action)

        if done:  # or env.current_step > 10:
            agent_a_score = next_state[env.get_target_index(agent_a.index)]
            agent_b_score = next_state[env.get_target_index(agent_b.index)]
            break

    print("\nDONE")
    print("steps:", env.current_step)
    print("agent_a_score:", agent_a_score)
    print("agent_b_score:", agent_b_score)


if __name__ == '__main__':
    n_pits = 6  # pits per player
    n_balls = 4  # balls per pit

    env = KalahaEnv(n_pits, n_balls)
    agent_a = KalahaAgent(0, n_pits, n_balls, strategy="max_score")
    agent_b = KalahaAgent(1, n_pits, n_balls, strategy="playbook")

    # play_game_with_render(env, None)  # human vs human
    # play_game_with_render(env, agent_b)  # human vs agent
    play_game(env, agent_a, agent_b)  # agent vs agent
