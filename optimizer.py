import logging
import sys
import collections

from model import Solution
from validation import validate_solution
from fitness import calculate_fitness
from candidates import create_canditate_list, build_solution_candidate
from neighbourhood import collect_solution_neighbours
from distances import Distances


logger = logging.getLogger()
logger.level = logging.INFO
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

class Optimizer:
    def __init__(self, *args, **kwargs):
        self.distances = Distances(distances=kwargs.get('matrix', None))
        self.jobs = kwargs.get('jobs', None)
        self.teams = kwargs.get('teams', None)
        self.config = kwargs.get('config', None)

    def optimize(self):
        logger.info('optimizing ...')
        tabu_queue = collections.deque([], self.config['tabu_size']) # queue size
        best_solution = Solution(self.jobs, self.teams)
        
        # candidates
        candidate_store = create_canditate_list(self.config, self.distances, best_solution)
        logger.info('candidate list created ... {}'.format(candidate_store.size()))

        # once we get the candidate list, build a solution with a jobs sequence
        build_solution_candidate(candidate_store, best_solution)

        best_fitness = self.evaluate(best_solution)
        logger.info('original fitness: {}'.format(best_fitness))

        current_solution = best_solution

        # loop through n iterations
        for n in range(0, self.config['iterations']):
            logger.info('iteration no: {}'.format(n))

            # get current solution neighbours (pass tabu set)
            neighbourhood = collect_solution_neighbours(best_solution, set(tabu_queue))

            logger.info('neighbour solutions no: {}'.format(len(neighbourhood)))

            # loop through solution candidates and evaluate fitness
            best_in_iteration = - sys.float_info.max
            for neighbour_solution in neighbourhood:

                 # best solution remains
                f = self.evaluate(neighbour_solution)
                if f >= best_in_iteration:
                    best_in_iteration = f
                    current_solution = neighbour_solution

                if f > best_fitness:
                    best_solution = neighbour_solution
                    best_fitness = f
                    logger.info('better: {}'.format(best_fitness))

            logger.info('best in iteration neghbourhood is: {}'.format(best_in_iteration))

            # tabu list
            tabu_queue.extendleft(current_solution.affected_jobs)
            # reapair solution
            current_solution = self.repair_solution(current_solution)

        logger.info('best: {}'.format(best_fitness))
        return { 'solution': best_solution, 'fitness': best_fitness}

    '''
    return solution fitness
    '''
    def evaluate(self, solution):
        valid = validate_solution(self.distances, solution)
        if not valid:
            return - sys.float_info.max

        return calculate_fitness(self.config, self.distances, solution)

    '''
    repair the unfulfilled in solutions
    '''
    def repair_solution(self, solution):
        cloned_solution = solution.clone() # no stats in it
        jobs_fulfilled = cloned_solution.collect_all_jobs()
        for job in self.jobs:
            if job not in jobs_fulfilled and job[0] not in cloned_solution.unfulfilled.keys():
                cloned_solution.unfulfilled[job[0]] = job[1]
            elif job in jobs_fulfilled and job[0] in cloned_solution.unfulfilled.keys():
                del cloned_solution.unfulfilled[job[0]]
        
        return cloned_solution



