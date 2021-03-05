import sys, os

import unittest

import test_utils as utils

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model import Team
from model import Solution

from neighbourhood import swap_in_same_sequence, swap_in_same_sequence_1, shift_in_same_sequence, remove_solution_neighbourhood, insert_unused_neighbourhood, replace_with_unused_neighbourhood


class TestSwapInSameSequence(unittest.TestCase):

    '''
    Test swap in the same sequence for one team
    generate all swapped alternatives, it doesn't change the other jobs positions

    '''
    def test_swap_in_same_sequence_one_team(self):
        all_jobs = [('DOCK_A', 3), ('DOCK_B', 4), ('DOCK_C', 6), ('DOCK_D', 1),  ('DOCK_E', 2)]
        team = Team()
        teams = [team]

        solution = Solution(all_jobs, teams)
        
        for j in all_jobs:
            solution.add_job(j, 0)

        rs = swap_in_same_sequence_1(solution, [], 1)

        expected_variations = [[ [('DOCK_A', 3), ('DOCK_B', 4), ('DOCK_C', 6), ('DOCK_E', 2), ('DOCK_D', 1)],
                                [('DOCK_A', 3), ('DOCK_B', 4), ('DOCK_D', 1), ('DOCK_C', 6), ('DOCK_E', 2)], 
                                [('DOCK_A', 3), ('DOCK_B', 4), ('DOCK_E', 2), ('DOCK_D', 1), ('DOCK_C', 6)], 
                                [('DOCK_A', 3), ('DOCK_C', 6), ('DOCK_B', 4), ('DOCK_D', 1), ('DOCK_E', 2)], 
                                [('DOCK_A', 3), ('DOCK_D', 1), ('DOCK_C', 6), ('DOCK_B', 4), ('DOCK_E', 2)], 
                                [('DOCK_A', 3), ('DOCK_E', 2), ('DOCK_C', 6), ('DOCK_D', 1), ('DOCK_B', 4)], 
                                [('DOCK_B', 4), ('DOCK_A', 3), ('DOCK_C', 6), ('DOCK_D', 1), ('DOCK_E', 2)], 
                                [('DOCK_C', 6), ('DOCK_B', 4), ('DOCK_A', 3), ('DOCK_D', 1), ('DOCK_E', 2)], 
                                [('DOCK_D', 1), ('DOCK_B', 4), ('DOCK_C', 6), ('DOCK_A', 3), ('DOCK_E', 2)], 
                                [('DOCK_E', 2), ('DOCK_B', 4), ('DOCK_C', 6), ('DOCK_D', 1), ('DOCK_A', 3)]]]

        self.assertEqual(len(rs), 10)
        self.assertTrue(self.expected_in_following_variations(expected_variations, rs))

    def test_swap_in_same_sequence_one_team_except_one_job(self):
        all_jobs = [('DOCK_A', 3), ('DOCK_B', 4), ('DOCK_C', 6), ('DOCK_D', 1),  ('DOCK_E', 2)]
        team = Team()
        teams = [team]

        solution = Solution(all_jobs, teams)
        
        for j in all_jobs:
            solution.add_job(j, 0)

        rs = swap_in_same_sequence_1(solution, [('DOCK_E', 2)], 1)

        expected_variations = [[ [('DOCK_B', 4), ('DOCK_A', 3), ('DOCK_C', 6), ('DOCK_D', 1)], 
                                [('DOCK_C', 6), ('DOCK_B', 4), ('DOCK_A', 3), ('DOCK_D', 1)],
                                [('DOCK_D', 1), ('DOCK_B', 4), ('DOCK_C', 6), ('DOCK_A', 3)],
                                [('DOCK_A', 3), ('DOCK_C', 6), ('DOCK_B', 4), ('DOCK_D', 1)], 
                                [('DOCK_A', 3), ('DOCK_D', 1), ('DOCK_C', 6), ('DOCK_B', 4)], 
                                [('DOCK_A', 3), ('DOCK_B', 4), ('DOCK_D', 1), ('DOCK_C', 6)]]]

        self.assertEqual(len(rs), 6)
        self.assertTrue(self.expected_in_following_variations(expected_variations, rs))

    def test_swap_in_same_sequence_two_teams(self):
        all_jobs = [('DOCK_A', 3), ('DOCK_B', 4), ('DOCK_C', 6), ('DOCK_D', 1)]
        team1 = Team()
        team2 = Team()

        teams = [team1, team2]

        solution = Solution(all_jobs, teams)
        
        # add to team 0
        solution.add_job(all_jobs[0], 0)
        solution.add_job(all_jobs[1], 0)
        # add to team 1
        solution.add_job(all_jobs[2], 1)
        solution.add_job(all_jobs[3], 1)

        rs = swap_in_same_sequence_1(solution, [], 1)

        expected_variations= [
                                        [   [('DOCK_B', 4), ('DOCK_A', 3)], 
                                            [('DOCK_C', 6), ('DOCK_D', 1)]],

                                        [   [('DOCK_A', 3), ('DOCK_B', 4)], 
                                            [('DOCK_D', 1), ('DOCK_C', 6)]]
                                    ]

        self.assertEqual(len(rs), 2)

        self.assertTrue(self.expected_in_following_variations_teams(expected_variations, rs))


    def test_swap_in_same_sequence_two_teams_except_one_job(self):

        all_jobs = [('DOCK_A', 3), ('DOCK_B', 4), ('DOCK_C', 6), ('DOCK_D', 1)]
        team1 = Team()
        team2 = Team()

        teams = [team1, team2]

        solution = Solution(all_jobs, teams)
        
        # add to team 0
        solution.add_job(all_jobs[0], 0)
        solution.add_job(all_jobs[1], 0)
        # add to team 1
        solution.add_job(all_jobs[2], 1)
        solution.add_job(all_jobs[3], 1)

        rs = swap_in_same_sequence(solution, [('DOCK_D', 1)])

        expected_variations= [
                                        [   [('DOCK_B', 4), ('DOCK_A', 3)], 
                                            [('DOCK_C', 6), ('DOCK_D', 1)]]
                                    ]

        self.assertEqual(len(rs), 1)
        self.assertTrue(self.expected_in_following_variations_teams(expected_variations, rs))


    # variation divided in two teams
    def expected_in_following_variations_teams(self, variations, rs):
        
        for ii, _ in enumerate(variations): 
            s = rs[ii]          
            for iii, var in enumerate(variations[ii]):
               
                tmp = set(var) - set(s.get_job_seq_at(iii).jobs_seq.jobs)
                
                if len(tmp) != 0:
                    return False

        return True
    
    def expected_in_following_variations(self, variations, rs):   
        for sol in rs:
            for idx, _ in enumerate(sol.teams):
                jbs = sol.get_job_seq_at(idx).jobs_seq.jobs
                if jbs not in variations[idx]:
                    return False
            
        return True

    '''
    reinserting job in a new possition, shifting the other's job positions
    '''
    def test_shift_in_same_sequence_one_team(self):
            all_jobs = [('DOCK_A', 3), ('DOCK_B', 4), ('DOCK_C', 6), ('DOCK_D', 1)]
            team = Team()
            teams = [team]

            solution = Solution(all_jobs, teams)
            
            for j in all_jobs:
                solution.add_job(j, 0)

            rs = shift_in_same_sequence(solution, [], 1)

            expected_variations = [[ 
                                    [('DOCK_B', 4), ('DOCK_A', 3), ('DOCK_C', 6), ('DOCK_D', 1)], 
                                    [('DOCK_B', 4), ('DOCK_C', 6), ('DOCK_A', 3), ('DOCK_D', 1)], 
                                    [('DOCK_B', 4), ('DOCK_C', 6), ('DOCK_D', 1), ('DOCK_A', 3)], 

                                    [('DOCK_A', 3), ('DOCK_C', 6), ('DOCK_B', 4), ('DOCK_D', 1)], 
                                    [('DOCK_A', 3), ('DOCK_C', 6), ('DOCK_D', 1), ('DOCK_B', 4)], 
                                    
                                    [('DOCK_C', 6), ('DOCK_A', 3), ('DOCK_B', 4), ('DOCK_D', 1)],
                                    [('DOCK_A', 3), ('DOCK_B', 4), ('DOCK_D', 1), ('DOCK_C', 6)],

                                    [('DOCK_D', 1), ('DOCK_A', 3), ('DOCK_B', 4), ('DOCK_C', 6)],
                                    [('DOCK_A', 3), ('DOCK_D', 1), ('DOCK_B', 4), ('DOCK_C', 6)]]]

            self.assertEqual(len(rs), 9)
            self.assertTrue(self.expected_in_following_variations(expected_variations, rs))
      
 
    def test_shift_in_same_sequence_one_team_except_one(self):

        all_jobs = [('DOCK_A', 3), ('DOCK_B', 4), ('DOCK_C', 6), ('DOCK_D', 1)]
        team = Team()
        teams = [team]

        solution = Solution(all_jobs, teams)
            
        for j in all_jobs:
            solution.add_job(j, 0)

        rs = shift_in_same_sequence(solution, [('DOCK_A', 3)], 1)

        expected_variations = [[ 
                                    [('DOCK_A', 3), ('DOCK_C', 6), ('DOCK_B', 4), ('DOCK_D', 1)],
                                    [('DOCK_A', 3), ('DOCK_C', 6), ('DOCK_D', 1), ('DOCK_B', 4)], 
                                    [('DOCK_C', 6), ('DOCK_A', 3), ('DOCK_B', 4), ('DOCK_D', 1)],
                                    [('DOCK_A', 3), ('DOCK_B', 4), ('DOCK_D', 1), ('DOCK_C', 6)],
                                    [('DOCK_D', 1), ('DOCK_A', 3), ('DOCK_B', 4), ('DOCK_C', 6)],
                                    [('DOCK_A', 3), ('DOCK_D', 1), ('DOCK_B', 4), ('DOCK_C', 6)]
                                ]]

        self.assertEqual(len(rs), 6)
        self.assertTrue(self.expected_in_following_variations(expected_variations, rs))

    def test_shift_in_same_sequence_two_team(self):
        all_jobs = [('DOCK_A', 3), ('DOCK_B', 4), ('DOCK_C', 6), ('DOCK_D', 1)]
        team1 = Team()
        team2 = Team()

        teams = [team1, team2]

        solution = Solution(all_jobs, teams)
        
        # add to team 0
        solution.add_job(all_jobs[0], 0)
        solution.add_job(all_jobs[1], 0)
        # add to team 1
        solution.add_job(all_jobs[2], 1)
        solution.add_job(all_jobs[3], 1)

        rs = swap_in_same_sequence(solution, [])

        expected_variations= [
                                        [   [('DOCK_B', 4), ('DOCK_A', 3)], 
                                            [('DOCK_C', 6), ('DOCK_D', 1)]],

                                        [   [('DOCK_A', 3), ('DOCK_B', 4)], 
                                            [('DOCK_D', 1), ('DOCK_C', 6)]]
                                    ]

        self.assertEqual(len(rs), 2)

        self.assertTrue(self.expected_in_following_variations_teams(expected_variations, rs))


    def test_shift_in_same_sequence_two_team_except_two_job(self):

        all_jobs = [('DOCK_A', 3), ('DOCK_B', 4), ('DOCK_C', 6), ('DOCK_D', 1)]
        team1 = Team()
        team2 = Team()

        teams = [team1, team2]

        solution = Solution(all_jobs, teams)
        
        # add to team 0
        solution.add_job(all_jobs[0], 0)
        solution.add_job(all_jobs[1], 0)
        # add to team 1
        solution.add_job(all_jobs[2], 1)
        solution.add_job(all_jobs[3], 1)

        rs = swap_in_same_sequence(solution, [('DOCK_C', 6), ('DOCK_D', 1)])

        expected_variations= [
                                        [   [('DOCK_B', 4), ('DOCK_A', 3)], 
                                            [('DOCK_C', 6), ('DOCK_D', 1)]]
                                    ]

        self.assertEqual(len(rs), 1)
        self.assertTrue(self.expected_in_following_variations_teams(expected_variations, rs))


    '''
    remove one of the jobs from the jobs added
    '''
    def test_remove_solution_neighbourhood(self):
        all_jobs = [('DOCK_A', 3), ('DOCK_B', 4), ('DOCK_C', 6), ('DOCK_D', 1), ('DOCK_E', 3), ('DOCK_F', 2)]
        team1 = Team()
        team2 = Team()

        teams = [team1, team2]

        solution = Solution(all_jobs, teams)

        # add to team 0
        solution.add_job(all_jobs[0], 0)
        solution.add_job(all_jobs[1], 0)
        # add to team 1
        solution.add_job(all_jobs[2], 1)

        rs = remove_solution_neighbourhood(solution, [])
        # keep order
        expected_variations= [                
                                [   [('DOCK_B', 4)],                [('DOCK_C', 6)] ],
                                [   [('DOCK_A', 3)],                [('DOCK_C', 6)] ],
                                [   [('DOCK_A', 3), ('DOCK_B', 4)], [] ]                              
                            ]

        self.assertEqual(len(rs), 3)
        self.assertTrue(self.expected_in_following_variations_teams(expected_variations, rs))

    def test_remove_solution_neighbourhood_except_one_job(self):
        all_jobs = [('DOCK_A', 3), ('DOCK_B', 4), ('DOCK_C', 6), ('DOCK_D', 1), ('DOCK_E', 3), ('DOCK_F', 2)]
        team1 = Team()
        team2 = Team()

        teams = [team1, team2]

        solution = Solution(all_jobs, teams)

        # add to team 0
        solution.add_job(all_jobs[0], 0)
        solution.add_job(all_jobs[1], 0)
        # add to team 1
        solution.add_job(all_jobs[2], 1)

        rs = remove_solution_neighbourhood(solution, [('DOCK_C', 6)])
        # keep order
        expected_variations= [                
                                [   [('DOCK_B', 4)],                [('DOCK_C', 6)] ],
                                [   [('DOCK_A', 3)],                [('DOCK_C', 6)] ]                             
                            ]

        self.assertEqual(len(rs), 2)
        self.assertTrue(self.expected_in_following_variations_teams(expected_variations, rs))


    '''
    insert an unused job to the jobs added
    '''
    def test_insert_unused_neighbourhood(self):
        all_jobs = [('DOCK_A', 3), ('DOCK_B', 4), ('DOCK_E', 2),  ('DOCK_F', 4)]
        team = Team()
        teams = [team]

        solution = Solution(all_jobs, teams)

         # add to team 0
        solution.add_job(all_jobs[0], 0)
        solution.add_job(all_jobs[1], 0)
        
        rs = insert_unused_neighbourhood(solution, [])

        expected_variations = [[ [('DOCK_E', 2), ('DOCK_A', 3), ('DOCK_B', 4)],
                                 [('DOCK_A', 3), ('DOCK_E', 2), ('DOCK_B', 4)],
                                 [('DOCK_A', 3), ('DOCK_B', 4), ('DOCK_E', 2)],
                                 [('DOCK_F', 4), ('DOCK_A', 3), ('DOCK_B', 4)],
                                 [('DOCK_A', 3), ('DOCK_F', 4), ('DOCK_B', 4)],
                                 [('DOCK_A', 3), ('DOCK_B', 4), ('DOCK_F', 4)]]]

        self.assertEqual(len(rs), 6)
        self.assertTrue(self.expected_in_following_variations(expected_variations, rs))


    def test_insert_unused_neighbourhood_except_one_job(self):
        # unused = [('DOCK_C', 6), ('DOCK_D', 1)]
        all_jobs = [('DOCK_A', 3), ('DOCK_B', 4), ('DOCK_E', 2),  ('DOCK_F', 4)]
        team = Team()
        teams = [team]

        solution = Solution(all_jobs, teams)

         # add to team 0
        solution.add_job(all_jobs[0], 0)
        solution.add_job(all_jobs[1], 0)
        
        rs = insert_unused_neighbourhood(solution, [('DOCK_E', 2)])

        expected_variations = [[ [('DOCK_F', 4), ('DOCK_A', 3), ('DOCK_B', 4)],
                                 [('DOCK_A', 3), ('DOCK_F', 4), ('DOCK_B', 4)],
                                 [('DOCK_A', 3), ('DOCK_B', 4), ('DOCK_F', 4)] ]]

        self.assertEqual(len(rs), 3)
        self.assertTrue(self.expected_in_following_variations(expected_variations, rs))

    '''
    pick an unused job and replace one of the job with it
    '''
    def test_replace_with_unused_neighbourhood(self):
        # unused = ('DOCK_C', 6), ('DOCK_D', 1)
        all_jobs = [('DOCK_A', 3), ('DOCK_B', 4), ('DOCK_E', 2),  ('DOCK_F', 4)]
        team = Team()
        teams = [team]

        solution = Solution(all_jobs, teams)

        # add to team 0
        solution.add_job(all_jobs[0], 0)
        solution.add_job(all_jobs[1], 0)

        
        rs = replace_with_unused_neighbourhood(solution, [])

        expected_variations = [[[('DOCK_E', 2), ('DOCK_B', 4)],
                                [('DOCK_A', 3), ('DOCK_E', 2)],
                                [('DOCK_F', 4), ('DOCK_B', 4)],
                                [('DOCK_A', 3), ('DOCK_F', 4)]]]

        self.assertEqual(len(rs), 4)
        self.assertTrue(self.expected_in_following_variations(expected_variations, rs))

    
    def test_replace_with_unused_neighbourhood_except_two_jobs(self):
        # unused = ('DOCK_C', 6), ('DOCK_D', 1)
        all_jobs = [('DOCK_A', 3), ('DOCK_B', 4), ('DOCK_E', 2),  ('DOCK_F', 4)]
        team = Team()
        teams = [team]

        solution = Solution(all_jobs, teams)

        # add to team 0
        solution.add_job(all_jobs[0], 0)
        solution.add_job(all_jobs[1], 0)

        
        rs = replace_with_unused_neighbourhood(solution, [('DOCK_E', 2), ('DOCK_A', 3)])

        expected_variations = [[[('DOCK_A', 3), ('DOCK_F', 4)]]]

        for s in rs:
            print(s.team_jobs[0].jobs_seq.jobs)
            
        self.assertEqual(len(rs), 1)
        self.assertTrue(self.expected_in_following_variations(expected_variations, rs))


if __name__ == '__main__':
    unittest.main()
