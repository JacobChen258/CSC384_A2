import random
from argparse import ArgumentParser
from simulator import Simulator
from state import *
from game_trees import *
from agents import GenericAgent
from grade_helpers_ef import load_test, convert_answer
import signal

SCALE_FACTOR = 15 # DO NOT ALTER
WAIT_TIME = 0.2
VERBOSE = False

def basic_evaluation(eval_fn, maps, solution):
  # Here maps will > 1 maps to be compared to via the given eval_fn
  states = [(m, GameState(m)) for m in maps]
  return evaluate(eval_fn, states, solution)

def evaluate(eval_fn, states, solution):
  # Compare them via the eval function
  winner = ("none", 0.0)
  for map_name, state in states:
    state_eval = eval_fn(state)
    if state_eval >= winner[1]:
      winner = (map_name, state_eval)

  return winner[0] == solution
  # return True, winner[0]

# This is to help test points evaluation more in depth
def boot_evaluation(eval_fn, maps, solution):
  # Just give the player the 'heavy boots' ability off the bat
  states = [(m, GameState(m)) for m in maps]
  for _, state in states:
    state.update_obtained_points(5)

  return evaluate(eval_fn, states, solution)

def test(tests, tester):
  total_marks, earned_marks = 0, 0

  for test in tests:
    name, maps, seed, solution  = load_test(test)

    total_marks += 1

    try:
      # Run the test
      random.seed(seed)

      result = tester(maps, solution)
      # result, answer = tester(maps, solution)
      #
      # print("Solution:")
      # print(answer)

      earned = int(result)
      print("Testing: {}\t [{}/{}]".format(name, earned, 1))

      earned_marks += earned

    except Exception as e:
      print("Testing {}\t [{}]\t [0/1]".format(name, e))

  return earned_marks, total_marks

if __name__ == "__main__":
  parser = ArgumentParser(description = "Running Autograder for Assignment 2")
  parser.add_argument("-v", "--verbose", help = "Displays the actions the agent is taking during the simulation",
                      required = False, default = "")
  parser.add_argument("-w", "--waitTime", type = float,
                      help = "How long the simulation waits before taking another action", required = False, default=0.1)

  # Setting up based on arguments
  args = parser.parse_args()
  VERBOSE = args.verbose
  if args.waitTime :
    WAIT_TIME = args.waitTime

  # Start the tests
  total_marks, earned_marks = 0, 0

  # Dan's New Autograder Tests
  print("------ Question 4 ------")
  e, t = test(["evaluation/box_no_enemies_test", "evaluation/box_enemy_test", "evaluation/multi_box_test", "evaluation/box_point_test", "evaluation/multi_box_point_test"],
              lambda maps, solution : basic_evaluation(EvaluationFunctions.box_evaluation, maps, solution))
  total_marks += t
  earned_marks += e

  print("------ Question 5 ------")
  e, t = test(["evaluation/points_no_enemies_test", "evaluation/points_enemy_test", "evaluation/points_box_test", "evaluation/enemy_range_test", "evaluation/point_route_test"],
              lambda maps, solution : basic_evaluation(EvaluationFunctions.points_evaluation, maps, solution))
  total_marks += t
  earned_marks += e

  e, t = test(["evaluation/points_vs_switch_test", "evaluation/points_vs_switch_vs_enemy_test"],
              lambda maps, solution : boot_evaluation(EvaluationFunctions.points_evaluation, maps, solution))
  total_marks += t
  earned_marks += e


  # ORIGINAL
  # print("------ Question 4 ------")
  # e, t = test(["evaluation/box_no_enemies_test", "evaluation/box_enemy_test", "evaluation/multi_box_test", "evaluation/box_point_test"],
  #             lambda maps, solution : basic_evaluation(EvaluationFunctions.box_evaluation, maps, solution))
  # total_marks += t
  # earned_marks += e
  #
  # print("------ Question 5 ------")
  # e, t = test(["evaluation/points_no_enemies_test", "evaluation/points_enemy_test", "evaluation/points_box_test"],
  #             lambda maps, solution : basic_evaluation(EvaluationFunctions.points_evaluation, maps, solution))
  # total_marks += t
  # earned_marks += e
  #
  # e, t = test(["evaluation/points_vs_switch_test"],
  #             lambda maps, solution : boot_evaluation(EvaluationFunctions.points_evaluation, maps, solution))
  # total_marks += t
  # earned_marks += e

  print("\n\nTotal Grade - EF: {}/{}".format(earned_marks, total_marks))
