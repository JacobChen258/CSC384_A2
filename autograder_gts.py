import random
from argparse import ArgumentParser
from simulator import Simulator
from state import *
from game_trees import *
from agents import GenericAgent
from grade_helpers_gts import load_test, convert_answer
import signal

SCALE_FACTOR = 15 # DO NOT ALTER
WAIT_TIME = 0.2
VERBOSE = False

# Dan's Tools
def run_tree_search(agent, maps, solution, trace_visited, trace_seen):
  # Dan's Changes for his testing
  GameStateHandler.trace_visited=[]
  GameStateHandler.trace_seen=[]

  sim = Simulator(maps[0], WAIT_TIME) # For these tests we deal with load exactly one map
  sim.verbose(VERBOSE)
  answer = sim.simulate_generic_agent(agent)

  final_solution_bool=convert_answer(answer) == solution
  visited_bool=str(GameStateHandler.trace_visited) == trace_visited or trace_visited[0] != "["
  seen_bool=str(GameStateHandler.trace_seen) == trace_seen or trace_visited[0] != "["

  # return final_solution_bool and visited_bool and seen_bool


  # total = int(visited_bool)/2 + int(seen_bool)/2
  # total = int(final_solution_bool)/3 + int(visited_bool)/3 + int(seen_bool)/3
  total = int(final_solution_bool)/2 + int(visited_bool)/4 + int(seen_bool)/4

  return total


# def run_tree_search(agent, maps, solution):
#
#   sim = Simulator(maps[0], WAIT_TIME) # For these tests we deal with load exactly one map
#   sim.verbose(VERBOSE)
#   answer = sim.simulate_generic_agent(agent)
#   final_solution_bool=convert_answer(answer) == solution
#   return final_solution_bool, convert_answer(answer)

def test(tests, tester):

  def signal_handler(signum, frame):
    raise Exception("Timed out!")

  total_marks, earned_marks = 0, 0

  for test in tests:
    # Dan's Tools
    name, maps, seed, solution, trace_visited, trace_seen  = load_test(test)
    # name, maps, seed, solution  = load_test(test)

    total_marks += 1
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(60)

    try:
      # Run the test
      random.seed(seed)

      # Dan's Tools
      result = tester(maps, solution, trace_visited, trace_seen)
      # result, solution = tester(maps, solution)

      earned = result
      print("Testing: {}\t [{}/{}]".format(name, earned, 1))

      # Dan's Tools
      # print("trace_visited")
      # print(str(GameStateHandler.trace_visited))
      # print("trace_seen")
      # print(str(GameStateHandler.trace_seen))
      # print("solution")
      # print(solution)

      earned_marks += earned

    except NotImplementedError as e:
      print("Testing: {}\t [{}]\t [0/1]".format(name, e))
    except TimeoutError:
      print("Testing: {}\t [Timed Out]\t [0/1]".format(name))
    except Exception as e:
      print(
            "Testing: {}\t [Raised an Exception: {}]\t [0/1]".format(name, e))

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
  print("------ Question 1 ------")
  e, t = test(["minimax/complex_map", "minimax/small_map", "minimax/medium_map", "minimax/test-1_map", "minimax/test-2_map", "minimax/test-3_map", "minimax/test-4_map", "minimax/test-5_map"], lambda maps, solution, visited, seen :
              run_tree_search(GenericAgent(GameTreeSearching.minimax_search, EvaluationFunctions.score_evaluation), maps, solution, visited, seen))
  total_marks += t
  earned_marks += e



  print("------ Question 2 ------")
  e, t = test(["alpha_beta/small_map", "alpha_beta/medium_map", "alpha_beta/medium_map_2", "alpha_beta/complex_map", "alpha_beta/test-1_map", "alpha_beta/test-2_map", "alpha_beta/test-3_map", "alpha_beta/test-4_map", "alpha_beta/test-5_map"], lambda maps, solution, visited, seen :
              run_tree_search(GenericAgent(GameTreeSearching.alpha_beta_search, EvaluationFunctions.score_evaluation), maps, solution, visited, seen))
  total_marks += t
  earned_marks += e


  print("------ Question 3 ------")
  e, t = test(["expectimax/small_map", "expectimax/medium_map", "expectimax/medium_map_2", "expectimax/complex_map", "expectimax/test-1_map", "expectimax/test-2_map", "expectimax/test-3_map", "expectimax/test-4_map", "expectimax/test-5_map"], lambda maps, solution, visited, seen :
              run_tree_search(GenericAgent(GameTreeSearching.expectimax_search, EvaluationFunctions.score_evaluation), maps, solution, visited, seen))
  total_marks += t
  earned_marks += e


  # DAN'S RECORDING TOOL
  # e, t = test(["expectimax/test-5_map"], lambda maps, solution:
  #             run_tree_search(GenericAgent(GameTreeSearching.expectimax_search, EvaluationFunctions.score_evaluation), maps, solution))
  # total_marks += t
  # earned_marks += e


  # ORIGINAL
  # print("------ Question 1 ------")
  # e, t = test(["minimax/complex_map", "minimax/small_map", "minimax/medium_map", "minimax/medium_map_2"], lambda maps, solution :
  #             run_tree_search(GenericAgent(GameTreeSearching.minimax_search, EvaluationFunctions.score_evaluation), maps, solution))
  # total_marks += t
  # earned_marks += e
  #
  # print("------ Question 2 ------")
  # e, t = test(["alpha_beta/small_map", "alpha_beta/medium_map", "alpha_beta/medium_map_2", "alpha_beta/complex_map"], lambda maps, solution :
  #             run_tree_search(GenericAgent(GameTreeSearching.alpha_beta_search, EvaluationFunctions.score_evaluation), maps, solution))
  # total_marks += t
  # earned_marks += e
  #
  # print("------ Question 3 ------")
  # e, t = test(["expectimax/small_map", "expectimax/medium_map", "expectimax/medium_map_2", "expectimax/complex_map"], lambda maps, solution :
  #             run_tree_search(GenericAgent(GameTreeSearching.expectimax_search, EvaluationFunctions.score_evaluation), maps, solution))
  # total_marks += t
  # earned_marks += e\


  print("\n\nTotal Grade - GTS: {}/{}".format(earned_marks, total_marks))
