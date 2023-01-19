"""
This module implements heuristic mining algorithm mentioned in [1].
It converts the input event log, which is a two-dimenal array, to a Causal net (c net).

The algorithm first creates dependency graph using count of direct follows (>) and dependency measure (=>). 
Then the algorithm converts the dependency graph to a c net.

References
    ----------
    [1] Wil.M.P. van der Aalst, Process Mining: Data Science in Action, vol. 2, Springer, 2016, doi: 10.1007/978-3-662-49851-4.
    Chapter 3.2.7 and 7.2
"""

import graphviz, copy
import pandas as pd
import dataframe_image as dfi
from itertools import chain, combinations, permutations


# step_1:
def traces(event_log):
    """return a dictionary of trace-frequency pairs. Example taken from L1.xes: \n
    frequency_traces([[a, e, d], [a, c, b, d], [a, b, c, d], [a, b, c, d], [a, b, c, d], [a, c, b, d]]) --> {(a, e, d): 1, (a, c, b, d): 2, (a, b, c, d): 3}
    """
    frequency_trace = {}
    for log in event_log:
         if tuple(log) not in frequency_trace.keys():
            frequency_trace[tuple(log)] = 1
         else:
            frequency_trace[tuple(log)] = 1+frequency_trace[tuple(log)]
    return frequency_trace  
    
# step_2
def find_transitions(event_log):
    """return a dictionary of transition-frequency pairs. Example taken from L1.xes: \n
    find_transitions([[a, e, d], [a, c, b, d], [a, b, c, d], [a, b, c, d], [a, b, c, d], [a, c, b, d]]) --> {a: 6, e: 1, d: 6, c: 5, b: 5}
    """
    transitions = {}
    for trace in event_log:
        for event in trace:
            if event not in transitions:
                transitions[event] = 1
            else:
                transitions[event] = 1 + transitions[event]
    return transitions

# step_3:
def direct_follows(traces):
    """return a dictionary of directFollow-frequency pairs, e.g., {(a, b, c):3, (a, c, b): 2} --> {(a, b):3, (b, c): 3, (a,c): 2, (c,b): 2} """
    frequency_df = {}
    for trace in traces:
        for t in range(len(trace)-1):
            if (trace[t], trace[t+1]) not in frequency_df:
                frequency_df[(trace[t], trace[t+1])] = traces[trace]
            else:
                frequency_df[(trace[t], trace[t+1])] = traces[trace]+frequency_df[(trace[t], trace[t+1])]
    return frequency_df

# step_4:
def denpendency_measure(event_log):
    """return a dictionary of DirectFollow-DependencyMeasure pairs. Example taken from L1.xes: \n
    directfollows: {(a, e): 1, (e, d): 1, (a, c): 2, (c, b): 2, (b, d): 2, (a, b): 3, (b, c): 3, (c, d): 3}
    return: {(a, e): 0.5, (e, d): 0.5, (a, c): 0.67, (c, b): -0.17, (b, d): 0.67, (a, b): 0.75, (b, c): 0.17, (c, d): 0.75}
    """
    trace = traces(event_log)
    directFollows = direct_follows(trace)
    denpendency_measure = {}
    for pair in directFollows.keys():
        # implement the formula on page 204 in [1]:
        if pair[0] == pair[1] or (pair[1],pair[0]) not in directFollows.keys():
            denpendency_measure[pair] = (directFollows[pair])/(directFollows[pair]+1)
        else:
            denpendency_measure[pair] = (directFollows[pair]-directFollows[(pair[1],pair[0])])/(directFollows[pair]+directFollows[(pair[1],pair[0])]+1)
        denpendency_measure[pair] = round(denpendency_measure[pair],2)
    return denpendency_measure

def dm_matrix(event_log):
    """generate a dependency measure matrix """
    transitions = sorted(find_transitions(event_log).keys())
    dm = denpendency_measure(event_log)
    table = []
    for row in transitions:
        r = []
        for column in transitions:
            if (row, column) in dm:
                r.append(dm[(row, column)])
            elif (column, row) in dm:
                r.append(-dm[(column, row)])
            else:
                r.append(0)
        table.append(r)
    df = pd.DataFrame(table, columns=transitions, index=transitions)
    styles = [dict(selector="caption", props=[("text-align", "center"),("font-size", "15"),("color", 'dark')])]
    df = df.style.set_caption("Dependency Measure Matrix").set_table_styles(styles).format(precision=2)
    dfi.export(df, "../frontend/static/output/dm_matrix.png", table_conversion = 'matplotlib')
    # dfi.export(df, "frontend/static/output/dm_matrix.png", table_conversion = 'matplotlib')   # for server

