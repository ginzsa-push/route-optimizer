
from utils import clone_pre_post_jobs
from travel_calculator import sum_no_bikes_in_jobs, calculate_total_time_in_seconds


def calculate_fitness(config, distances, solution):
    fitness = 0.0
    for team in solution.teams:
        fitness += calculate_jobs_fitness(config, distances, solution.get_job_seq_at[team.id].jobs, team)
    return fitness


def calculate_jobs_fitness(config, distances, jobs, team):

    bikes = min(sum_no_bikes_in_jobs(jobs), team.vehicle.capacity)
   
    total_travel_time = calculate_total_time_in_seconds(distances, jobs, team)

    bike_weight = config['bike_weight']
    time_weight = config['time_weight']

    return (bikes * bike_weight) - (total_travel_time * time_weight)
