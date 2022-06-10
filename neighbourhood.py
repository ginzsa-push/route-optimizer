import logging

from itertools import permutations

from model import Solution


logger = logging.getLogger()
'''
filter only with two shared position
'''
def filter_only_two_places(seq, l):
    if len(seq) != len(l):
        return False

    count = 0
    for idx, _ in enumerate(seq):    
        if seq[idx] != l[idx]:
            count += 1

    return count == 2

# implementation using permutation generation
# keep it we might use this approach
def swap_in_same_sequence(solution, jobs_to_ignore):

    solutions = [] 
    # iterate through team jobs
    for team in solution.teams:
        j = solution.get_job_seq_at(team.id)

        logger.debug('get job sequence jobs: {}'.format(j))
        seq = j.jobs_seq.jobs

        logger.debug('get seq: {}'.format(seq))
        # filter out jobs in jobs_to_ignore
        seq = [x for x in seq if x not in jobs_to_ignore]
        logger.debug('filtered seq: {}'.format(seq))

        prmttns = list(permutations(seq, len(seq)))
        logger.debug('permutations: {}'.format(prmttns))
 
        prmttns =  [p for p in prmttns if filter_only_two_places(seq, p)]
        logger.debug('filtered permutations: {}'.format(prmttns))
    
        for p_job in prmttns:
            new_solution = Solution(list(p_job), solution.teams)
            # add solution to the team
            for jb in p_job:
                new_solution.add_job(jb, team.id)

            # copy the same job values from other team different to team.id
            for another_team in solution.teams:
                if another_team.id != team.id:
                    
                    in_jobs = solution.get_job_seq_at( another_team.id).jobs_seq.jobs
                    for in_job in in_jobs:
                        new_solution.add_job(in_job,  another_team.id)

            solutions.append(new_solution)

    return solutions



# implementation using list insert, this will shift the index position
# of other values
def shift_in_same_sequence(solution, jobs_to_ignore, width):

    logger.info("shift in same sequence ...")
    solutions = [] 
    for team in solution.teams:
        j = solution.get_job_seq_at(team.id)

        logger.debug('get job sequence jobs: {}'.format(j))
        seq = j.jobs_seq.jobs

        logger.debug('get seq: {}'.format(seq))
       
        for ia, va in enumerate(seq):
            # filter out jobs in jobs_to_ignore
            if va in jobs_to_ignore:
                continue
            for ib, _ in enumerate(seq):
                
                if ib >= ia and ib < (ia + width):
                    continue
                if ib == (ia - width):
                    continue
                else:
                    new_seq, affected = reinsert(seq, ia, ib)
                    new_solution = Solution(list(new_seq), solution.teams)

                    new_solution.affected_jobs.append(affected)
                    ######
                    # add solution to the team
                    for jb in new_seq:
                        new_solution.add_job(jb, team.id)

                    # copy the same job values from other team different to team.id
                    for another_team in solution.teams:
                        if another_team.id != team.id:
                            in_jobs = solution.get_job_seq_at(another_team.id).jobs_seq.jobs
                            for in_job in in_jobs:
                                new_solution.add_job(in_job, another_team.id)
                    #####
                    solutions.append(new_solution)

    return solutions


# implementation using list swap values for a given index
# (use this)
def swap_in_same_sequence_1(solution, jobs_to_ignore, width):
    logger.info("swap in same sequence ...")
    solutions = [] 
    for team in solution.teams:
        j = solution.get_job_seq_at(team.id)

        logger.debug('get job sequence jobs: {}'.format(j))
        seq = j.jobs_seq.jobs

        # filter out jobs in jobs_to_ignore
        seq = [x for x in seq if x not in jobs_to_ignore]

        logger.debug('get seq: {}'.format(seq))
       
        for ia, va in enumerate(seq):
            # filter out jobs in jobs_to_ignore
            if va in jobs_to_ignore:
                continue
            for ib, _ in enumerate(seq):
                
                # avoid
                if (ia >= ib and ia < (ib + width)) or (ib >= ia and ib < (ia + width)):
                    continue
                if ia > ib:
                    continue
                else:
                    new_seq, affected = swapvalues(seq, ia, ib)
                    new_solution = Solution(list(new_seq), solution.teams)
                    new_solution.affected_jobs.append(affected)
                    
                    # add solution to the team
                    for jb in new_seq:
                        new_solution.add_job(jb, team.id)

                    # copy the same job values from other team different to team.id
                    for other_team in solution.teams:
                        if other_team.id != team.id:
                            in_jobs = solution.get_job_seq_at(other_team.id).jobs_seq.jobs
                            for in_job in in_jobs:
                                new_solution.add_job(in_job, team.id)
                    #####
                    solutions.append(new_solution)

    return solutions

