"""
This test file tests the first 5 steps of my heuristic miner implementation using the 11 test files. 
The expected static test data are from test_data.py
"""

import os, sys, unittest as ut

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import heuristic_miner as hm, import_xes
import test_data


class test_heuristic(ut.TestCase):
    # static test data taken from test file
    test_files = test_data.file_names
    traces = test_data.traces_freq
    transitions = test_data.transitions_freq
    df = test_data.direct_follows_freq
    parallel = test_data.parallel_freq
    dm = test_data.dependency_measures
    parser = import_xes.importer()

    # test step1
    def test_traces(self):
        for file in self.test_files:
            expected_trace = self.traces[file]
            actual_trace = hm.traces(self.parser.read_xes("test_files/" + str(file)))
            self.assertEqual(expected_trace, actual_trace)
    
    # test step2
    def test_find_tansitions(self):   
        for file in self.test_files:
            expected_trans = self.transitions[file]
            actual_trans = hm.find_transitions(self.parser.read_xes("test_files/" + str(file)))
            self.assertEqual(expected_trans, actual_trans)
    
    # test step3
    def test_direct_follows(self):
        for file in self.test_files:
            expected_df = self.df[file]
            actual_df = hm.direct_follows(self.traces[file])
            self.assertEqual(expected_df, actual_df)
        
     # test step4
    def test_dependency_measure(self):
        for file in self.test_files:
            expected_dm = self.dm[file]   
            actual_dm = hm.denpendency_measure(self.parser.read_xes("test_files/" + str(file)))
            self.assertEqual(expected_dm, actual_dm)

     # test parallel method in step6
    def test_find_parallel_transitions(self):
        for file in self.test_files:
            expected_parallel = self.parallel[file]
            actual_parallel = hm.find_parallel_transitions(self.df[file])
            self.assertEqual(expected_parallel, actual_parallel)

if __name__ == "__main__":
    ut.main()