# step_5:
def draw_denpendencyGraph(log, threshold_df=0, threshold_dm=0.0):
    """draw a dependency graph for the given event log."""
    transitions = find_transitions(log)
    t = traces(log)
    directFollows = direct_follows(t)
    dm = denpendency_measure(log)
    denpendencyGraph(transitions, directFollows, dm, threshold_df, threshold_dm)

def denpendencyGraph(transitions, directFollows, denpendency_measure, threshold_df=0, threshold_dm=0.0):
    """draw a dependency graph using graphviz.
    transitions: a dictionary of transition-frequency pairs
    directfollows: a dictionary of directFollow-frequency pairs
    denpendency_measure: a dictionary of DirectFollow-DependencyMeasure pairs
    threshold_df: threshold for direct follow frequency, given by the user. Default value is zero
    threshold_dm: threshold for dependency measure, given by the user. Default value is zero
    """
    g = graphviz.Digraph(format='png', filename='dependency_graph.gv')
    g.attr(rankdir = 'LR', height = '10', width='18',  nodesep = '0.5')
    # filter out the edges below the given thresholds
    _helper_DG_delete(directFollows, denpendency_measure, threshold_df, threshold_dm)
    g.attr('node', shape = 'rectangle', fontsize='18',width='0.7', fixedsize='false', ordering='in') # transitions in rectangle
    for t in sorted(transitions):
        g.node(t)
    # add edges between nodes 
    g.attr(rankdir = 'LR', height = '10', width='18',  nodesep = '0.5')
    g.attr('edge', arrowsize='0.6', fontsize='12', forcelabels='true') 
    if len(directFollows) != 0: 
        for edge in sorted(directFollows):
            g.edge(edge[0], edge[1], label = str(directFollows[edge]) + '(' + str(denpendency_measure[edge]) +')')
    # render a png file for the dependency graph
    g.render(directory ='../frontend/static/output', view = False)
    # g.render(directory ='frontend/static/output', view = False)   # for server

def _helper_DG_delete(frequency_df, denpendency_measure, threshold_df =0, threshold_dm =0.0):
    """delete directFollows and denpendency_measure pairs that are ≤ given threshold respectively"""
    delete = dict.fromkeys(frequency_df.keys(), 0)
    for k in frequency_df:
        if frequency_df[k] < threshold_df or denpendency_measure[k] < threshold_dm:
            delete[k] = 1
    for k in delete:
        if delete[k] == 1:
            del frequency_df[k] 
            del denpendency_measure[k] 

# extra function
def find_first_transitions(event_log):
    """return a set of all initial transitions. Example taken from L1.xes: \n
    find_first_transitions([[a, e, d], [a, c, b, d], [a, b, c, d], [a, b, c, d], [a, b, c, d], [a, c, b, d]]) --> {a}
    """
    intial_transitions = set()
    for case in event_log:
        if case[0] not in intial_transitions:
            intial_transitions.add(case[0])
    return intial_transitions   
  
# extra function
def find_last_transitions(event_log):
    """return a set of all last transitions. Example taken from L1.xes: \n
    find_last_transitions([[a, e, d], [a, c, b, d], [a, b, c, d], [a, b, c, d], [a, b, c, d], [a, c, b, d]]) --> {d}
    """
    last_transitions = set()
    for case in event_log:
        if case[-1] not in last_transitions:
            last_transitions.add(case[-1])
    return last_transitions

# ========= all the following methods serve for visualization of causal net ========

# step_6:
def draw_cnet(eventlog):
    """draw causal net by calling all relevant functions"""
    transitions = find_transitions(eventlog)
    trace = traces(eventlog)
    directFollows = direct_follows(trace)
    parallel = find_parallel_transitions(directFollows)

    input_bind = input_binding(eventlog)
    output_bind = output_binding(eventlog)
    in_bind_freq = in_binding_freq(trace, input_bind, directFollows)
    out_bind_freq = out_binding_freq(trace, output_bind, directFollows)
    inbind_labelled = label_input_binding(input_bind, in_bind_freq)
    outbind_labelled = label_output_binding(output_bind, out_bind_freq)
    
    nodes = nodes_on_cnet(transitions, directFollows, parallel, out_bind_freq, in_bind_freq, outbind_labelled, inbind_labelled)
    edges = edges_on_cnet(nodes, directFollows, parallel, outbind_labelled, inbind_labelled)
    cnet(nodes, edges, directFollows)

