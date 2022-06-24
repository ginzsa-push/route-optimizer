import logging

from itertools import permutations

from model import Solution
from model import SwapInSameSequenceNeighbourhood
from model import ShiftInSameSequenceNeighbourhood
from model import RemoveSolutionNeighbourhood
from model import InsertUnusedNeighbourhood
from model import ReplaceWithUnusedNeighbourhood


logger = logging.getLogger()

def swap_in_same_sequence_v2(solution, jobs_to_ignore, width_a, width_b, sample_freq):
    neighbourhood = SwapInSameSequenceNeighbourhood(width_a, width_b, sample_freq)
    rs = neighbourhood.generate_neighbourhood(solution, list(jobs_to_ignore))
    return rs

def shift_in_the_same_sequence_v2(solution, tabu_set, width, sample_freq):
    neighbourhood = ShiftInSameSequenceNeighbourhood(width, sample_freq)
    rs = neighbourhood.generate_neighbourhood(solution, list(tabu_set))
    return rs

def remove_solution_neighbourhood_v2(solution, tabu_set):
    neighbourhood = RemoveSolutionNeighbourhood(1.)
    rs = neighbourhood.generate_neighbourhood(solution, tabu_set)
    return rs

def insert_unused_neighbourhood_v2(solution, tabu_set):
    neighbourhood = InsertUnusedNeighbourhood(1.)
    rs = neighbourhood.generate_neighbourhood(solution, tabu_set)
    return rs

def replace_unused_neighbourhood_v2(solution, tabu_set):
    neighbourhood = ReplaceWithUnusedNeighbourhood(1.)
    rs = neighbourhood.generate_neighbourhood(solution, tabu_set)
    return rs
'''
generate nighbouring solutions
'''
def collect_solution_neighbours(solution, tabu_set):
    logger.info('collect neighbours')
    freq = 1.0

    return swap_in_same_sequence_v2(solution, tabu_set, 1, 1, freq) + swap_in_same_sequence_v2(solution, tabu_set, 2, 1, freq) + swap_in_same_sequence_v2(solution, tabu_set, 2, 2, freq) + \
        shift_in_the_same_sequence_v2(solution, tabu_set, 1, freq) + shift_in_the_same_sequence_v2(solution, tabu_set, 2, freq) + shift_in_the_same_sequence_v2(solution, tabu_set, 3, freq) + \
        insert_unused_neighbourhood_v2(solution, tabu_set) + \
        remove_solution_neighbourhood_v2(solution, tabu_set) +\
        replace_unused_neighbourhood_v2(solution, tabu_set)

