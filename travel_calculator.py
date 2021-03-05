from model import JobsSequence


'''
calculate total time in seconds
'''
def calculate_total_time_in_seconds(distances, jobs_seq, team):
    return total_travel_time_in_sec(distances, jobs_seq, team) + \
            calc_load_time_seconds(jobs_seq, team.vehicle) + \
            calc_stopping_time_seconds(jobs_seq, team.vehicle)


'''
calculate travel time for a job sequence
this function includes start and end service points
'''
def total_travel_time_in_sec(distances, jobs_seq, team):
    travel_time = 0
    if type(jobs_seq) == JobsSequence:
        jobs_to_process = [jobs_seq.start] + jobs_seq.jobs + [jobs_seq.end]
    else:
        jobs_to_process = jobs_seq
    
    previous_job = None
    for job in jobs_to_process:
        if previous_job is not None:
            travel_time += distances.get_travel_time(previous_job, job, team.vehicle.speed)
        previous_job = job
    return travel_time

'''
return time in seconds for the stopping time in each job 
'''
def calc_stopping_time_seconds(jobs_seq, vehicle):
    # +1 includes end stop
    jobs = jobs_sequence_or_list(jobs_seq)
    return (len(jobs) + 1) * vehicle.avg_stopping_time_sec

'''
return time in seconds, corresponding to the sum of time taken to handle each job 
'''
def calc_load_time_seconds(jobs_seq, vehicle):
    return total_no_bikes(jobs_seq, vehicle) * vehicle.avg_load_time_sec

'''
return the minimum value betwee:
    sum number of bikes in a jobs sequence
    vehicle capacity
'''
def total_no_bikes(jobs_seq, vehicle):

    jobs = jobs_sequence_or_list(jobs_seq)

    total_bikes = 0
    for job in jobs:
        total_bikes += int(job[1])

    return min(total_bikes, vehicle.capacity)

'''
handle jobs list or job sequence
'''
def jobs_sequence_or_list(jobs_seq):
    # 
    if type(jobs_seq) == list: 
        jobs = jobs_seq
    else:
        jobs =  jobs_seq.jobs
    return jobs

'''
sum number of bikes except last one
'''
def sum_no_bikes_except_last_job(jobs_seq):
    return sum_no_bikes_in_jobs(jobs_seq.jobs[:-1])

def sum_no_bikes_in_jobs(jobs):
    count = 0
    for j in jobs:
        count += j[1]

    return count