def input_transitions(transitions, direct_follows):
    """return all ingoing transitions of each transition. \n
    transitions: {a: 6, e: 1, d: 6, c: 5, b: 5} \n
    direct_follows: {(a, e): 1, (e, d): 1, (a, c): 2, (c, b): 2, (b, d): 2, (a, b): 3, (b, c): 3, (c, d): 3} \n
    return: {a: [], e: [a], d: [e, b, c], c: [a, b], b: [c, a]}
    """
    result = {}
    for t in transitions:
        input_arc = []
        for df in direct_follows:
            if t == df[1]:
                input_arc.append(df[0])
        result[t] = input_arc
    return result

def output_transitions(transitions, direct_follows):
    """return all outgoing transitions of each transition. \n
    transitions: {a: 6, e: 1, d: 6, c: 5, b: 5} \n
    direct_follows: {(a, e): 1, (e, d): 1, (a, c): 2, (c, b): 2, (b, d): 2, (a, b): 3, (b, c): 3, (c, d): 3} \n
    return: {a: [e, c, b], e: [d], d: [], c: [b, d], b: [d, c]}
    """
    result = {}
    for t in transitions:
        output_arc = []
        for df in direct_follows:
            if t == df[0]:
                output_arc.append(df[1])
        result[t] = output_arc
    return result

def potential_bindings(in_or_out_transitions):
    """create a powerset of the given input or output transitions for every key \n
    potential_bindings({a: [b,c], b:[d], c:[d], d:[]}) --> {a: [{b},{c},{b,c}], b:[{d}], c:[{d}], d:[]} 
    """
    result = {}
    for t in in_or_out_transitions:
        result[t] = _helper_powerset(in_or_out_transitions[t])
    return result

def _helper_powerset(iterable):
    """powerset([1,2,3]) --> [{1}, {2}, {3}, {1,2}, {1,3}, {2,3}, {1,2,3}]"""
    s = list(iterable)
    result = chain.from_iterable(combinations(s, r) for r in range(1,len(s)+1))
    return list(map(set, result))

def find_parallel_transitions(directfollows):
    """return a dictionary of parallel-frequency pairs, e.g., {(a, c): 2, (c, b): 2, (a, b): 3, (b, c): 3} --> {(c, b): 2, (b, c): 2}"""
    parallel = {}
    for t in directfollows.keys():
        if t not in parallel and (t[1],t[0]) in directfollows.keys():
            parallel[t] = min(directfollows[t], directfollows[(t[1],t[0])])
            parallel[(t[1],t[0])] = parallel[t]
    return parallel

def _helper_parallel_freq(parallel, single_transition):
    """return the first parallel pairs that contains the given single_transition. \n
    e.g., parallel_freq({(b, c): 10, (c, b): 10}, b) --> {(b, c): 10} or {(c, b): 10}
    """
    result = {}
    for p in parallel:
        if single_transition in p:
            result[p] = parallel[p]
            break
    return result

def input_binding(event_log):
    """draw causal net by calling all relevant functions"""
    transitions = find_transitions(event_log)
    trace = traces(event_log)
    directFollows = direct_follows(trace)
    parallel = find_parallel_transitions(directFollows)
    input_tran = input_transitions(transitions, directFollows)
    potential_in = potential_bindings(input_tran)
    input_bind = _helper_input_binding(potential_in, parallel, directFollows, trace)
    return dict(sorted(input_bind.items()))

def output_binding(event_log):
    """draw causal net by calling all relevant functions"""
    transitions = find_transitions(event_log)
    trace = traces(event_log)
    directFollows = direct_follows(trace)
    parallel = find_parallel_transitions(directFollows)
    output_tran = output_transitions(transitions, directFollows)
    potential_out = potential_bindings(output_tran)
    output_bind = _helper_output_binding(potential_out, parallel, directFollows, trace)
    return dict(sorted(output_bind.items()))

