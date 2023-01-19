"""
This file contains static test data for both Alpha Miner and Heuristic Miner.
The data are extracted from the 11 test files. As Alpha miner doesn't consider frequency, 
the static data is relatively short. As for the Heuristic miner, frequency is necessary, 
the traces might appear thousands of times, which is difficult to store in this file. 
"""

# ========= test data for alpha miner start ===========

file_names = ['L1.xes', 'L2.xes', 'L3.xes','L4.xes','L5.xes', 'L6.xes', 'L7.xes', 'billinstances.xes', 'flyerinstances.xes', 'posterinstances.xes','running-example.xes', ]

event_logs = {
    'L1.xes': [['a', 'e', 'd'], ['a', 'c', 'b', 'd'], ['a', 'b', 'c', 'd']], 
    'L2.xes': [['a', 'c', 'b', 'd'], ['a', 'c', 'b', 'e', 'f', 'b', 'c', 'd'], ['a', 'b', 'c', 'e', 'f', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'e', 'f', 'c', 'b', 'd'], ['a', 'c', 'b', 'e', 'f', 'b', 'c', 'e', 'f', 'c', 'b', 'd']], 
    'L3.xes': [['a', 'b', 'c', 'd', 'e', 'f', 'b', 'c', 'd', 'e', 'f', 'b', 'd', 'c', 'e', 'g'], ['a', 'b', 'd', 'c', 'e', 'g'], ['a', 'b', 'c', 'd', 'e', 'f', 'b', 'd', 'c', 'e', 'g']], 
    'L4.xes': [['a', 'c', 'd'], ['b', 'c', 'd'], ['b', 'c', 'e'], ['a', 'c', 'e']], 
    'L5.xes': [['a', 'b', 'e', 'c', 'd', 'b', 'f'], ['a', 'e', 'b', 'c', 'd', 'b', 'f'], ['a', 'b', 'c', 'e', 'd', 'b', 'f'], ['a', 'b', 'c', 'd', 'e', 'b', 'f'], ['a', 'b', 'e', 'f']], 
    'L6.xes': [['b', 'f', 'd', 'g'], ['b', 'd', 'f', 'g'], ['a', 'e', 'c', 'g'], ['a', 'c', 'e', 'g']], 
    'L7.xes': [['a', 'b', 'b', 'c'], ['a', 'b', 'c'], ['a', 'b', 'b', 'b', 'b', 'c'], ['a', 'c']], 
    'billinstances.xes': [['write bill', 'print bill', 'deliver bill']], 
    'flyerinstances.xes': [['receive flyer order', 'design flyer', 'send draft to customer', 'design flyer', 'send draft to customer', 'design flyer', 'send draft to customer', 'print flyer', 'deliver flyer'], ['receive flyer order', 'design flyer', 
                            'send draft to customer', 'design flyer', 'send draft to customer', 'print flyer', 'deliver flyer'], ['receive flyer order', 'design flyer', 'send draft to customer', 'print flyer', 'deliver flyer']], 
    'posterinstances.xes': [['receive order and photo', 'design photo poster', 'print poster', 'deliver poster']],
    'running-example.xes': [['register request', 'examine casually', 'check ticket', 'decide', 'reinitiate request', 'examine thoroughly', 'check ticket', 'decide', 'pay compensation'], 
                            ['register request', 'check ticket', 'examine casually', 'decide', 'pay compensation'], ['register request', 'examine thoroughly', 'check ticket', 'decide', 'reject request'], 
                            ['register request', 'examine casually', 'check ticket', 'decide', 'pay compensation'], 
                            ['register request', 'examine casually', 'check ticket', 'decide', 'reinitiate request', 'check ticket', 'examine casually', 'decide', 'reinitiate request', 'examine casually', 'check ticket', 'decide', 'reject request'], 
                            ['register request', 'check ticket', 'examine thoroughly', 'decide', 'reject request']], 
}

