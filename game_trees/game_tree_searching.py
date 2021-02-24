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
        best_move, value = GameTreeSearching.minimax_search_helper(state.copy(),eval_fn, depth , 0)
        return best_move

    @staticmethod
    def minimax_search_helper(state, eval_fn, depth, count):
        best_move = None
        if state.is_win():
            return best_move, eval_fn(state)
        elif depth <= 0:
            return best_move, eval_fn(state)
        handler = GameStateHandler(state)
        agents = handler.get_agents()
        num_agent = handler.get_agent_count()
        if count == 0:
            strategy = 'Max'
            value = -math.inf
        else:
            strategy = 'Min'
            value = math.inf
        cur_pos = agents[count]
        # print(handler.get_agent_actions(cur_pos))
        for action in handler.get_agent_actions(cur_pos):
            if action != Direction.STOP:
                next_state = handler.get_successor(cur_pos, action)
                if count == num_agent - 1:
                    count = 0
                    depth -= 1
                else:
                    count += 1
                next_move, next_value = GameTreeSearching.minimax_search_helper(next_state, eval_fn, depth, count)
                if strategy == 'Max' and value < next_value:
                    best_move, value = action, next_value
                if strategy == 'Min' and value > next_value:
                    best_move, value = action, next_value
        return best_move, value

    '''

  def minimax_search_helper(state,best_move,eval_fn, depth):
      handler = GameStateHandler(state)
      agents = handler.get_agents()
      if state.is_win():
          return (best_move, eval_fn(state))
      elif depth == 0:
          return (best_move, eval_fn(state))
      for agent_pos in agents:
          cur_pos = agent_pos
          if cur_pos == state.get_player_position():
              strategy = 'Max'
              value = -math.inf
          else:
              strategy = 'Min'
              value = math.inf
          for action in handler.get_agent_actions(cur_pos):
              if action != Direction.STOP:
                  next_state = handler.get_successor(cur_pos, action)
                  next_step = GameTreeSearching.minimax_search_helper(next_state, best_move, eval_fn, depth - 1)
                  if strategy == 'Max' and next_step[1] > value:
                      value = next_step[1]
                      print(value)
                      best_move = action
                  if strategy == 'Min' and next_step[1] < value:
                      value = next_step[1]
                      best_move = action
      return next_step
  '''

    '''
  def minimax_search_helper(state, eval_fn, depth):
      best_move = None
      if state.is_win():
          return best_move, eval_fn(state)
      elif depth == 0:
          return best_move, eval_fn(state)
      handler = GameStateHandler(state)
      agents = handler.get_agents()
      for agent_pos in agents:
          cur_pos = agent_pos
          if cur_pos == state.get_player_position():
              strategy = 'Max'
              value = -math.inf
          else:
              strategy = 'Min'
              value = math.inf
          for action in handler.get_agent_actions(cur_pos):
              next_state = handler.get_successor(cur_pos, action)
              next_move, next_value = GameTreeSearching.minimax_search(next_state, eval_fn, depth - 1)
              if strategy == 'Max' and value < next_value:
                  best_move, value = next_move, next_value
              if strategy == 'Min' and value > next_value:
                  best_move, value = next_move, next_value
      return best_move, value
      '''

    @staticmethod
    def alpha_beta_search(state, eval_fn, depth):
        # Question 2, your alpha beta pruning search solution goes here
        # Returns a SINGLE action based off the results of the search
        raise NotImplementedError("Alpha Beta Pruning search not implemented")

    @staticmethod
    def expectimax_search(state, eval_fn, depth):
        # Question 3, your expectimax search solution goes here
        # Returns a SINGLE action based off the results of the search
        raise NotImplementedError("Expectimax search not implemented")
