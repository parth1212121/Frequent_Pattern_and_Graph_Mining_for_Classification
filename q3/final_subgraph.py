import igraph as ig
import hashlib
import math
import sys

class GraphProcessor:
    def __init__(self):
        self.graphs = dict() 

    def read_graph_file(self, filepath):

        with open(filepath, 'r') as f:
            lines = f.readlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue
            if line.startswith('#'):
                freq = int(line.split()[1])
                i += 1
                g = ig.Graph()
                edges = []
                edge_labels = []
                transaction_id = None
                while i < len(lines) and lines[i].strip():
                    parts = lines[i].strip().split()
                    
                    if parts[0] == 't':
                        transaction_id = int(parts[1])
                    elif parts[0] == 'v':
                        node_id = int(parts[1])
                        label = int(parts[2])
           
                        while len(g.vs) <= node_id:
                            g.add_vertex()
                        g.vs[node_id]['label'] = label
                    elif parts[0] == 'e':  
                        src = int(parts[1])
                        dst = int(parts[2])
                        edge_label = int(parts[3])
                        edges.append((src, dst))
                        edge_labels.append(edge_label)
                    else:
                        break
                    i += 1

                g.add_edges(edges)

                g.es['label'] = edge_labels
                
                
                canonical_label = self.get_canonical_label(g)
                self.graphs[transaction_id]=(g, freq,canonical_label)   
               
    
    def get_canonical_label(self, graph):

        vertex_labels = [v['label'] for v in graph.vs]
        canonical_perm = graph.canonical_permutation(color=vertex_labels)
    
        canonical_graph = graph.permute_vertices(canonical_perm)
        canon_str = []

        vertex_info = sorted([(v.index, v['label']) for v in canonical_graph.vs])
        canon_str.extend(f"v{idx}_{label}" for idx, label in vertex_info)
        
        edge_info = []
        for e in canonical_graph.es:
            source, target = sorted([e.source, e.target]) 
            edge_info.append((source, target, e['label']))
        edge_info.sort() 
        canon_str.extend(f"e{src}_{tgt}_{label}" for src, tgt, label in edge_info)
        canonical_str = "_".join(map(str, canon_str))



        return hashlib.sha256(canonical_str.encode()).hexdigest()


def main():
    if len(sys.argv) < 1:
        raise ValueError("Not enough arguments")


 
    PATH_DISCRIMINATIVE_SUBGRAPHS = sys.argv[1]

    processor_0 = GraphProcessor()
    processor_0.read_graph_file("./data/gaston_graph0_output.txt")

    processor_1 = GraphProcessor()
    processor_1.read_graph_file("./data/gaston_graph1_output.txt")
    final_graphs_0 = dict()
    final_graphs_1 = dict()

    final_graphs = dict()
    for graph1 in processor_1.graphs.keys():
        final_graphs[processor_1.graphs[graph1][2]] = [processor_1.graphs[graph1][0]]
        final_graphs_1[processor_1.graphs[graph1][2]] = (processor_1.graphs[graph1][0],processor_1.graphs[graph1][1])
        
    for graph0 in processor_0.graphs.keys():

        final_graphs[processor_0.graphs[graph0][2]] = [processor_0.graphs[graph0][0]]
        final_graphs_0[processor_0.graphs[graph0][2]] = (processor_0.graphs[graph0][0],processor_0.graphs[graph0][1])      
        

    # final_graph : cannonical label -> [(graph,freq)]

    top_sorted_graphs_1 = []
    top_sorted_graphs_0 = []


    for graph_id in final_graphs_0.keys():
        if graph_id in final_graphs_1.keys():
            top_sorted_graphs_0.append((graph_id, len(final_graphs_0[graph_id][0].es)*(final_graphs_0[graph_id][1] - final_graphs_1[graph_id][1])   ))
        else:
            top_sorted_graphs_0.append((graph_id,len(final_graphs_0[graph_id][0].es)*final_graphs_0[graph_id][1]))

    for graph_id in final_graphs_1.keys():
        if graph_id in final_graphs_0.keys():
            top_sorted_graphs_1.append((graph_id,  len(final_graphs_1[graph_id][0].es)*(final_graphs_1[graph_id][1] - final_graphs_0[graph_id][1])  ))
        else:
            top_sorted_graphs_1.append((graph_id,len(final_graphs_1[graph_id][0].es)*final_graphs_1[graph_id][1]))
    

    top_sorted_graphs_0.sort(key = lambda x: x[1],reverse=True)
    top_sorted_graphs_1.sort(key = lambda x: x[1],reverse=True)

    graph_0_count = 0
    graph_1_count = 0

    with open("./data/graph_0_count.txt",'r') as f:
        graph_0_count = int(f.readline())
    with open("./data/graph_1_count.txt",'r') as f:
        graph_1_count = int(f.readline())
    print("---------------------------------------------------")
    print()
    print("graph_0_count : ",graph_0_count)
    print("graph_1_count : ",graph_1_count)
    print()
    print("---------------------------------------------------")
    
    division =  math.ceil((100)*(graph_0_count)/(graph_0_count + graph_1_count) )


    if ( len(top_sorted_graphs_0) > len(top_sorted_graphs_1) ):

        if len(top_sorted_graphs_1) > (100- division):
            top_sorted_graphs_1 = top_sorted_graphs_1[:(100- division)]
            top_sorted_graphs_0 = top_sorted_graphs_0[:(100 - len(top_sorted_graphs_1))]
        else:
            if len(top_sorted_graphs_0) > 100 - len(top_sorted_graphs_1):
                top_sorted_graphs_0 = top_sorted_graphs_0[:(100 - len(top_sorted_graphs_1))]
            
    else:
        
        if len(top_sorted_graphs_0) > division:
            top_sorted_graphs_0 = top_sorted_graphs_0[:division]
            top_sorted_graphs_1 = top_sorted_graphs_1[:(100 - len(top_sorted_graphs_0))]
        else:
            if len(top_sorted_graphs_1) > 100 - len(top_sorted_graphs_0):
                top_sorted_graphs_1 = top_sorted_graphs_1[:(100 - len(top_sorted_graphs_0))]
    
    print("---------------------------------------------------")
    print()
    print("division : ",division)
    print("sub_graphs of graph 0 :" , len(top_sorted_graphs_0)) 
    print("sub_graphs of graph 1 :" , len(top_sorted_graphs_1))
    print()
    print("---------------------------------------------------")


    top_sorted_graphs = []

    top_sorted_graphs = top_sorted_graphs_0 + top_sorted_graphs_1


    graph_count = 1
    with open(PATH_DISCRIMINATIVE_SUBGRAPHS,'w') as f:
        for graph_id in top_sorted_graphs:
            for graph in final_graphs[graph_id[0]]:
                g = graph
                f.write(f"t # {graph_count}\n")
                graph_count += 1
                for v in g.vs:
                    f.write(f"v {v.index} {v['label']}\n")
                for e in g.es:
                    f.write(f"e {e.source} {e.target} {e['label']}\n")

                if(graph_count > 100):
                    break

       


if __name__ == "__main__":

    main()