def _helper_input_binding(in_binding_potential, parallel, directfollows, trace):
    """return a dictionary of potential Transition-InputBinding pairs for all transitions. 
    in_binding_potential: powerset of ingoing transitions
    parallel: a dictionary of parallel-frequency pairs 
    directfollows: a dictionary of directFollow-frequency pairs \n
    Example for L1.xes: it should return {a: [], e: [{a}], d: [{e}, {c}, {c, b}], c: [{a}, {b}], b: [{a}]}
    """
    potential_copy = copy.deepcopy(in_binding_potential)
    for key in in_binding_potential.keys():
        temp_list = in_binding_potential.get(key)
        to_delete = [0]*len(temp_list)
        flatten = list(sum(parallel, ()))
        if len(temp_list) > 1:
            # marked the subset to be deleted with 1
            for t in temp_list:
                t2 = list(t)[0]
                if len(t) == 1 and (t2,key) in parallel and parallel[(t2,key)] == directfollows[(t2,key)] and t2!=key:
                    to_delete[temp_list.index(t)] = 1  
                elif len(t) == 1 and (t2,key) not in parallel and t2 in flatten and (t2,t2) not in parallel:
                    k = list(_helper_parallel_freq(parallel, t2))[0]
                    min_freq = min(directfollows[(k[0], key)], directfollows[(k[1], key)], parallel[k])
                    if directfollows[(t2,key)] == min_freq:
                        to_delete[temp_list.index(t)] = 1
                if len(t) > 1 and _helper_input_binding_delete(key,t,trace):
                    to_delete[temp_list.index(t)] = 1
            # delete subsets
            new_list = []
            for i in range(len(to_delete)):
                if to_delete[i] == 0:
                    new_list.append(temp_list[i])
            potential_copy[key] = new_list
    return potential_copy

def _helper_output_binding(out_binding_potential, parallel, directfollows, trace):
    """return a dictionary of potential Transition-InputBinding pairs for all transitions 
    out_binding_potential: powerset of it's outgoing transitions
    parallel: a dictionary of parallel-frequency pairs 
    directfollows: a dictionary of directFollow-frequency pairs \n
    Example for L1.xes: it should return {a: [{e}, {b}, {b, c}], e: [{d}], d: [], c: [{d}], b: [{d}, {c}]}
    """
    potential_copy = copy.deepcopy(out_binding_potential)
    for key in out_binding_potential: 
        temp_list = out_binding_potential.get(key)
        to_delete = [0]*len(temp_list)
        flatten = list(sum(parallel, ()))
        if len(temp_list) > 1:
            # marked the subset to be deleted with 1
            for t in temp_list:
                t2 = list(t)[0]
                if len(t) == 1 and (key,t2) in parallel and parallel[(key,t2)] == directfollows[(key,t2)] and t2!=key:
                    to_delete[temp_list.index(t)] = 1  
                elif len(t) == 1 and (key,t2) not in parallel and t2 in flatten and (t2,t2) not in parallel:
                    k = list(_helper_parallel_freq(parallel, t2))[0]
                    min_freq = min(directfollows[(key,k[0])], directfollows[(key,k[1])], parallel[k])
                    if directfollows[(key,t2)] == min_freq:
                        to_delete[temp_list.index(t)] = 1
                if len(t) > 1 and _helper_output_binding_delete(key,t,trace):
                    to_delete[temp_list.index(t)] = 1       
            # delete subsets
            new_list = []
            for i in range(len(to_delete)):
                if to_delete[i] == 0:
                    new_list.append(temp_list[i])
            potential_copy[key] = new_list
    return potential_copy

def _helper_output_binding_delete(key, binding_set, trace):
    """return true if the subString of key+binding_set is not found in the parentString of trace. \n
    e.g. (a, {b,e}, {(a, b, c, d): 4, (a, b, e, f): 2}) -> true (delete), because 'aeb' is not in any trace
    """
    permu = list(permutations(binding_set))
    for j in permu:
        subStr = key + ' ' + ' '.join(map(str, j))
        subStr_counter = 0
        for t in trace:
            parentStr = ' '.join(map(str, t))
            if subStr in parentStr:
                subStr_counter += trace[t]
        if subStr_counter == 0:
            return True
    return False

def _helper_input_binding_delete(key, binding_set, trace):
    """return true if the subString of key+binding_set is not found in the parentString of trace. \n
    e.g. (c, {b,e}, {(a, b, c, d): 4, (a, b, e, f): 2}) -> true (delete), because 'bec' and 'ebc' are not found in any trace.
    """
    permu = list(permutations(binding_set))
    for j in permu:
        subStr = ' '.join(map(str, j)) + ' ' + key 
        subStr_counter = 0
        for t in trace:
            parentStr = ' '.join(map(str, t))
            if subStr in parentStr:
                subStr_counter += trace[t]
        if subStr_counter == 0:
            return True
    return False

