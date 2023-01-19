"""This test file tests the first 5 steps of my alpha miner implementation. 
The expected static test data are from test_data.py
"""

import unittest as ut
import alpha, test_data


class test_alpha(ut.TestCase):
    event_log = test_data.event_logs
    ab_pairs = test_data.AB_paris
    test_files = test_data.file_names

    # test step1
    def test_find_tansitions(self):   
        for file in self.test_files:
            log = self.event_log.get(file)
            actual = alpha.find_transitions(log)
            expected = test_data.transitions.get(file) 
            self.assertEqual(actual, expected)

    # test step2
    def test_find_intial_transitions(self):
        for file in self.test_files:
            log = self.event_log.get(file)
            actual = alpha.find_intial_transitions(log)
            expected = test_data.init_transitions.get(file)
            self.assertEqual(actual, expected)
        
     # test step3
    def test_find_last_transitions(self):
        for file in self.test_files:
            log = self.event_log.get(file)
            actual = alpha.find_last_transitions(log)
            expected = test_data.last_transitions.get(file)   
            self.assertEqual(actual, expected)

     # test step4
    def test_find_AB_pairs(self):
        for file in self.test_files:
            log = self.event_log.get(file)
            actual = alpha.find_AB_pairs(log)
            expected = test_data.AB_paris.get(file)  
            self.assertTrue(alpha.is_equal(actual, expected))

     # test step5
    def test_delete_subsets(self):
        for file in self.test_files:
            pair = self.ab_pairs.get(file)
            actual = alpha.delete_subsets(pair)
            expected = test_data.max_AB_pairs.get(file)
            self.assertTrue(alpha.is_equal(actual, expected))

if __name__ == "__main__":
    ut.main()
