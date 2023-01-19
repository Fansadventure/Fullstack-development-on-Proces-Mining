"""
This module implements the 8 steps of the alpha miner mentioned in [1] and [2].
It converts the input event log, which is a two-dimenal array, to a Petri net.

The algorithm first creates direct follow abstraction (>). For example, from a trace of 
the form <...a,b,...>, I observe the direct follow relation a>b, which means activity a 
is directly followed by activity b. From the direct follows relations, the relations 
parallelism (||), choice (x) and causality (->) are deduced.
These relations help to find the places and flows which are nodes and edges respectively in the petri net.

References
    [1] Wil.M.P. van der Aalst, Process Mining: Data Science in Action, vol. 2, Springer, 2016, doi: 10.1007/978-3-662-49851-4.
    [2] Wil M. P. van der Aalst et al., Workflow Mining: Discovering Process Models from Event Logs,
        IEEE Transactions on Knowledge and Data Engineering, vol.16, no. 9, 1128-1142, 2004. `DOI <https://doi.org/10.1109/TKDE.2004.47>`_.
"""

import graphviz
import pandas as pd
import dataframe_image as dfi

# step_1
def find_transitions(event_log):
    """return a set of transitions.
    event_log: 2D-array of transitions   
    """
    transitions = set()
    for case in event_log:
        for event in case:
            if event not in transitions:
                transitions.add(event)
    return transitions

# step_2
def find_intial_transitions(event_log):
    """return a set of all initial transitions.
    event_log: 2D-array of transitions  
    """
    intial_transitions = set()
    for case in event_log:
        if case[0] not in intial_transitions:
            intial_transitions.add(case[0])
    return intial_transitions   
  
# step_3:
def find_last_transitions(event_log):
    """return a set of all last transitions.
    event_log: 2D-array of transitions 
    """
    last_transitions = set()
    for case in event_log:
        if case[-1] not in last_transitions:
            last_transitions.add(case[-1])
    return last_transitions

# step_4:
def find_AB_pairs(event_log):
    """return a list of AB-pairs, e.g. [({a},{b}), ({c},{d})].
    event_log: 2D-array of transitions 
    """
    transitions = find_transitions(event_log)
    direct_follows = _direct_follows(event_log)
    a = _simpify_choice(_choice(transitions, direct_follows))
    b = a
    c = _causality(direct_follows)
    last = find_last_transitions(event_log)
    pairs = []
    for s1 in a:
        for s2 in b:
            not_Choice = 0
            for i in s1:
                for j in s2:
                    if (i,j) not in c:
                        not_Choice += 1   
            if not_Choice == 0:
                pairs.append((s1, s2))     
    return pairs


# ============ helpers for step_4 start ============ 

def _direct_follows(event_log):
    """return a set of direct-follow tuples, e.g. {(a,b)}.  
    event_log: 2D-array of transitions 
    """
    direct_follows = set()
    for case in event_log:
        for event_id in range(len(case)-1):
            if (case[event_id],case[event_id+1]) not in direct_follows:
                direct_follows.add((case[event_id],case[event_id+1]))
    return direct_follows

def _causality(direct_follows):
    """return a set of causality tuples, e.g. {(a,b)}.
    direct_follows: set of direct-follow tuples 
    """
    cause = set()
    for t in direct_follows:
        if (t[1],t[0]) not in direct_follows:
            cause.add(t)
    return cause

def _choice(transitions, direct_fllows):
    """return a set of choice tuples, e.g. {(a,b)}.
    transitions: set of transitions
    direct_follows: set of direct-follow tuples 
    """
    choice = set()
    for t in transitions:
        for l in transitions:
            if (t,l) not in direct_fllows and (l,t) not in direct_fllows:
                choice.add((t,l))
                choice.add((l,t))
    return choice

def _parallel(direct_fllows):
    """return a set of parallel tuples e.g. {(a,b)}.
    direct_follows: set of direct-follow tuples 
    """
    parallel = set()
    for t in direct_fllows:
        if (t[1],t[0]) in direct_fllows:
            parallel.add(t)
            parallel.add((t[1],t[0]))
    return parallel

def _simpify_choice(choice):
    """return a list of simplified choice sets. 
    Example: _simpify_choice({(a, a), (a, d), (d, a)}) --> [{a}, {a, d}]
    """
    simplified_choice = []
    for t in choice:
        if t[0] == t[1] and {t[0]} not in simplified_choice:
            simplified_choice.append({t[0]})
        elif {t[0], t[1]} not in simplified_choice :
            simplified_choice.append({t[0], t[1]})
    return simplified_choice

# ============ helper methods end ============  

# step_5:
def delete_subsets(AB_pairs):
    """return a list of max AB-pairs.
    AB_pairs: a list of AB-pairs
    Example: [({a}, {b}), ({a}, {b,e}), ({a}, {e})] --> [({a}, {b,e})]
    """
    to_delete = [0]*len(AB_pairs) 
    max_set = []
    # find the to-delete minimal subset and mark 1 at its index   
    for p in AB_pairs:
        for q in AB_pairs:
            if p[1]==q[1]:
                if p[0].issubset(q[0]) and len(p[0])<len(q[0]):
                    to_delete[AB_pairs.index(p)] = 1
                if q[0].issubset(p[0]) and len(p[0])>len(q[0]):
                    to_delete[AB_pairs.index(q)] = 1
            if p[0] == q[0]:
                if p[1].issubset(q[1]) and len(p[1])<len(q[1]):
                 to_delete[AB_pairs.index(p)] = 1   
                if q[1].issubset(p[1]) and len(p[1])>len(q[1]):
                 to_delete[AB_pairs.index(q)] = 1
    # delete the subsets which is marked as 1
    for i in range(len(to_delete)):
        if to_delete[i]==0:
            max_set.append(AB_pairs[i])
    return max_set