def cnet(nodes, edges, directFollows):
    """draw a causal net with given nodes and edges"""
    g = graphviz.Digraph(format='png', filename='cnet.gv')
    g.attr(rankdir = 'LR', height = '10', width='18',  nodesep = '0.5')
    for n in nodes:
        if '-' not in n:
            l = n +'\n'+ str(nodes[n])
            g.node(n, shape = 'rectangle', fontsize='22',width='0.8', label=l)
        else:
            g.node(n, shape = 'circle', fontsize='15',width='0.4', fillcolor='lightblue', style='filled',label=str(nodes[n]), fixedsize= 'True')
    for e in edges:
        if len(e)==3:
            g.edge(e[0],e[1], arrowhead = 'none', color='lightblue3',penwidth='2') # different color for binding edges
        elif e[0][-1] == 'o' or e[0][0]=='1' and '-' not in e[1]:
            g.edge(e[0],e[1])
        elif e[0]==e[1]:
            g.edge(e[0],e[1], label=str(directFollows[e]))
        elif e[0][0] == 'o' or e[1][-1] == 'o':
            g.edge(e[0],e[1], arrowhead = 'none', minlen= '5')
        else:
            g.edge(e[0],e[1], arrowhead = 'none')
    g.render(directory ='../frontend/static/output', view = False)
    # g.render(directory ='frontend/static/output', view = False)   for server

def out_binding_freq(trace, out_binding, directFollows):
    """mark the binding nodes with their frequencies. Example from L1.xes: \n
    trace: {(a, e, d): 1, (a, c, b, d): 2, (a, b, c, d): 3} \n
    out_binding:  {a: [{e}, {b}, {b, c}], e: [{d}], d: [], c: [{d}], b: [{d}, {c}]} \n
    directFollows: {(a, e): 1, (e, d): 1, (a, c): 2, (c, b): 2, (b, d): 2, (a, b): 3, (b, c): 3, (c, d): 3} \n
    return: {a: [({e}, 1), ({b}, 1), ({b, c}, 4)], e: [({d}, 1)], d: [], c: [({d}, 3)], b: [({d}, 2), ({c}, 3)]}
    """
    str_trace = _helper_key_to_string(trace)
    # find the min frequency of all binding string whose order ≥ 2
    min_freq = {}
    for key in out_binding:
        temp_freq = [] 
        for subset in out_binding[key]:
            if len(subset)>1:
                permu = list(permutations(subset))
                # find freq for each permutation
                permu_freq = {}
                for p in permu:
                    subStr = key + ' ' + ' '.join(map(str, p))
                    for parentString in str_trace:
                        index=0
                        while index<len(parentString) and subStr in parentString[index:]:
                            if p in permu_freq:
                                permu_freq[p] = str_trace[parentString] + permu_freq[p]
                            else:
                                permu_freq[p] = str_trace[parentString]
                            index += parentString.index(subStr) + len(subStr)
                min_pair = min(permu_freq.items(), key=lambda x: x[1])
                temp_freq.append(min_pair)
        min_freq[key]= dict(temp_freq)
    # calculate frequency for every binding
    result = {}
    for key in out_binding:
        list1 = []
        for subset in out_binding[key]:
            if len(subset) == 1:
                total_freq = directFollows[(key,list(subset)[0])]
                if len(min_freq[key]) > 0:
                    for key2 in min_freq[key]:
                        if list(subset)[0] in key2:
                            total_freq -= min_freq[key][key2]
                list1.append((subset, total_freq))
            else:
                for key2 in min_freq[key]:
                    if set(key2) == subset:
                        list1.append((subset, min_freq[key][key2] * len(subset)))
        result[key] = list1
    return result

def in_binding_freq(trace, in_binding, directFollows):
    """mark the binding nodes with their frequencies. Example: \n
    trace: {(a, e, d): 1, (a, c, b, d): 2, (a, b, c, d): 3} \n
    in_binding:  {a: [], e: [{a}], d: [{e}, {c}, {b, c}], c: [{a}, {b}], b: [{a}]} \n
    directFollows: {(a, e): 1, (e, d): 1, (a, c): 2, (c, b): 2, (b, d): 2, (a, b): 3, (b, c): 3, (c, d): 3} \n
    return: {a: {a: [], e: [({a}, 1)], d: [({e}, 1), ({c}, 1), ({b, c}, 4)], c: [({a}, 2), ({b}, 3)], b: [({a}, 3)]}
    """
    str_trace = _helper_key_to_string(trace)
    # find the freq of all binding string whose order ≥ 2
    min_freq = {}
    for key in in_binding:
        temp_freq = [] 
        for subset in in_binding[key]:
            if len(subset)>1:
                permu = list(permutations(subset))
                # find freq for each permutation
                permu_freq = {}
                for p in permu:
                    subStr = ' '.join(map(str, p)) +' '+ key
                    for parentString in str_trace:
                        index=0
                        while index<len(parentString) and subStr in parentString[index:]:
                            if p in permu_freq:
                                permu_freq[p] = str_trace[parentString] + permu_freq[p]
                            else:
                                permu_freq[p] = str_trace[parentString]
                            index += parentString.index(subStr) + len(subStr)
                min_pair = min(permu_freq.items(), key=lambda x: x[1])
                temp_freq.append(min_pair)
        min_freq[key]= dict(temp_freq)
    # calculate frequency for every binding
    result = {}
    for key in in_binding:
        list1 = []
        for subset in in_binding[key]:  
            if len(subset) == 1:
                total_freq = directFollows[(list(subset)[0], key)] 
                if len(min_freq[key]) > 0:
                    for key2 in min_freq[key]:
                        if list(subset)[0] in key2:
                            total_freq -= min_freq[key][key2]
                list1.append((subset, total_freq))
            else:
                for key2 in min_freq[key]:
                    if set(key2) == subset:
                        list1.append((subset, min_freq[key][key2] * len(subset)))
        result[key] = list1
    return result

