import pygame


class KalahaEnv(object):
    """
    Environment for Kalaha

    Observation space: [PR6 - PR0, PL6 - PL0]
    Player Left 0 is a goal
    Player Right 0 is a goal

    Action space: [6-1]

    """

    def __init__(self, n_pits=6, n_balls=4, n_players=2):
        self.n_pits = n_pits
        self.n_balls = n_balls
        self.n_players = n_players

        self.total_balls = self.n_pits * n_players * n_balls
        print("total_balls", self.total_balls)
        self.total_pits = (self.n_pits + 1) * n_players

        self.current_step = None
        self.current_state = None
        self.current_player = None

        # render variables
        # os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.font.init()
        self.font = pygame.font.SysFont('Ariel', 30)
        self.screen = None

        self.reset()

    def __repr__(self):
        return "player: {}, state: {}".format(self.current_player, self.current_state)

    def reset(self):
        """ Reset states """
        self.current_step = 0
        self.current_state = [0, 4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4]
        # self.current_state = [0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 1]
        self.current_player = 0
        return self.current_state

    def step(self, action):
        """ Next step in time """
        self.current_step += 1

        next_state, next_player = self.eval_action(self.current_state, self.current_player, action)
        self.current_state = next_state
        self.current_player = next_player

        reward = self.get_reward()

        opponent_target_index = self.get_target_index((self.current_player + 1) % 2)
        player_target_index = self.get_target_index(self.current_player)

        score_a = self.current_state[player_target_index]
        score_b = self.current_state[opponent_target_index]
        diff_player_balls = abs(score_a - score_b)
        total_board_balls = self.total_balls - (score_a + score_b)
        done = diff_player_balls > total_board_balls or total_board_balls == 1

        return self.current_state, reward, done

    @staticmethod
    def eval_action(state, player_index, action):
        if str(action) not in "123456":
            raise IndexError


        n_players = 2
        n_pits = (len(state) - n_players) / n_players
        total_pits = len(state)

        # make passed state non-mutable
        state = state.copy()
        player_index = player_index + 0

        # convert action to state index
        action_index = action + player_index * 7

        # pick up balls
        balls = state[action_index]
        state[action_index] = 0

        player_target_index = KalahaEnv.target_index(player_index, n_pits)
        enemy_index = (player_index + 1) % n_players
        enemy_target_index = KalahaEnv.target_index(enemy_index, n_pits)

        last_drop_index = -1
        skip = 0
        for i in range(balls):
            drop_index = (action_index - i - 1) % total_pits
            if drop_index == enemy_target_index:
                skip = 1
            drop_index = (drop_index - skip) % total_pits
            # print("drop_index:",drop_index)

            last_drop_index = drop_index
            state[drop_index] += 1 if drop_index >= 0 else 0

        if player_target_index != last_drop_index:  # if didn't hit target switch turn
            player_index = (player_index + 1) % 2

        # return new state and last_drop_index
        return state, player_index

    @staticmethod
    def target_index(player_index, n_pits):
        return player_index * (n_pits + 1)

    def get_target_index(self, player_index):
        return KalahaEnv.target_index(player_index, self.n_pits)

    def get_reward(self):
        return 0

    def render(self):
        if self.screen is None: self.screen = pygame.display.set_mode((1000, 400))

        self.screen.fill((200, 200, 200))

        player_colors = [(255, 0, 100), (0, 100, 255)]
        scale = 3
        h_space = 35 * scale
        v_space = 40 * scale
        pit_size = 10 * scale

        current_player_text = self.font.render('current_player: {}'.format(self.current_player), False,
                                               player_colors[self.current_player])
        self.screen.blit(current_player_text, (int(h_space / (scale * 2)), int(v_space / (scale * 2))))

        for i in range(0, 2):

            extra_h_space = i * 7 * h_space
            extra_v_space = int(v_space / 2 - v_space * i)
            player_pit_x = h_space + extra_h_space
            player_pit_y = v_space + i * v_space + extra_v_space

            pygame.draw.circle(self.screen, player_colors[i], [player_pit_x, player_pit_y], pit_size)

            target_balls = self.current_state[self.get_target_index(i)]
            target_ball_text = self.font.render('{}'.format(target_balls), False, (0, 0, 0))
            self.screen.blit(target_ball_text, (player_pit_x - 10, player_pit_y - 10))

            for j in range(1, 7):

                pit_x = (j + 1) * h_space
                pit_y = v_space + i * v_space
                pit_number_y = pit_y - 60 if i == 0 else pit_y + 40
                if i == 1:  # invert for player 1
                    pit_x = ((6 + 3) * h_space) - pit_x

                pygame.draw.circle(self.screen, player_colors[i], [pit_x, pit_y], pit_size)

                ball_count = self.current_state[i * 7 + j]
                ball_count_text = self.font.render('{}'.format(ball_count), False, (0, 0, 0))
                self.screen.blit(ball_count_text, (pit_x - 10, pit_y - 10))

                pit_number = j
                pit_number_text = self.font.render('{}'.format(pit_number), False, (0, 0, 0))
                self.screen.blit(pit_number_text, (pit_x - 10, pit_number_y))

        pygame.display.flip()
