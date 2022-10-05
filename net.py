import networkx as nx
from pygraphviz import *
import time


url = "http://134.122.18.168:2000/getData?amount=50"

while True: 
    r = requests.get(url, stream=True)
    
    if r.encoding is None:
        r.encoding = 'utf-8'
    
    for line in r.iter_lines(decode_unicode=True):
        if line:
            node_indices  = []
            for l in json.loads(line):
                p = eval(l['proximity'])
                for e in p:
                    #node_indices.append((l['moodid'],e['id'], {'weight': 10**((-69+e['distance'])/20)})) 
                    node_indices.append((l['moodid'],e['id'],  10**((-69+e['distance'])/20))) 
    
    fixedpos = {'mb01':(0,0), 'mb02':(1,1)} 
    node_d ={}
    for e in node_indices:
        if (e[0],e[1]) not in node_d:
            node_d[e[0],e[1]] = e[2]
    node_l = []
    
    for e in node_d:
        node_l.append((e[0], e[1], node_d[e]))
    
    A = AGraph()
    
    for e in node_l:
        A.add_edge(e[0],e[1],len=e[2])
        
    G = nx.nx_agraph.from_agraph(A)
    pos = nx.nx_agraph.graphviz_layout(G)
    #print(pos)
    
    pos_l = [(e, pos[e][0], pos[e][1]) for e in pos]
    purl = "http://134.122.18.168:2000/setBL?beacons="+str(pos_l)
    
    r = requests.get(purl)
    
    
            
            
    #print(pos_l)
        
    
    #nx.draw(G, pos, with_labels=True)    
    time.sleep(2)