def _helper_key_to_string(trace):
    """convert trace to string. e.g., {(a, b, e, c, d, b, f): 3, (a, b, e, f): 2} -> {'a b e c d b f': 3, 'a b e f': 2}"""
    str_trace = {}
    for t in trace:
            str_key = ' '.join(map(str, t))
            str_trace[str_key] = trace[t]
    return str_trace

def label_output_binding(out_binding, out_binding_freq):
    """label only the output binding nodes with the order, in which it apprears in the out_bind. 
    DirectFollow arcs without binding are ommitted. Example taken from L1.xes: \n
    out_binding: {a: [{e}, {b}, {b, c}], e: [{d}], d: [], c: [{d}], b: [{d}, {c}]} \n
    out_binding_freq: {a: [({e}, 1), ({b}, 1), ({b, c}, 4)], e: [({d}, 1)], d: [], c: [({d}, 3)], b: [({d}, 2), ({c}, 3)]} \n
    return: {a: [[[a-b1], 1], [[a-b2, a-c1], 4]], e: [], d: [], c: [], b: []}
    """
    out_freq = _helper_freq(out_binding)
    out_bind = _helper_set_to_list(out_binding_freq)
    # label binding nodes
    for key in out_freq:
        for i in out_freq[key]:
            j=1
            for k in out_bind[key]:
                if out_freq[key][i] == 1 and i in k[0] and len(k[0])==1: # direct follow arc without black dots
                    k[0]=[]
                else: 
                    for t in range(len(k[0])):
                        if i==k[0][t]:
                            k[0][t] = key+'-'+i+str(j)
                            j += 1 
    # remove direct follow arcs that have no black dots
    result = {}
    for key in out_bind:
        l = []
        for pair in out_bind[key]:
            if len(pair[0]) !=0 and pair[1] !=0:  # special case pair[1]!=0: exclude freq=1
                l.append(pair)
        result[key] = l
    return result

def label_input_binding(in_binding, in_binding_freq):
    """label only the input binding nodes with the order, in which it apprears in the in_bind. 
    DirectFollow arcs without binding are ommitted. Example taken from L1.xes: \n
    in_binding: {a: [], e: [{a}], d: [{e}, {c}, {b, c}], c: [{a}, {b}], b: [{a}]} \n
    in_binding_freq: {a: {a: [], e: [({a}, 1)], d: [({e}, 1), ({c}, 1), ({b, c}, 4)], c: [({a}, 2), ({b}, 3)], b: [({a}, 3)]} \n
    return: {a: [], e: [], d: [[[1c-d], 1], [[1b-d, 2c-d], 4]], c: [], b: []} 
    """
    out_freq = _helper_freq(in_binding)
    in_bind = _helper_set_to_list(in_binding_freq)
    # label binding nodes
    for key in out_freq:
        for i in out_freq[key]:
            j=1
            for k in in_bind[key]:
                 if out_freq[key][i] == 1 and i in k[0] and len(k[0])==1: # direct follow arc without black dots
                    k[0]=[]
                 else:
                    for t in range(len(k[0])):
                        if i==k[0][t]:
                            k[0][t] = str(j)+i+'-'+key
                            j += 1 
    result = {}
    for key in in_bind:
        l = []
        for pair in in_bind[key]:
            if len(pair[0]) !=0 and pair[1] !=0:
                l.append(pair)
        result[key] = l
    return result

