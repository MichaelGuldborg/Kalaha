import sys

import pygame

from kalaha.kalaha_agent import KalahaAgent
from kalaha.kalaha_env import KalahaEnv


def play_game(env):
    """
    while True:
        action = int(input("action: "))
        next_state, reward, done = env.step(action)
        print(next_state)
    """

    env.render()
    while True:
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
                    print(next_state)
                    env.render()

                    if done:
                        print("DONE")
                        env.reset()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass


def test_agent(env, agent_a, agent_b):
    env.reset()
    print("\nNow playing Kalaha!!")
    print(agent_a)
    print(agent_b)

    while True:
        print(env)  # print environment
        # env.render()  # render game states as window

        # time.sleep(.800)  # slow down

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
    """
    is_player_1_bot = input("is player 1 a bot? (y/n)").lower() == 'y'
    is_player_2_bot = input("is player 2 a bot? (y/n)").lower() == 'y'
    player_1_name = input("player 1 name: ")
    player_2_name = input("player 2 name: ")
    """

    env = KalahaEnv(n_pits=6, n_balls=4)
    agent_a = KalahaAgent(0, env.n_pits, env.n_balls, strategy="max_score")
    agent_b = KalahaAgent(1, env.n_pits, env.n_balls, strategy="playbook")
    test_agent(env, agent_a, agent_b)
    # play_game(env)
