
import logging

import pandas as pd
from validation import is_cadidate_valid
from fitness import calculate_jobs_fitness
from utils import clone_pre_post_jobs, clone_pre_post_to_jobs
from model import JobsSequence

logger = logging.getLogger()

'''
create candidate list from solution
'''
def create_canditate_list(config, distances, best_solution):
    logger.info('creating initial candidate list ...')
    # candidates
    candidates = []
    # for each team 
    for i, team in enumerate(best_solution.teams):
        add_to_canditate_list(config, distances, candidates, best_solution.unfulfilled, best_solution.team_jobs[i].jobs_seq, team, i)
        
    return candidates

'''
add to candidates list for team's job sequence 
'''
def add_to_canditate_list(config, distances, candidates, unfulfilled, job_seq, team, team_idx):
    
    count = 0
    reject_after_count = 30

    # for each job unfulfilled in best solution
    for idx, j in enumerate(unfulfilled.items()):
        # put jobs in different index positions in the job sequence
        for position in range(0, len(job_seq.jobs) + 1):
            
             # the j job will be temporarely added (post) to the job sequence for 'ahead' validations
            pre, post = clone_pre_post_to_jobs(position, job_seq.jobs, j)
            
            # post addition job sequence
            post_job_seq = JobsSequence(jobs=post, start=job_seq.start, end=job_seq.end)
            # comply with validations : 
            if not is_cadidate_valid(distances, post_job_seq, team):
                logger.info('temp job not valid: {}'.format(j))

                # reject after 100 consecutive rejections TODO review this
                count += 1
                if count > reject_after_count:
                    logger.info('{} rejected candidates, reject {}'.format(reject_after_count, len(candidates)))
                    return
                continue
            else:
                count = 0
                # calculate fitness
                fitness = calculate_jobs_fitness(config, distances, post, team) - calculate_jobs_fitness(config, distances, pre, team)
                # if fitness is valid (assumed valid)
                    # create candidate
                    # add candidate to a list of "moves" candidates sorted by best fit
                candidates.append([team_idx,  idx, j[0], j[1], fitness])

'''
use pandas to sort candidates
'''
def candidate_dataframe_sort_by_fitness_desc(candidates):
    df = pd.DataFrame(candidates, columns=['team_idx', 'job_idx', 'dock_id', 'bikes', 'fitness'])
    df = df.sort_values(by='fitness', ascending=False)
    return df

'''
get best candidate
'''
def get_best_candidate(candidates):
    df = candidate_dataframe_sort_by_fitness_desc(candidates)
    candidate = df.head(1).values.tolist()[0]
    # delete head 1
    df = df.drop(df.index[0])
    # delete candidates with the same job dock
    df = df.drop(df[(df['dock_id'] == candidate[2] ) & (df['bikes'] == candidate[3]) & (df['team_idx'] == candidate[0])].index)
    # drop duplicates
    df = df.drop_duplicates()
    candidates =  df.values.tolist() # candidate deleted from list
    return candidate, candidates

'''
apply candidate to solution
'''
def apply_candidate(solution, candidate):
    # [team_idx,  idx, j[0], j[1], fitness]
    #logger.info('unfulfilled: {}'.format(len(solution.unfulfilled)))
    job = (candidate[2], candidate[3])
    team_idx = candidate[0]
    job_seq_idx = candidate[1]

    solution.add_job(job, team_idx, job_seq_idx=job_seq_idx)


'''
extract candidates for each iteration
'''
def extract_candidates_for_solution(config, distances, candidates, team, team_idx, to_solution):

    # pick and remove best "move" candidate (peek from top)
    candidate, new_candidates = get_best_candidate(candidates)
    candidates = new_candidates

    #logger.info('candidate: {}'.format(candidate))

    apply_candidate(to_solution, candidate)
    #logger.info('solution candidates ... {}'.format(to_solution.team_jobs[team_idx].jobs_seq.jobs))

    # if still have candidates
    if len(candidates) > 0:
        #logger.info('extract more candidates after new job addition: {}'.format(len(to_solution.team_jobs[team_idx].jobs_seq.jobs)))
        # extract  more candidates with the new addition
        add_to_canditate_list(config, distances, candidates, to_solution.unfulfilled, to_solution.team_jobs[team_idx].jobs_seq, team, team_idx)
        # repeat
        extract_candidates_for_solution(config, distances, candidates, team, team_idx, to_solution)
    
    logger.debug('... end candidate creation')
   
   

def build_solution_candidate(config, distances, candidates, best_solution):

    logger.info('building solution with candidates ... {}'.format(len(candidates)))
    for idx, team in enumerate(best_solution.teams):
        logger.info('extract candidate for solution for team ... {}'.format(idx))
        extract_candidates_for_solution(config, distances, candidates, team, idx, best_solution)