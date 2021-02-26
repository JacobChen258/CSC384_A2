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
        # Question 4, your box evaluation solution goes here
        # Returns a numeric value evaluating the given state where the larger the better
        enemies_pos = state.get_enemies()
        switches = state.get_switches().items()
        boxes = state.get_boxes()[:]
        player_pos = state.get_player_position()
        player_box_distance = 0
        box_switch_distance = 0  # after getting a box
        enemy_player_distance = 0
        smallest_switch_distance = math.inf
        smallest_box_distance = math.inf
        smallest_enemy_distance = math.inf
        direction = None
        p_to_b = None
        b_to_s = None

        # Rank of the distance
        # 1.direction toward box is opposite of enemy direction (player_box)
        # 2.direction toward box is the same as enemy direction (enemy_player)

        #Agent should prioritize box to player distance until within close range of box
        #Once in range, agent should prioritize box to player to switch distance
        #If at any point, enemy agent gets to close to agent (maybe 1-2 spaces), switch
        #priority to evasion
        for switch in switches:
            if not switch[1]:  # not on
                for box in boxes:
                    if box == switch[0]:
                        boxes.remove(box)
                    else:
                        box_switch_distance = EvaluationFunctions.manhattan_heuristic(switch[0], box) + \
                                   EvaluationFunctions.manhattan_heuristic(box, player_pos)
                        player_box_distance = EvaluationFunctions.manhattan_heuristic(box, player_pos)

                        if smallest_switch_distance <= 0 or box_switch_distance < smallest_switch_distance:
                            smallest_switch_distance = box_switch_distance #player to box to switch
                            p_to_b = EvaluationFunctions.manhattan_axis_heuristic(switch[0], box)
                            b_to_s = EvaluationFunctions.manhattan_axis_heuristic(box, player_pos)
                            direction = (b_to_s[0] - p_to_b[0]), (b_to_s[1] - p_to_b[1])
                        if smallest_box_distance <= 0 or player_box_distance < smallest_box_distance:
                            smallest_box_distance = player_box_distance #player to box only
                            p_to_b = EvaluationFunctions.manhattan_axis_heuristic(switch[0], box)
                            b_to_s = EvaluationFunctions.manhattan_axis_heuristic(box, player_pos)
                            direction = (b_to_s[0] - p_to_b[0]), (b_to_s[1] - p_to_b[1])

        for enemy_pos in enemies_pos:
            enemy_player_distance = EvaluationFunctions.euclidean_heuristic(enemy_pos, player_pos) 
            if smallest_enemy_distance <= 0 or enemy_player_distance < smallest_enemy_distance:
                smallest_enemy_distance = enemy_player_distance #enemy to player only

        priority = EvaluationFunctions.assign_priority(smallest_switch_distance, smallest_box_distance, smallest_enemy_distance)

        if priority == 1:
            return 1/smallest_box_distance
        elif priority == 2:
            calc = ((direction[0] ** 2 + direction[1] ** 2) ** 0.5)
            if (calc != 0):
                return 1/calc
            else: 
                return 1/smallest_switch_distance 
        #priority 3
        #weighted_x = (smallest_switch_distance * 0.25 + smallest_enemy_distance * 0.75)
        return -1/smallest_enemy_distance    #weighted_x 

    @staticmethod
    def assign_priority(switch_dist, box_dist, enemy_dist):
        priority = 1 #1 means box priority only
        if box_dist < 2:
            priority = 2 #2 means player to box to switch
        if enemy_dist <= 2:
            priority = 3 #3 means evade enemy 
        return priority

    @staticmethod
    def points_evaluation(state):
        # Question 5, your points evaluation solution goes here
        # Returns a numeric value evaluating the given state where the larger the better
        raise NotImplementedError("Points Evaluation not implemented")
    
    @staticmethod
    def manhattan_axis_heuristic(p1, p2):
        return p1[0] - p2[0], p1[1] - p2[1]

    @staticmethod
    def manhattan_heuristic(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    @staticmethod
    def euclidean_heuristic(p1, p2):
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5
