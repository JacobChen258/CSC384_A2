from state import *
from utils import *
import math


class GameTreeSearching:
    # You will also find that the GameStateHandler class (already imported) will help perform needed operations on the
    # the game states. To declare a GameStateHandler simply wrap it around a GameState like such,
    # handler = GameStateHandler(GameState) where GameState will be an instance of GameState.

    # Below is a list of helpful functions:
    # GameStateHandler.get_successors() --> returns successors of the handled state
    # GameStateHandler.get_agents() --> returns a list of the positions of the agents on the map
    # GameStateHandler.get_agent_count() --> returns the number of agents on the map
    # GameStateHandler.get_agent_actions(agent_pos) --> returns a list of the possible actions the given agent can take
    # GameStateHandler.get_successor(agent_pos, action) --> returns the successor state if the given agent took the given action
    # GameState.get_player_position() --> returns the players position in that game state as (row, col)
    # GameState.copy() --> returns a copy
    # GameState.is_win() --> returns True if the game state is a winning state
    # GameState.is_loss() --> returns True if the game state is a losing state

    # Hint:
    # To avoid unwanted issues with recursion and state manipulation you should work with a _copy_ of the state
    # instead of the original.

    @staticmethod
    def minimax_search(state, eval_fn, depth=2):
        # Question 1, your minimax search solution goes here
        # Returns a SINGLE action based off the results of the search
        num_agent = GameStateHandler(state.copy()).get_agent_count()
        best_move, value = GameTreeSearching.minimax_search_helper(state.copy(), eval_fn, depth, num_agent * depth)
        return best_move

    @staticmethod
    def minimax_search_helper(state, eval_fn, depth, count):
        best_move = None
        if not state.is_loss() and state.is_win():
            return best_move, eval_fn(state)
        elif count == 0:
            return best_move, eval_fn(state)
        handler, agents, num_agent, cur_index, cur_pos = GameTreeSearching.get_state_info(state, count)
        if cur_index == 0:
            strategy = 'Max'
            value = -math.inf
        else:
            strategy = 'Min'
            value = math.inf
        for action in handler.get_agent_actions(cur_pos):
            next_state = handler.get_successor(cur_pos, action)
            next_move, next_value = GameTreeSearching.minimax_search_helper(
                next_state.copy(), eval_fn, depth, count - 1)
            if strategy == 'Max' and next_value > value or strategy == 'Min' and value > next_value:
                best_move, value = action, next_value
        return best_move, value

    @staticmethod
    def alpha_beta_search(state, eval_fn, depth):
        # Question 2, your alpha beta pruning search solution goes here
        # Returns a SINGLE action based off the results of the search
        num_agent = GameStateHandler(state.copy()).get_agent_count()
        alpha = -math.inf
        beta = math.inf
        best_move, value = GameTreeSearching.alpha_beta_search_helper(
            state.copy(), eval_fn, depth, num_agent * depth, alpha, beta)
        return best_move

    @staticmethod
    def alpha_beta_search_helper(state, eval_fn, depth, count, alpha, beta):
        best_move = None
        if not state.is_loss() and state.is_win():
            return best_move, eval_fn(state)
        elif count == 0:
            return best_move, eval_fn(state)
        handler, agents, num_agent, cur_index, cur_pos = GameTreeSearching.get_state_info(state, count)
        if cur_index == 0:
            strategy = 'Max'
            value = -math.inf
        else:
            strategy = 'Min'
            value = math.inf
        for action in handler.get_agent_actions(cur_pos):
            next_state = handler.get_successor(cur_pos, action)
            next_move, next_value = GameTreeSearching.alpha_beta_search_helper(
                next_state.copy(), eval_fn, depth, count - 1, alpha, beta)
            if strategy == 'Max':
                if next_value > value:
                    best_move, value = action, next_value
                if value >= beta:
                    return best_move, value
                alpha = max(alpha, value)
            if strategy == 'Min':
                if next_value < value:
                    best_move, value = action, next_value
                if value <= alpha:
                    return best_move, value
                beta = min(beta, value)
        return best_move, value

    @staticmethod
    def expectimax_search(state, eval_fn, depth):
        # Question 3, your expectimax search solution goes here
        # Returns a SINGLE action based off the results of the search
        best_move, value = GameTreeSearching.expectimax_search_helper(
            state.copy(), eval_fn, depth,
            depth * GameStateHandler(state).get_agent_count())
        return best_move

    @staticmethod
    def expectimax_search_helper(state, eval_fn, depth, count):
        best_move = None
        if not state.is_loss() and state.is_win():
            return best_move, eval_fn(state)
        elif count == 0:
            return best_move, eval_fn(state)
        handler, agents, num_agent, cur_index, cur_pos = GameTreeSearching.get_state_info(state, count)
        if cur_index == 0:
            strategy = 'Max'
            value = -math.inf
        else:
            strategy = 'Chance'
            value = 0
        for action in handler.get_agent_actions(cur_pos):
            next_state = handler.get_successor(cur_pos, action)
            next_move, next_value = GameTreeSearching.expectimax_search_helper(
                next_state.copy(), eval_fn, depth, count - 1)
            if strategy == 'Max' and next_value > value:
                best_move, value = action, next_value
            if strategy == 'Chance':
                value += next_value / (len(handler.get_agent_actions(cur_pos)))
        return best_move, value

    @staticmethod
    def get_state_info(state, count):
        handler = GameStateHandler(state)
        agents = handler.get_agents()
        num_agent = handler.get_agent_count()
        cur_index = (num_agent - count % num_agent) % num_agent

        cur_pos = agents[cur_index]
        return handler, agents, num_agent, cur_index, cur_pos