transitions = {
    'L1.xes': {'c', 'e', 'a', 'd', 'b'},
    'L2.xes': {'e', 'd', 'a', 'c', 'b', 'f'},
    'L3.xes': {'d', 'a', 'b', 'g', 'e', 'f', 'c'},
    'L4.xes': {'d', 'e', 'b', 'c', 'a'},
    'L5.xes': {'d', 'c', 'e', 'b', 'a', 'f'},
    'L6.xes': {'g', 'c', 'd', 'e', 'b', 'f', 'a'},
    'L7.xes': {'c', 'a', 'b'},
    'billinstances.xes': {'write bill', 'print bill', 'deliver bill'},
    'flyerinstances.xes': {'receive flyer order', 'print flyer', 'deliver flyer', 'send draft to customer', 'design flyer'},
    'posterinstances.xes': {'print poster', 'receive order and photo', 'design photo poster', 'deliver poster'},
    'running-example.xes': {'pay compensation', 'reinitiate request', 'register request', 'decide', 'examine casually', 'reject request', 'check ticket', 'examine thoroughly'}
}

init_transitions = {
    'L1.xes': {'a'},
    'L2.xes': {'a'},
    'L3.xes': {'a'},
    'L4.xes': {'b', 'a'},
    'L5.xes': {'a'},
    'L6.xes': {'b', 'a'},
    'L7.xes': {'a'},
    'billinstances.xes': {'write bill'},
    'flyerinstances.xes': {'receive flyer order'},
    'posterinstances.xes': {'receive order and photo'},
    'running-example.xes': {'register request'}
}

last_transitions = {
    'L1.xes': {'d'},
    'L2.xes': {'d'},
    'L3.xes': {'g'},
    'L4.xes': {'e', 'd'},
    'L5.xes': {'f'},
    'L6.xes': {'g'},
    'L7.xes': {'c'},
    'billinstances.xes': {'deliver bill'},
    'flyerinstances.xes': {'deliver flyer'},
    'posterinstances.xes': {'deliver poster'},
    'running-example.xes': {'reject request', 'pay compensation'}
}

AB_paris = {
    'L1.xes': [({'b'}, {'d'}), ({'e', 'c'}, {'d'}), ({'e', 'b'}, {'d'}), ({'c'}, {'d'}), ({'e'}, {'d'}), ({'a'}, {'b'}), ({'a'}, {'e', 'c'}), ({'a'}, {'e', 'b'}), ({'a'}, {'c'}), ({'a'}, {'e'})],
    'L2.xes': [({'a'}, {'c'}), ({'a'}, {'b'}), ({'c'}, {'e', 'd'}), ({'c'}, {'d'}), ({'c'}, {'e'}), ({'a', 'f'}, {'c'}), ({'a', 'f'}, {'b'}), ({'f'}, {'c'}), ({'f'}, {'b'}), ({'b'}, {'e', 'd'}), ({'b'}, {'d'}), ({'b'}, {'e'}), ({'e'}, {'f'})],
    'L3.xes': [({'a', 'f'}, {'b'}), ({'c'}, {'e'}), ({'e'}, {'g'}), ({'e'}, {'g', 'f'}), ({'e'}, {'f'}), ({'b'}, {'c'}), ({'b'}, {'d'}), ({'d'}, {'e'}), ({'a'}, {'b'}), ({'f'}, {'b'})],
    'L4.xes': [({'b', 'a'}, {'c'}), ({'c'}, {'e', 'd'}), ({'c'}, {'e'}), ({'c'}, {'d'}), ({'b'}, {'c'}), ({'a'}, {'c'})],
    'L5.xes': [({'a', 'd'}, {'b'}), ({'e'}, {'f'}), ({'b'}, {'c', 'f'}), ({'b'}, {'f'}), ({'b'}, {'c'}), ({'d'}, {'b'}), ({'c'}, {'d'}), ({'a'}, {'e'}), ({'a'}, {'b'})],
    'L6.xes': [({'c'}, {'g'}), ({'d'}, {'g'}), ({'d', 'e'}, {'g'}), ({'c', 'd'}, {'g'}), ({'f', 'e'}, {'g'}), ({'f'}, {'g'}), ({'c', 'f'}, {'g'}), ({'e'}, {'g'}), ({'a'}, {'c'}), ({'a'}, {'e'}), ({'b'}, {'d'}), ({'b'}, {'f'})],
    'L7.xes': [({'a'}, {'c'})],
    'billinstances.xes': [({'write bill'}, {'print bill'}), ({'print bill'}, {'deliver bill'})],
    'flyerinstances.xes': [({'receive flyer order'}, {'design flyer'}), ({'print flyer'}, {'deliver flyer'}), ({'send draft to customer'}, {'print flyer'})],
    'posterinstances.xes': [({'receive order and photo'}, {'design photo poster'}), ({'print poster'}, {'deliver poster'}), ({'design photo poster'}, {'print poster'})],
    'running-example.xes': [({'examine casually', 'examine thoroughly'}, {'decide'}), ({'register request', 'reinitiate request'}, {'examine casually', 'examine thoroughly'}), ({'register request', 'reinitiate request'}, {'examine thoroughly'}), 
                            ({'register request', 'reinitiate request'}, {'examine casually'}), ({'register request', 'reinitiate request'}, {'check ticket'}), ({'decide'}, {'reject request', 'reinitiate request'}), 
                            ({'decide'}, {'reinitiate request', 'pay compensation'}), ({'decide'}, {'reject request', 'pay compensation'}), ({'decide'}, {'reinitiate request'}), ({'decide'}, {'pay compensation'}), ({'decide'}, {'reject request'}), 
                            ({'examine thoroughly'}, {'decide'}), ({'register request'}, {'examine casually', 'examine thoroughly'}), ({'register request'}, {'examine thoroughly'}), ({'register request'}, {'examine casually'}), 
                            ({'register request'}, {'check ticket'}), ({'reinitiate request'}, {'examine casually', 'examine thoroughly'}), ({'reinitiate request'}, {'examine thoroughly'}), ({'reinitiate request'}, {'examine casually'}), 
                            ({'reinitiate request'}, {'check ticket'}), ({'examine casually'}, {'decide'}), ({'check ticket'}, {'decide'})]
}