def _helper_freq(bindings):
    """calculate the frequencies of transitions in the bindings. \n
    _freq({a: [{b},{d},{c,d}, {b,c,d}], e: [{b},{d},{c,d},{b,c,d}]}) --> {a: {c: 2, d: 3, b: 2}, e: {c: 2, d: 3, b: 2}}
    """
    freq = {}
    for key in bindings:
        sub_freq = {}
        flatt =  [t for subset in bindings[key] for t in subset]
        s = set(flatt)
        for i in s:
            appear = 0
            for j in flatt:
                if i==j:
                    appear += 1
                sub_freq[i] = appear
        freq[key] = sub_freq
    return freq

def _helper_set_to_list(binding_freq):
    """convert for example {'a': [({'b'}, 8)} to {'a': [['b'], 8]}"""
    out_bind = {}
    for key in binding_freq:
        li = []
        for tuple in binding_freq[key]:
            l = list(tuple)
            l[0] = list(l[0])
            li.append(l)
        out_bind[key] = li
    return out_bind

def nodes_on_cnet(transitions, directFollows, parallel, out_binding_freq, in_binding_freq, output_bind_labelled, input_bind_labelled):
    """create nodes for the causal net. Example taken from L1.xes \n
    transitions: {a: 6, e: 1, d: 6, c: 5, b: 5} \n
    directFollows: {(a, e): 1, (e, d): 1, (a, c): 2, (c, b): 2, (b, d): 2, (a, b): 3, (b, c): 3, (c, d): 3} \n
    parallel: {(c, b): 2, (b, c): 2} \n
    out_binding_freq: {a: [({e}, 1), ({b}, 1), ({b, c}, 4)], e: [({d}, 1)], d: [], c: [({d}, 3)], b: [({d}, 2), ({c}, 3)]} \n
    in_binding_freq: {a: [], e: [({a}, 1)], d: [({e}, 1), ({c}, 1), ({b, c}, 4)], c: [({a}, 2), ({b}, 3)], b: [({a}, 3)]} \n
    output_bind_labelled: {a: [[[a-b1], 1], [[a-c1, a-b2], 4]], e: [], d: [], c: [], b: []} \n
    input_bind_labelled: {a: [], e: [], d: [[[1c-d], 1], [[2c-d, 1b-d], 4]], c: [], b: []} \n
    return: {a: 6, e: 1, d: 6, c: 5, b: 5, a-b1: 1, a-c1: 4, a-b2: 4, 1c-d: 1, 2c-d: 4, 1b-d: 4, a-e-i: 1, a-e-o: 1, e-d-i: 1, e-d-o: 1, a-co: 4, ob-d: 4, a-bo: 5, oc-d: 5}
    """
    nodes = transitions
    # add binding nodes onto output arcs
    for key in output_bind_labelled:
        for pair in output_bind_labelled[key]:
            if not _helper_contain_parallel(pair, parallel): # bug fix for L5
                for pair_0 in pair[0]:
                    nodes[pair_0] = pair[1]
    # add binding nodes onto input arcs
    for key in input_bind_labelled:
        for pair in input_bind_labelled[key]:
            if not _helper_contain_parallel(pair, parallel): # bug fix for L5
                for pair_0 in pair[0]:
                    if pair_0[1:]+pair_0[0] not in nodes: # aviod dulpicates
                        nodes[pair_0] = pair[1]
    # add non binding nodes
    for df in directFollows:
        if df in parallel:
            pass
        elif df[0]+'-'+df[1]+'1' in nodes: # on output arc
            binded_freq = 0
            for pair in out_binding_freq[df[0]]:
                if len(pair[0])>1 and df[1] in pair[0]:
                    binded_freq += int(pair[1]/2)
            nodes[df[0]+'-'+df[1]+'o'] = directFollows[df]+binded_freq
        elif '1'+df[0]+'-'+df[1] in nodes:   # on input arc
            binded_freq = 0
            for pair in in_binding_freq[df[1]]:
                if len(pair[0])>1 and df[0] in pair[0]:
                    binded_freq += int(pair[1]/2)
            nodes['o'+df[0]+'-'+df[1]] = directFollows[df]+binded_freq
        else:  # no binding nodes on this direct follow arcs
            nodes[df[0]+'-'+df[1]+'-'+'i'] = nodes[df[0]+'-'+df[1]+'-'+'o'] = directFollows[df]
    return nodes

def _helper_contain_parallel(pair, parallel):
    """return true if binding list contains transition that is parallel with the key"""
    for i in pair[0]:
        index = i.index('-')
        if i[0].isnumeric() and (i[1:index], i[index+1:]) in parallel:   #input binding nodes like 1e-b
            return True
        elif i[-1].isnumeric() and (i[0:index],i[index+1:-1]) in parallel:  #output binding nodes like b-e1
            return True
    return False