''' 
reinsert in a given list 'l' 
from ('frm') position to position ('to')
This will shift the other values to different idx positions
'''
def reinsert(l, frm, to):
     ll = list(l)
     affected = ll[frm]
     del ll[frm]
     ll.insert(to, affected)
     return ll, affected


''' 
swapvalues in a given list 'l' 
from ('frm') position to position ('to')
This will swap the other values to different idx positions
'''
def swapvalues(l, frm, to):
     ll = list(l)
     affected = ll[frm]
     ll[frm], ll[to] = ll[to], ll[frm]
     return ll, affected     

def remove_solution_neighbourhood(solution, jobs_to_ignore):

    logger.info("remove in solution ...")
    solutions = [] 

    for team in solution.teams:
        j = solution.get_job_seq_at(team.id)

        logger.debug('get job sequence jobs: {}'.format(j))
        seq = j.jobs_seq.jobs

        # filter out jobs in jobs_to_ignore
        seq = [x for x in seq if x not in jobs_to_ignore]
        for i, _ in enumerate(seq):
            
            # delete job from sequence
            copy_seq = list(seq)
            affected = copy_seq[i]
            del copy_seq[i]

            new_solution = Solution(copy_seq, solution.teams)
            new_solution.affected_jobs.append(affected)

            # add job to the team
            for jb in copy_seq:
                new_solution.add_job(jb, team.id)

            # copy the same job values from other team different to team.id
            for another_team in solution.teams:
                if another_team.id != team.id:
                    in_jobs = solution.get_job_seq_at(another_team.id).jobs_seq.jobs
                    for in_job in in_jobs:
                        new_solution.add_job(in_job, another_team.id)

            solutions.append(new_solution)

    return solutions

#
def insert_unused_neighbourhood(solution, jobs_to_ignore):
    logger.info("insert unused  ...")
    solutions = [] 
    
    for jb in solution.unfulfilled.items():

        if jb not in jobs_to_ignore:

            for team in solution.teams:
                j = solution.get_job_seq_at(team.id)

                logger.debug('get job sequence jobs: {}'.format(j))
                seq = j.jobs_seq.jobs
                
                for index in range(0, len(seq) + 1):
                    new_seq = list(seq)
                    new_seq.insert(index, jb)
                    new_solution = Solution(new_seq, solution.teams)
                    new_solution.affected_jobs.append(jb)

                    for job in new_seq:
                        new_solution.add_job(job, team.id)

                    solutions.append(new_solution)

    return solutions


def replace_with_unused_neighbourhood(solution, jobs_to_ignore):

    logger.info("replace with unused ...")
    solutions = [] 
    for jb in solution.unfulfilled.items():

        # avoid unfulfilled jobs in 'to_ignore' list
        if jb not in jobs_to_ignore:

            for team in solution.teams:
                j = solution.get_job_seq_at(team.id)

                logger.debug('get job sequence jobs: {}'.format(j))
                seq = j.jobs_seq.jobs           

                for index in range(0, len(seq)):
                    new_seq = list(seq)
                    # only replace jobs not in 'to_ignore' list
                    if new_seq[index] not in jobs_to_ignore:
                        new_seq[index] = jb
                        new_solution = Solution(new_seq, solution.teams)
                        new_solution.affected_jobs.append(jb)
                        
                        for job in new_seq:
                            new_solution.add_job(job, team.id)

                        solutions.append(new_solution)
    return solutions

'''
generate nighbouring solutions
'''
def collect_solution_neighbours(solution, tabu_set):
    logger.info('collect neighbours')
    return swap_in_same_sequence_1(solution, tabu_set, 1) + swap_in_same_sequence_1(solution, tabu_set, 2) + \
        shift_in_same_sequence(solution, tabu_set, 1) + shift_in_same_sequence(solution, tabu_set, 2) + shift_in_same_sequence(solution, tabu_set, 3) + \
        remove_solution_neighbourhood(solution, tabu_set) + \
        insert_unused_neighbourhood(solution, tabu_set) + \
        replace_with_unused_neighbourhood(solution, tabu_set)
