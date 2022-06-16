import logging
import copy
import uuid

logger = logging.getLogger()

class Vehicle:
    def __init__(self, *args, **kwargs):
        self.capacity = kwargs.get('capacity', None)
        self.avg_load_time_sec = kwargs.get('avg_load_time_sec', None)
        self.avg_stopping_time_sec = kwargs.get('avg_stopping_time_sec', None)
        self.speed = kwargs.get('speed', 15.) # default to 15
        self.id = str(uuid.uuid4())

class Team:
    def __init__(self, *args, **kwargs):
        self.vehicle = kwargs.get('vehicle', None)
        self.time_available_sec = kwargs.get('time_available_sec', None) 
        self.max_single_journey_time_sec = kwargs.get('max_single_journey_time_sec', None) 
        self.starting_bikes_on_board = kwargs.get('starting_bikes_on_board', None) 
        self.allowedEndDepot = []
        self.id = str(uuid.uuid4())

'''
job sequence contain a list 'sequence' of touple ('DOCK_2',3) jobs
it also contain the start and end ds
'''
class JobsSequence:

    def __init__(self, *args, **kwargs):
        jobs_seq = kwargs.get('jobs_seq', None)

        if jobs_seq is None:
            self.jobs = kwargs.get('jobs', [])
            #TODO assume hardcoded value! 
            self.start = kwargs.get('start', ('DEPOT_1', 0))
            self.end = kwargs.get('end', ('DEPOT_1', 0))
        else:
            self.jobs.append(jobs_seq.jobs)
            self.start = jobs_seq.start
            self.end = jobs_seq.end

'''
Team jobs, job sequence  and teams
'''
class TeamJobs:
    def __init__(self, *args, **kwargs):
        self.team = kwargs.get('team', None)
        self.indx = kwargs.get('indx', None)

        self.jobs_seq = None
        jbs_seq = kwargs.get('jobs_seq', None)

        if jbs_seq is None:
            self.jobs_seq = JobsSequence()
        else:
            self.jobs_seq = JobsSequence(jbs_seq)

'''
jobs is list of dock id, no of broken bikes touples ' ('DOCK_0', 0) '
'''
class Solution:
    def __init__(self, jobs, teams):
        self.teams = teams

        if type(jobs) == dict: # for clone
            self.unfulfilled = jobs
        else:
            self.unfulfilled = dict((j[0], j[1]) for j in jobs)

        self.team_jobs_map = {}
        self.affected_jobs = []
        for i, t in enumerate(teams):
            tj = TeamJobs(team=t, indx=i)
            self.team_jobs_map[t.id] = tj
        self.id = str(uuid.uuid4())

    '''
    when a job is added, should be removed from the 'unfulfilled', 
    '''
    def add_job(self, job_in, idx, job_seq_idx=None):
        logger.debug('adding job {}'.format(job_in))
        job_in_tuple = None 

        if type(job_in) == tuple:
            job_in_tuple = job_in
            job_in = job_in[0]

        # get obj from dict and delete
        j = self.unfulfilled.get(job_in, None)

        logger.debug('job: ({},{}) with unfullfiled size: {}'.format(job_in, j, len(self.unfulfilled)))

        # if is in unfulfilled, delete it
        if j is not None:
            del self.unfulfilled[job_in]
            job_to_append =(job_in, j)
        else:
            job_to_append = job_in_tuple

        logger.debug('job extracted: {} with unfulfilled size: {}'.format(job_to_append, len(self.unfulfilled)))

        if job_seq_idx is None:    
            self.team_jobs_map[idx].jobs_seq.jobs.append(job_to_append)
        else:
            self.team_jobs_map[idx].jobs_seq.jobs.insert(job_seq_idx, job_to_append)

    def get_job_seq_at(self, idx):
        return self.team_jobs_map[idx]

    def clone(self):
        cloned_solution = Solution(copy.deepcopy(self.unfulfilled), copy.deepcopy(self.teams))
        # copy the same job values from other team different to idx
        for team in self.teams:
            in_jobs = self.get_job_seq_at(team.id).jobs_seq.jobs
            for idx, in_job in enumerate(in_jobs):
                cloned_solution.add_job(in_job, team.id, job_seq_idx=idx)
                
        return cloned_solution

    def collect_all_jobs(self):
        all_jobs = []
        for team in self.teams:
            in_jobs = self.get_job_seq_at(team.id).jobs_seq.jobs
            all_jobs.append(in_jobs)
        return all_jobs


'''
Candidate 
[team_jobs.indx,  idx, j[0], j[1], fitness]
'''
class Candidate:
    def __init__(self, *args, **kwargs):
        self.candidate = kwargs.get('candidate')
        if self.candidate is None:
            self.team = kwargs.get('team')
            self.position = kwargs.get('pos')
            self.item = kwargs.get('item')
            self.value = kwargs.get('value')
            self.fitness = kwargs.get('fitness')
            self.candidate = [self.team.id, self.position, self.item, self.value, self.fitness]
        else:
            self.team = self.candidate[0]
            self.position = self.candidate[1]
            self.item = self.candidate[2]
            self.value = self.candidate[3]
            self.fitness = self.candidate[4]
        
        self.job_key =  '{}-{}'.format(self.item, self.value)
        self.job = (self.item, self.value)
        self.id = str(uuid.uuid4())