max_AB_pairs = {
    'L1.xes': [({'e', 'c'}, {'d'}), ({'e', 'b'}, {'d'}), ({'a'}, {'e', 'c'}), ({'a'}, {'e', 'b'})],
    'L2.xes': [({'c'}, {'e', 'd'}), ({'a', 'f'}, {'c'}), ({'a', 'f'}, {'b'}), ({'b'}, {'e', 'd'}), ({'e'}, {'f'})],
    'L3.xes': [({'a', 'f'}, {'b'}), ({'c'}, {'e'}), ({'e'}, {'g', 'f'}), ({'b'}, {'c'}), ({'b'}, {'d'}), ({'d'}, {'e'})],
    'L4.xes': [({'b', 'a'}, {'c'}), ({'c'}, {'e', 'd'})],
    'L5.xes': [({'a', 'd'}, {'b'}), ({'e'}, {'f'}), ({'b'}, {'c', 'f'}), ({'c'}, {'d'}), ({'a'}, {'e'})],
    'L6.xes': [({'d', 'e'}, {'g'}), ({'c', 'd'}, {'g'}), ({'f', 'e'}, {'g'}), ({'c', 'f'}, {'g'}), ({'a'}, {'c'}), ({'a'}, {'e'}), ({'b'}, {'d'}), ({'b'}, {'f'})],
    'L7.xes': [({'a'}, {'c'})],
    'billinstances.xes': [({'write bill'}, {'print bill'}), ({'print bill'}, {'deliver bill'})],
    'flyerinstances.xes': [({'receive flyer order'}, {'design flyer'}), ({'print flyer'}, {'deliver flyer'}), ({'send draft to customer'}, {'print flyer'})],
    'posterinstances.xes': [({'receive order and photo'}, {'design photo poster'}), ({'print poster'}, {'deliver poster'}), ({'design photo poster'}, {'print poster'})],
    'running-example.xes': [({'examine casually', 'examine thoroughly'}, {'decide'}), ({'register request', 'reinitiate request'}, {'examine casually', 'examine thoroughly'}), 
                            ({'register request', 'reinitiate request'}, {'check ticket'}), ({'decide'}, {'reject request', 'reinitiate request'}), 
                            ({'decide'}, {'reinitiate request', 'pay compensation'}), ({'decide'}, {'reject request', 'pay compensation'}), ({'check ticket'}, {'decide'})]
}

# ================== end ====================



# ================== test data for heuristic miner start =================

