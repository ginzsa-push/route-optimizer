
from utils import clone_pre_post_jobs
from travel_calculator import total_travel_time_in_sec, sum_no_bikes_except_last_job, calculate_total_time_in_seconds

'''
validate that distances are present for all jobs
'''
def is_distance_valid_for_vehicle(distances, solution):

    for i, team in enumerate(solution.teams):

        jobs_seq = solution.get_job_seq_at(i).jobs_seq

        valid = is_distance_valid_for_job_vehicle(distances, jobs_seq, team)

        if not valid:
            return False

    return True

def is_distance_valid_for_job_vehicle(distances, jobs_seq, team):

    previous_job = None
    jobs_to_validate = [jobs_seq.start] + jobs_seq.jobs + [jobs_seq.end]
    for job in jobs_to_validate:
        if previous_job is not None:
            # if jobs are not in distance travel return False
            if distances.get_travel_time(previous_job, job, team.vehicle.speed) == -1:
                return False
        previous_job = job

    return True


'''
validates if is within vahicle's load capacity constrains
'''
def is_journey_capacity_within_constrains(solution):
    for i, team in enumerate(solution.teams):

        jobs_seq = solution.get_job_seq_at(i).jobs_seq

        valid = is_journey_capacity_within_vehicle_constrain(jobs_seq, team.vehicle)

        if not valid:
            return False

    return True

def is_journey_capacity_within_vehicle_constrain(jobs, vehicle):
    return sum_no_bikes_except_last_job(jobs) < vehicle.capacity
    



'''
validates that jorney's time is within the team's vehicle time constrains
'''
def is_journey_time_within_constrains(distances, solution):
    for i, team in enumerate(solution.teams):

        jobs_seq = solution.get_job_seq_at(i)

        valid = is_journey_time_within_team_constrains(distances, jobs_seq, team)

        if not valid:
            return False

    return True

def is_journey_time_within_team_constrains(distances, jobs, team):
    return total_travel_time_in_sec(distances, jobs, team) < team.max_single_journey_time_sec


'''
validate if total journey (here includes waiting and loading time) is within team's vehicle time constrains
'''
def is_total_journey_time_within_constrains(distances, solution):
    for i, team in enumerate(solution.teams):
        jobs_seq = solution.get_job_seq_at(i)

        valid = is_total_journey_time_within_team_constrains(distances, jobs_seq.jobs, team)

        if not valid:
            return False

    return True

'''
is total journey within team constrains
'''
def is_total_journey_time_within_team_constrains(distances, jobs, team):
    return calculate_total_time_in_seconds(distances, jobs, team) < team.time_available_sec

'''
is jobs sequence valid
'''
def is_cadidate_valid(distances, jobs, team):
    return is_distance_valid_for_job_vehicle(distances, jobs, team) and \
                        is_journey_capacity_within_vehicle_constrain(jobs, team.vehicle) and \
                        is_journey_time_within_team_constrains(distances, jobs, team) and \
                        is_total_journey_time_within_team_constrains(distances, jobs, team)


'''
extract a candidate jobs and validate it
'''
def is_solution_cadidate_valid(distances, solution, job, team_idx, position):
    _, temp = clone_pre_post_jobs(position, solution, job, team_idx)
    return is_cadidate_valid(distances, temp, solution.teams[team_idx])


'''
validate solution
'''
def validate_solution(distances, solution):
    return is_distance_valid_for_vehicle(distances, solution) and \
                        is_journey_capacity_within_constrains(solution) and \
                        is_journey_time_within_constrains(distances, solution) and \
                        is_total_journey_time_within_constrains(distances, solution)