def edges_on_cnet(nodes, directFollows, parallel, output_bind_labelled, input_bind_labelled):
    """create edges for the causal net. Example taken from L1.xes: \n
    return: [('1b-d', 'd'), ('1c-d', 'd'), ('2c-d', '1b-d', 'bind'), ('2c-d', '1c-d'), ('a', 'a-e-i'), ('a', 'a-b1'), ('a', 'a-c1'), 
    ('a-b1', 'a-b2'), ('a-b2', 'a-bo'), ('a-bo', 'b'), ('a-c1', 'a-b2', 'bind'), ('a-c1', 'a-co'), ('a-co', 'c'), ('a-e-i', 'a-e-o'), 
    ('a-e-o', 'e'), ('b', 'ob-d'), ('c', 'oc-d'), ('e', 'e-d-i'), ('e-d-i', 'e-d-o'), ('e-d-o', 'd'), ('ob-d', '1b-d'), ('oc-d', '2c-d')]
    [('2c-d', '1b-d', 'bind'), ('a-c1', 'a-b2', 'bind')]
    """
    edges = set()
    # connect nodes on direct follow arcs
    for df in directFollows:
        if df[0]==df[1]:
            edges.add(df)
        elif df in parallel:
            pass
        elif df[0]+'-'+df[1]+'-'+'i' in nodes: # direct follow arcs without binding on it
            edges.add((df[0], df[0]+'-'+df[1]+'-'+'i'))
            edges.add((df[0]+'-'+df[1]+'-'+'i',df[0]+'-'+df[1]+'-'+'o'))
            edges.add((df[0]+'-'+df[1]+'-'+'o',df[1]))
        elif df[0]+'-'+df[1]+'1' in nodes: # output arc with binding
            j = 1
            label = df[0]+'-'+df[1]
            while True:  # connect blue dots on output arcs
                if j==1:  
                    edges.add((df[0],label+str(j))) # (a,a-b1)
                elif j > 1 and label+str(j) in nodes:
                    edges.add((label+str(j-1),label+str(j)))  # (a-b1, a-b2).
                else:
                    edges.add((label+str(j-1),label+'o')) # (a-b2, a-bo)
                    edges.add((label+'o',df[1])) # (a-bo,b)
                    break
                j += 1  
        elif '1'+df[0]+'-'+df[1] in nodes: # input arc with binding
                j = 1
                label = df[0]+'-'+df[1]
                while True:  #  connect blue dots on input arcs
                    if j==1:  
                        edges.add((str(j)+label, df[1])) # (1b-e,e)
                    elif j > 1 and str(j)+label in nodes:
                        edges.add((str(j)+label, str(j-1)+label))  # (2b-e, 1b-e)
                    else:                      
                        edges.add(('o'+label, str(j-1)+label)) # (ob-e, 2b-e)
                        edges.add((df[0],'o'+label)) # (b,ob-e)
                        break
                    j += 1  
    # connect nodes that are binded as parallel pairs
    edges.update(_helper_bind(parallel, output_bind_labelled, input_bind_labelled)) 
    return sorted(edges, key=lambda x:x[0])
    
def _helper_bind(parallel, input_bind_labelled, output_bind_labelled):
    """connect the binding nodes. Example taken from L1.xes: \n
    parallel: {(c, b): 2, (b, c): 2} \n
    output_bind_labelled: {a: [[[a-b1], 1], [[a-b2, a-c1], 4]], e: [], d: [], c: [], b: []} \n
    input_bind_labelled: {a: [], e: [], d: [[[1c-d], 1], [[1b-d, 2c-d], 4]], c: [], b: []} \n
    return: [(a-b2, a-c1, bind), (1b-d, 2c-d, bind)]
    """
    edges = []
    for key in input_bind_labelled:
        for i in input_bind_labelled[key]:
            if len(i[0]) > 1 and not _helper_contain_parallel(i, parallel):
                for j in range(len(i[0])-1):
                    # 'bind' serves as an identifier of binding edges and later a different color used in method 'cnet'
                    edges.append((i[0][j],i[0][j+1],'bind'))  
    for key in output_bind_labelled:
        for i in output_bind_labelled[key]:
          if len(i[0]) > 1 and not _helper_contain_parallel(i, parallel):
                for j in range(len(i[0])-1):
                    edges.append((i[0][j],i[0][j+1],'bind')) 
    return edges