traces_freq = {
    'L1.xes': {('a', 'e', 'd'): 1, ('a', 'c', 'b', 'd'): 2, ('a', 'b', 'c', 'd'): 3},
    'L2.xes': {('a', 'c', 'b', 'd'): 4, ('a', 'c', 'b', 'e', 'f', 'b', 'c', 'd'): 2, ('a', 'b', 'c', 'e', 'f', 'b', 'c', 'd'): 2, ('a', 'b', 'c', 'd'): 3, ('a', 'b', 'c', 'e', 'f', 'c', 'b', 'd'): 1, ('a', 'c', 'b', 'e', 'f', 'b', 'c', 'e', 'f', 'c', 'b', 'd'): 1},
    'L3.xes': {('a', 'b', 'c', 'd', 'e', 'f', 'b', 'c', 'd', 'e', 'f', 'b', 'd', 'c', 'e', 'g'): 1, ('a', 'b', 'd', 'c', 'e', 'g'): 2, ('a', 'b', 'c', 'd', 'e', 'f', 'b', 'd', 'c', 'e', 'g'): 1},
    'L4.xes': {('a', 'c', 'd'): 45, ('b', 'c', 'd'): 42, ('b', 'c', 'e'): 22, ('a', 'c', 'e'): 38},
    'L5.xes': {('a', 'b', 'e', 'c', 'd', 'b', 'f'): 3, ('a', 'e', 'b', 'c', 'd', 'b', 'f'): 3, ('a', 'b', 'c', 'e', 'd', 'b', 'f'): 2, ('a', 'b', 'c', 'd', 'e', 'b', 'f'): 4, ('a', 'b', 'e', 'f'): 2},
    'L6.xes': {('b', 'f', 'd', 'g'): 4, ('b', 'd', 'f', 'g'): 2, ('a', 'e', 'c', 'g'): 3, ('a', 'c', 'e', 'g'): 2},
    'L7.xes': {('a', 'b', 'b', 'c'): 2, ('a', 'b', 'c'): 3, ('a', 'b', 'b', 'b', 'b', 'c'): 1, ('a', 'c'): 2},
    'billinstances.xes': {('write bill', 'print bill', 'deliver bill'): 1800},
    'flyerinstances.xes': {('receive flyer order', 'design flyer', 'send draft to customer', 'design flyer', 'send draft to customer', 'design flyer', 'send draft to customer', 'print flyer', 'deliver flyer'): 312, 
                           ('receive flyer order', 'design flyer', 'send draft to customer', 'design flyer', 'send draft to customer', 'print flyer', 'deliver flyer'): 285, 
                           ('receive flyer order', 'design flyer', 'send draft to customer', 'print flyer', 'deliver flyer'): 303},
    'posterinstances.xes': {('receive order and photo', 'design photo poster', 'print poster', 'deliver poster'): 900},
    'running-example.xes': {('register request', 'examine casually', 'check ticket', 'decide', 'reinitiate request', 'examine thoroughly', 'check ticket', 'decide', 'pay compensation'): 1, 
                            ('register request', 'check ticket', 'examine casually', 'decide', 'pay compensation'): 1, 
                            ('register request', 'examine thoroughly', 'check ticket', 'decide', 'reject request'): 1, 
                            ('register request', 'examine casually', 'check ticket', 'decide', 'pay compensation'): 1, 
                            ('register request', 'examine casually', 'check ticket', 'decide', 'reinitiate request', 'check ticket', 'examine casually', 'decide', 'reinitiate request', 'examine casually', 'check ticket', 'decide', 'reject request'): 1, 
                            ('register request', 'check ticket', 'examine thoroughly', 'decide', 'reject request'): 1}
    }
transitions_freq = {
    'L1.xes': {'a': 6, 'e': 1, 'd': 6, 'c': 5, 'b': 5},
    'L2.xes': {'a': 13, 'c': 20, 'b': 20, 'd': 13, 'e': 7, 'f': 7},
    'L3.xes': {'a': 4, 'b': 7, 'c': 7, 'd': 7, 'e': 7, 'f': 3, 'g': 4},
    'L4.xes': {'a': 83, 'c': 147, 'd': 87, 'b': 64, 'e': 60},
    'L5.xes': {'a': 14, 'b': 26, 'e': 14, 'c': 12, 'd': 12, 'f': 14},
    'L6.xes': {'b': 6, 'f': 6, 'd': 6, 'g': 11, 'a': 5, 'e': 5, 'c': 5},
    'L7.xes': {'a': 8, 'b': 11, 'c': 8},
    'billinstances.xes': {'write bill': 1800, 'print bill': 1800, 'deliver bill': 1800},
    'flyerinstances.xes': {'receive flyer order': 900, 'design flyer': 1809, 'send draft to customer': 1809, 'print flyer': 900, 'deliver flyer': 900},
    'posterinstances.xes': {'receive order and photo': 900, 'design photo poster': 900, 'print poster': 900, 'deliver poster': 900},
    'running-example.xes': {'register request': 6, 'examine casually': 6, 'check ticket': 9, 'decide': 9, 'reinitiate request': 3, 'examine thoroughly': 3, 'pay compensation': 3, 'reject request': 3}
}