# Step_6
def add_places(AB_pairs_min):
    """return a list of places without quotation mark in between.
    AB_pairs_min: a list of minimized(no subsets) AB-pairs
    Return example: [p({a},{b,e}), p({a},{c,e}), iL, oL]
    """
    places = []
    for i in AB_pairs_min:
        i_0 = sorted(i[0])
        i_1 = sorted(i[1])
        s_0 = '{'
        s_1 = '{'
        for t in i_0:
            s_0 += t
            if i_0.index(t) < len(i_0) -1:
                s_0 += ','
            else:
                s_0 += '}'
        for t in i_1:
            s_1 += t
            if i_1.index(t) < len(i_1) -1:
                s_1 += ','
            else:
                s_1 += '}'
        places.append('p(' + s_0 + ',' + s_1 +')')
    places.append('iL')
    places.append('oL')
    return places

# step_7:
def add_flows(initial, last, AB_pairs_min, places):
    """return a list of flows (edges).
    initial/last: set of transitions
    AB_pairs_min: a list of minimized(no subsets) AB-pairs
    places: list of places
    Return example: [(iL, a), (a, p({a},{b})), (p({a},{b}), b), (d, oL)]
    """
    flows = []
    for i in initial:
        flows.append(('iL', i))
    for i in range(len(AB_pairs_min)):
        for j in AB_pairs_min[i][0]:
            for k in AB_pairs_min[i][1]:
                # the same arrow shouldn't be added twice
                if (j, places[i]) not in flows:
                    flows.append((j, places[i]))
                if (places[i], k) not in flows:
                    flows.append((places[i], k))
    for i in last:
        flows.append((i, 'oL'))
    return flows

# step_8:
def draw_petri_net(event_log):
    """generate a Petri net as a png image."""
    tran = find_transitions(event_log)
    initial = find_intial_transitions(event_log)
    last = find_last_transitions(event_log)
    pairs = find_AB_pairs(event_log);  
    subSet = delete_subsets(pairs)
    places = add_places(subSet)
    flows = add_flows(initial,last,subSet,places)
    petri_net(tran, places, flows)

def petri_net(transitions, places, flows):
    """draw a Petri net using graphviz.
    places: list of places
    flows: list of flows (edges)
    """
    g = graphviz.Digraph(format='png', filename='petri_net.gv')
    g.attr(rankdir = 'LR', height = '12', width='15',  nodesep = '0.8')
    # add rectangle nodes as transitions(activities)
    g.attr('node', shape = 'rectangle', width='0.8', fixedsize='false', ordering='in')
    for t in sorted(transitions):
        g.node(t, fontsize='22')
    # add circle nodes as places
    g.attr('node', shape = 'circle', width='0.3', label='', forcelabels='true', fixedsize='true', ordering='out')
    graph_label = ''
    for p in places:
        if p == 'iL':
            g.node(p, xlabel='<i<sub>L</sub>>')
        elif p == 'oL':
            g.node(p, xlabel='<o<sub>L</sub>>') 
        else:
            g.node(p, label= 'p' + str(places.index(p)))
            graph_label += 'p' + str(places.index(p)) + ': ' + p +' '
            
    g.attr('edge', arrowsize='0.6', forcelabels='true')
    flows.sort()
    g.edges(flows)
    if len(places)-2 >3:
        break_at = graph_label.index('p'+ str(len(places)//2-1))
        graph_label = graph_label[0: break_at] + '\n' + graph_label[break_at:]
    g.attr(overlap='false')
    g.attr(label='Places: '+ graph_label, fontsize='19' ) 
    g.render(directory ='../frontend/static/output', view = False)
    # g.render(directory ='frontend/static/output', view = False)   # for server

# help method to compare if two array are equal if order of elements is not considered
def is_equal(actual, expected):
    """compare if two arrays are equal when order is not considered. return true if equal, false otherwise
    actual/expected: list of pair tulpes
    example: [({a}, {b}), ({a}, {c})] == [({a}, {c}), ({a}, {b})] since order of the list is not considered
    """
    # idea: just like sets, if two list of sets are equal, every element of one list should also 
    # be in the other. In other words, the number of element which is not in the other list is 0.
    if len(actual) != len(expected):
        return False
    not_in_expected = 0
    for i in actual:
        if i not in expected:
            not_in_expected += 1
    not_in_actual = 0
    for i in expected:
        if i not in actual:
            not_in_actual += 1
    return not_in_expected == not_in_actual == 0

# additional funtion
def footprint_matrix(event_log):
    """generare a footprint matrix for the user-uploaded event log"""
    transitions = sorted(find_transitions(event_log))
    df = _direct_follows(event_log)
    causality = _causality(df)
    choice = _choice(transitions, df)
    parallel = _parallel(df)
    table =[]
    for row in transitions:
        r = []
        for column in transitions:
            if (row,column) in causality:
                r.append('→')
            elif (column,row) in causality:
                r.append('←') 
            elif (row,column) in choice:
                r.append('#')
            elif (row,column) in parallel:
                r.append('||')
        table.append(r)
    df = pd.DataFrame(table, columns=transitions, index=transitions)
    styles = [dict(selector="caption", props=[("text-align", "center"),("font-size", "15"),("color", 'dark')])]
    df = df.style.set_caption("The Footprint Matrix").set_table_styles(styles)
    dfi.export(df,"../frontend/static/output/footprint_matrix.png", table_conversion = 'matplotlib')
    # dfi.export(df,"frontend/static/output/footprint_matrix.png", table_conversion = 'matplotlib')  # for server
    