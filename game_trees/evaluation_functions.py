from state import *
import math


# Here you will implement evaluation functions. Recall that weighing components of your
# evaluation differently can have positive effects on performance. For example, you could
# have your evaluation prioritize running away from opposing agents instead of activiating
# switches. Also remember that for values such as minimum distance to have a positive effect
# you should inverse the value as _larger_ evaluation values are better than smaller ones.

# Helpful Functions:
# You may define any helper functions you want in this file.
# GameState.get_enemies() --> returns a list of opposing agent positions.
# GameState.get_boxes() --> returns a list of (row, col) positions representing where the boxes are on the map
# GameState.get_switches() --> returns a dictionary where the keys are the locations of the switches as (row, col) and the value
#                              being True if the switch is on and False if off.
# GameState.get_player_position() --> returns the current position of the player in the form (row, col)
# GameState.get_remaining_points() --> returns a list of the positions of the remaining armory points of the map in the form (row, col) 

class EvaluationFunctions:

    @staticmethod
    def score_evaluation(state):
        return state.get_score()

    @staticmethod
    def box_evaluation(state):
        # Question 4, your box evaluation solution goes here
        # Returns a numeric value evaluating the given state where the larger the better
        raise NotImplementedError("Box Evaluation not implemented")

    @staticmethod
    def points_evaluation(state):
        # Question 5, your points evaluation solution goes here
        # Returns a numeric value evaluating the given state where the larger the better
        points_pos = state.get_remaining_points()
        enemies_pos = state.get_enemies()
        enemies_range = []
        player_pos = state.get_player_position()
        for enemy in enemies_pos:
            enemies_range.append((enemy[0] + 1, enemy[1]))
            enemies_range.append((enemy[0], enemy[1] + 1))
            enemies_range.append((enemy[0] - 1, enemy[1]))
            enemies_range.append((enemy[0], enemy[1] - 1))
        if player_pos in enemies_range:
            return -math.inf
        switch_pos = state.get_switches().keys()[0]
        score = 0
        cost = -2  # Cost of moving 1 unit
        points_reward = 25
        switch_reward = 550
        pts_dist = []  # List of points to switch distance with direction
        # list of (x,y). If x > 0, east. If y > 0, north
        ptp_dist = []  # List of player to points distance with direction
        for point in points_pos:
            pts_dist.append((switch_pos[1] - point[1], point[0] - switch_pos[0]))
            ptp_dist.append((point[1] - player_pos[1], player_pos[0] - point[0]))
        for i in range(len(pts_dist)):
            if pts_dist[i][0] * ptp_dist[i][0] < 0 or pts_dist[i][1] * ptp_dist[i][1] < 0:
                # If player to point and point to switch are at opposite direction,
                # partial cost is doubled
                cur_cost = EvaluationFunctions.manhattan_origin_heuristic(pts_dist[i]) * cost + \
                            EvaluationFunctions.manhattan_origin_heuristic(ptp_dist[i]) * cost * 2

            else:
                cur_cost = EvaluationFunctions.manhattan_origin_heuristic(pts_dist[i]) * cost + \
                            EvaluationFunctions.manhattan_origin_heuristic(ptp_dist[i]) * cost
            cur_score = points_reward + cur_cost + switch_reward
            score = max(score, cur_score)
        return score

    @staticmethod
    def composition_points(pos, pts_dist, comp_score):
        return 0

    @staticmethod
    def manhattan_origin_heuristic(p1):
      return EvaluationFunctions.manhattan_heuristic((0, 0), p1)

    @staticmethod
    def manhattan_heuristic(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