direct_follows_freq = {
    'L1.xes': {('a', 'e'): 1, ('e', 'd'): 1, ('a', 'c'): 2, ('c', 'b'): 2, ('b', 'd'): 2, ('a', 'b'): 3, ('b', 'c'): 3, ('c', 'd'): 3},
    'L2.xes': {('a', 'c'): 7, ('c', 'b'): 9, ('b', 'd'): 6, ('b', 'e'): 3, ('e', 'f'): 7, ('f', 'b'): 5, ('b', 'c'): 11, ('c', 'd'): 7, ('a', 'b'): 6, ('c', 'e'): 4, ('f', 'c'): 2},
    'L3.xes': {('a', 'b'): 4, ('b', 'c'): 3, ('c', 'd'): 3, ('d', 'e'): 3, ('e', 'f'): 3, ('f', 'b'): 3, ('b', 'd'): 4, ('d', 'c'): 4, ('c', 'e'): 4, ('e', 'g'): 4},
    'L4.xes': {('a', 'c'): 83, ('c', 'd'): 87, ('b', 'c'): 64, ('c', 'e'): 60},
    'L5.xes': {('a', 'b'): 11, ('b', 'e'): 5, ('e', 'c'): 3, ('c', 'd'): 10, ('d', 'b'): 8, ('b', 'f'): 12, ('a', 'e'): 3, ('e', 'b'): 7, ('b', 'c'): 9, ('c', 'e'): 2, ('e', 'd'): 2, ('d', 'e'): 4, ('e', 'f'): 2},
    'L6.xes': {('b', 'f'): 4, ('f', 'd'): 4, ('d', 'g'): 4, ('b', 'd'): 2, ('d', 'f'): 2, ('f', 'g'): 2, ('a', 'e'): 3, ('e', 'c'): 3, ('c', 'g'): 3, ('a', 'c'): 2, ('c', 'e'): 2, ('e', 'g'): 2},
    'L7.xes': {('a', 'b'): 6, ('b', 'b'): 5, ('b', 'c'): 6, ('a', 'c'): 2},
    'billinstances.xes': {('write bill', 'print bill'): 1800, ('print bill', 'deliver bill'): 1800},
    'flyerinstances.xes': {('receive flyer order', 'design flyer'): 900, ('design flyer', 'send draft to customer'): 1809, ('send draft to customer', 'design flyer'): 909, ('send draft to customer', 'print flyer'): 900, ('print flyer', 'deliver flyer'): 900},
    'posterinstances.xes': {('receive order and photo', 'design photo poster'): 900, ('design photo poster', 'print poster'): 900, ('print poster', 'deliver poster'): 900},
    'running-example.xes': {('register request', 'examine casually'): 3, ('examine casually', 'check ticket'): 4, ('check ticket', 'decide'): 6, ('decide', 'reinitiate request'): 3, 
                            ('reinitiate request', 'examine thoroughly'): 1, ('examine thoroughly', 'check ticket'): 2, ('decide', 'pay compensation'): 3, 
                            ('register request', 'check ticket'): 2, ('check ticket', 'examine casually'): 2, ('examine casually', 'decide'): 2, ('register request', 'examine thoroughly'): 1, 
                            ('decide', 'reject request'): 3, ('reinitiate request', 'check ticket'): 1, ('reinitiate request', 'examine casually'): 1, ('check ticket', 'examine thoroughly'): 1, ('examine thoroughly', 'decide'): 1}
}

parallel_freq ={
    'L1.xes': {('c', 'b'): 2, ('b', 'c'): 2},
    'L2.xes': {('c', 'b'): 9, ('b', 'c'): 9},
    'L3.xes': {('c', 'd'): 3, ('d', 'c'): 3},
    'L4.xes': {},
    'L5.xes': {('b', 'e'): 5, ('e', 'b'): 5, ('e', 'c'): 2, ('c', 'e'): 2, ('e', 'd'): 2, ('d', 'e'): 2},
    'L6.xes': {('f', 'd'): 2, ('d', 'f'): 2, ('e', 'c'): 2, ('c', 'e'): 2},
    'L7.xes': {('b', 'b'): 5},
    'billinstances.xes': {},
    'flyerinstances.xes': {('design flyer', 'send draft to customer'): 909, ('send draft to customer', 'design flyer'): 909},
    'posterinstances.xes': {},
    'running-example.xes': {('examine casually', 'check ticket'): 2, ('check ticket', 'examine casually'): 2, ('examine thoroughly', 'check ticket'): 1, ('check ticket', 'examine thoroughly'): 1}
}

