#!/usr/bin/env python
import sys

import click

from gym_tictactoe.env import TicTacToeEnv, agent_by_mark, check_game_status,\
    after_action_state, tomark, next_mark


class HumanAgent(object):
    def __init__(self, mark):
        self.mark = mark

    def act(self, state, ava_actions):
        while True:
            uloc = input("Enter location[1-9], q for quit: ")
            if uloc.lower() == 'q':
                return None
            try:
                action = int(uloc) - 1
                if action not in ava_actions:
                    raise ValueError()
            except ValueError:
                print("Illegal location: '{}'".format(uloc))
            else:
                break

        return action

class MinimaxAgent(object):
    def __init__(self, mark):
        self.mark = mark

    #The actual minimax recursive function
    def minimax(self, state, depth, isMax, ava_actions):
        board, extra = state
        gameState = check_game_status(board)

        if gameState == 0:
            return 0
        elif gameState == 1:
            return 1
        elif gameState == 2:
            return -1

        if isMax:
            bestScore = -100000
            for i in range(0, 9, 1):
                if i in ava_actions:
                    statet = after_action_state(state, i)
                    ava_actions.remove(i) 
                    score = self.minimax(statet, depth + 1, False, ava_actions)
                    ava_actions.append(i)
                    bestScore = max(score, bestScore)

            return bestScore
        else:
            bestScore = 100000
            for i in range(0, 9, 1):
                if i in ava_actions:
                    statet = after_action_state(state, i)
                    ava_actions.remove(i)
                    score = self.minimax(statet, depth + 1, True, ava_actions)
                    ava_actions.append(i)
                    bestScore = min(score, bestScore)

            return bestScore
            

#   return the move in this function. ava_actions is an array containting the possible actions 
#   you might want to use after_action_state and check_game_status. Also look at env.py
#   state is a tuple with the first value indicating the board and second value indicating mark
#   proper use of inbuilt functions will avoid interacting with state
    def act(self, state, ava_actions):
        #raise NotImplementedError()
        
        bestScore = -100000
        bestMove = 1

        for i in range(0, 9, 1):
            if i in ava_actions:
                statet = after_action_state(state, i)
                ava_actions.remove(i)
                score = self.minimax(statet, 0, False, ava_actions)
                ava_actions.append(i)

                if score > bestScore:
                    bestScore = score
                    bestMove = i

        return bestMove


@click.command(help="Play minimax agent.")
@click.option('-n', '--show-number', is_flag=True, default=False,
              show_default=True, help="Show location number in the board.")
def play(show_number):
    env = TicTacToeEnv(show_number=show_number)
    agents = [MinimaxAgent('O'),
              HumanAgent('X')]
    episode = 0
    while True:
        state = env.reset()
        _, mark = state
        done = False
        env.render()
        while not done:
            agent = agent_by_mark(agents, mark)
            env.show_turn(True, mark)
            ava_actions = env.available_actions()
            action = agent.act(state, ava_actions)
            if action is None:
                sys.exit()

            state, reward, done, info = env.step(action)
        
            print('')
            env.render()
            if done:
                env.show_result(True, mark, reward)
                # board, temp = state
                # gameState = check_game_status(board)
                # print(gameState)
                break
            else:
                _, _ = state
            mark = next_mark(mark)

        episode += 1


if __name__ == '__main__':
    play()