dependency_measures ={
    'L1.xes': {('a', 'e'): 0.5, ('e', 'd'): 0.5, ('a', 'c'): 0.67, ('c', 'b'): -0.17, ('b', 'd'): 0.67, ('a', 'b'): 0.75, ('b', 'c'): 0.17, ('c', 'd'): 0.75},
    'L2.xes': {('a', 'c'): 0.88, ('c', 'b'): -0.1, ('b', 'd'): 0.86, ('b', 'e'): 0.75, ('e', 'f'): 0.88, ('f', 'b'): 0.83, ('b', 'c'): 0.1, ('c', 'd'): 0.88, ('a', 'b'): 0.86, ('c', 'e'): 0.8, ('f', 'c'): 0.67},
    'L3.xes': {('a', 'b'): 0.8, ('b', 'c'): 0.75, ('c', 'd'): -0.12, ('d', 'e'): 0.75, ('e', 'f'): 0.75, ('f', 'b'): 0.75, ('b', 'd'): 0.8, ('d', 'c'): 0.12, ('c', 'e'): 0.8, ('e', 'g'): 0.8},
    'L4.xes': {('a', 'c'): 0.99, ('c', 'd'): 0.99, ('b', 'c'): 0.98, ('c', 'e'): 0.98},
    'L5.xes': {('a', 'b'): 0.92, ('b', 'e'): -0.15, ('e', 'c'): 0.17, ('c', 'd'): 0.91, ('d', 'b'): 0.89, ('b', 'f'): 0.92, ('a', 'e'): 0.75, ('e', 'b'): 0.15, ('b', 'c'): 0.9, ('c', 'e'): -0.17, ('e', 'd'): -0.29, ('d', 'e'): 0.29, ('e', 'f'): 0.67},
    'L6.xes': {('b', 'f'): 0.8, ('f', 'd'): 0.29, ('d', 'g'): 0.8, ('b', 'd'): 0.67, ('d', 'f'): -0.29, ('f', 'g'): 0.67, ('a', 'e'): 0.75, ('e', 'c'): 0.17, ('c', 'g'): 0.75, ('a', 'c'): 0.67, ('c', 'e'): -0.17, ('e', 'g'): 0.67},
    'L7.xes': {('a', 'b'): 0.86, ('b', 'b'): 0.83, ('b', 'c'): 0.86, ('a', 'c'): 0.67},
    'billinstances.xes': {('write bill', 'print bill'): 1.0, ('print bill', 'deliver bill'): 1.0},
    'flyerinstances.xes': {('receive flyer order', 'design flyer'): 1.0, ('design flyer', 'send draft to customer'): 0.33, ('send draft to customer', 'design flyer'): -0.33, ('send draft to customer', 'print flyer'): 1.0, ('print flyer', 'deliver flyer'): 1.0},
    'posterinstances.xes': {('receive order and photo', 'design photo poster'): 1.0, ('design photo poster', 'print poster'): 1.0, ('print poster', 'deliver poster'): 1.0},
    'running-example.xes': {('register request', 'examine casually'): 0.75, ('examine casually', 'check ticket'): 0.29, ('check ticket', 'decide'): 0.86, ('decide', 'reinitiate request'): 0.75, 
                            ('reinitiate request', 'examine thoroughly'): 0.5, ('examine thoroughly', 'check ticket'): 0.25, ('decide', 'pay compensation'): 0.75, ('register request', 'check ticket'): 0.67, 
                            ('check ticket', 'examine casually'): -0.29, ('examine casually', 'decide'): 0.67, ('register request', 'examine thoroughly'): 0.5, ('decide', 'reject request'): 0.75, 
                            ('reinitiate request', 'check ticket'): 0.5, ('reinitiate request', 'examine casually'): 0.5, ('check ticket', 'examine thoroughly'): -0.25, ('examine thoroughly', 'decide'): 0.5}
}

# =================  end  ==================