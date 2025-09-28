import sys



""" def apply_gspan(graph_struct,graph_id):
    head = 't # ' + str(graph_id) +"\n"
    new_graph_struct = [head]

    for _ in graph_struct:
        data = _.split(' ')
        if (data[0]=='v'):
            new_graph_struct.append(_)
        elif(data[0]=='e'):
            new_graph_struct.append(_)
        else:
            raise ValueError("graph.txt format not correct, got :",data)
    return new_graph_struct

def apply_fsg(graph_struct,graph_id):
    head = 't # ' + str(graph_id) +"\n"
    new_graph_struct = [head]

    for _ in graph_struct:
        data = _.split(' ')
        if (data[0]=='v'):
            new_graph_struct.append(_)
        elif(data[0]=='e'):
            new_graph_struct.append(_)
        else:
            raise ValueError("graph.txt format not correct, got :",data)
    return new_graph_struct
 """
def apply_gaston(graph_struct,graph_id,prune_label,no_edge_label):

    head = 't # ' + str(graph_id) +"\n"                 
    new_graph_struct = [head]
    nodes_to_label = dict()
    label_to_nodes = dict()
    adj = dict()

    for _ in graph_struct:
        _ = _.strip()
        data = _.split(' ')
        if (data[0]=='v'):
            if data[2] in  label_to_nodes.keys():
                label_to_nodes[data[2]].append(data[1])
            else:
                label_to_nodes[data[2]]=[data[1]]
            nodes_to_label[data[1]] = data[2]
        elif(data[0]=='e'):
            if data[1] in adj.keys():
                adj[data[1]][data[2]]=data[3]
            else:
                adj[data[1]] = {data[2]:data[3]}
            
        else:
            raise ValueError("graph.txt format not correct, got :",data)
    # print("Error in graph ",graph_id)
    # print("Nodes to label ",nodes_to_label)
    # print("Adjacency ",adj)
    # print("Label to nodes ",label_to_nodes)
    # print()
    remove_zero_edge_nodes = []
    for key_ in nodes_to_label.keys():
        if key_ not in adj.keys():
            remove_zero_edge_nodes+=[key_]

    for key_ in remove_zero_edge_nodes:
        label = nodes_to_label[key_]
        label_to_nodes[label].remove(key_)
        nodes_to_label.pop(key_)
            
    prunable_nodes = adj.keys()
    removable_nodes = dict()
    for key_ in adj.keys():
        for adj_key in adj[key_].keys():
            if key_ not in adj[adj_key].keys():
                print("1. Error in graph ",graph_id)
                print("1. Nodes to label ",nodes_to_label)
                print("1. Adjacency ",adj)
                print("1. Removable nodes ",removable_nodes)
                print("1. Label to nodes ",label_to_nodes)
                sys.exit(1)
    
    if (prune_label in label_to_nodes.keys()):


        for nodes_ in label_to_nodes[prune_label]:
            if nodes_ in prunable_nodes:
                if (len(adj[nodes_].keys()) == 1):
                    removable_nodes[nodes_] = adj[nodes_]
                
        
    
        for nodes_ in removable_nodes.keys():
            if nodes_ in adj.keys() :
                temp_adj_node = list(adj[nodes_].keys())
                # if( nodes_ == '26'):
                #     print("Temp adj node ",temp_adj_node)
                #     print(nodes_)
                #     print()
                # if ( temp_adj_node[0] == '26'):
                #     print("Temp adj node ",temp_adj_node)
                #     print("Adj ",adj)
                #     print(nodes_)
                #     print()
                adj[temp_adj_node[0]].pop(nodes_)
                if (len(adj[temp_adj_node[0]].keys())==0):
                    adj.pop(temp_adj_node[0])
                    label_to_nodes[nodes_to_label[temp_adj_node[0]]].remove(temp_adj_node[0])
                    nodes_to_label.pop(temp_adj_node[0])
                    
                adj.pop(nodes_)
                nodes_to_label.pop(nodes_)

        label_to_nodes.pop(prune_label)

    mex = 0 
    new_node_idx = dict()
    for key in adj.keys() :
        
        new_node_idx[key] = str(mex)
        mex += 1
    for key_ in adj.keys():
        for adj_key in adj[key_].keys():
            if key_ not in adj[adj_key].keys():
                print("Error in graph ",graph_id)
                print("Nodes to label ",nodes_to_label)
                print("Adjacency ",adj)
                print("Removable nodes ",removable_nodes)
                print("Label to nodes ",label_to_nodes)
                sys.exit(1)

    for key_ in adj.keys():
        if key_ not in nodes_to_label.keys():

            print("Error in graph ",graph_id)
            print("Nodes to label ",nodes_to_label)
            print("Adjacency ",adj)
            print("New node idx ",new_node_idx)
            print("Removable nodes ",removable_nodes)
            print("Label to nodes ",label_to_nodes)
            print("Prune label ",prune_label)
            print("No edge label ",no_edge_label)
            sys.exit(1)

    for key_ in nodes_to_label.keys():
        if key_ not in adj.keys():
            print("Error in graph ",graph_id)
            print("Nodes to label ",nodes_to_label)
            print("Adjacency ",adj)
            print("New node idx ",new_node_idx)
            print("Removable nodes ",removable_nodes)
            print("Label to nodes ",label_to_nodes)
            print("Prune label ",prune_label)
            print("No edge label ",no_edge_label)

            sys.exit(1)

    def find_6_cycles_from_node(start_node, current_path, edge_sequence):

        cycles = []
  
        if len(current_path) == 6:
            if start_node in adj[current_path[-1]]:
                
                last_edge = adj[current_path[-1]][start_node]
                """ print(edge_sequence + [last_edge])
                print(set(nodes_to_label[n] for n in current_path)) """
                if ((edge_sequence + [last_edge]) == [0,1,0,1,0,'1'] or 
                    (edge_sequence + [last_edge]) == [1,0,1,0,1,'0']):

                    if len(set(nodes_to_label[n] for n in current_path)) == 1:
                        cycles.append(current_path[:])
            return cycles
            
        current_node = current_path[-1]
        for next_node in adj[current_node]:
            edge_label = int(adj[current_node][next_node])
            
            if edge_sequence and edge_label == edge_sequence[-1]:
                continue 
            if next_node in current_path[:-1]:
                continue
            if nodes_to_label[next_node] != nodes_to_label[current_node]:
                continue
                
            current_path.append(next_node)
            edge_sequence.append(edge_label)
            cycles.extend(find_6_cycles_from_node(start_node, current_path, edge_sequence))
            current_path.pop()
            edge_sequence.pop()
            
        return cycles

    all_cycles = set()
    for start_node in adj:
        cycles = find_6_cycles_from_node(start_node, [start_node], [])
        for cycle in cycles:
            all_cycles.add(frozenset(cycle))

    for cycle in all_cycles:
        cycle = list(cycle)
        for node in cycle :
            for adj_node in adj[node]:
                if adj_node in cycle:
                    adj[node][adj_node] = str(no_edge_label)
        """ for i in range(len(cycle)):
            print(cycle[i],"->",adj[cycle[i]]," ",cycle[(i+1)%(len(cycle))],"->",adj[cycle[(i+1)%len(cycle)]])
            j = (i + 1) % len(cycle)
            adj[cycle[i]][cycle[j]] = '-1'
            adj[cycle[j]][cycle[i]] = '-1' """

    try:
        for key in adj.keys():
            new_graph_struct.append('v '+new_node_idx[key]+' '+nodes_to_label[key]+'\n')
        for key in adj.keys():
            for value in adj[key].keys():
                new_graph_struct.append('e '+new_node_idx[key]+' '+new_node_idx[value]+' '+adj[key][value]+'\n')
    except:  
     
        print("Error in graph ",graph_id)
        print("Nodes to label ",nodes_to_label)
        print("Adjacency ",adj)
        print("New node idx ",new_node_idx)
        print("Removable nodes ",removable_nodes)
        print("Prunable nodes ",prunable_nodes)
        print("Label to nodes ",label_to_nodes)
        print("All cycles ",all_cycles)
        print("Prune label ",prune_label)
        print("No edge label ",no_edge_label)
        raise ValueError("Error in graph ",graph_id )
    

    return new_graph_struct  

def distinct_graph_label_txt(raw_label_file,raw_graph_file, format_algo ):
    graph_id = 0
    graph_0_count = 0
    graph_1_count = 0
    label_freq = dict()
    edge_freq = dict()
    label_degree = dict()
    temp_node_label = dict()

    with open(raw_graph_file,'r') as f2 :
     
        graph_line = f2.readlines()
        j = 1
        while ( j < len(graph_line)):
            data_l = graph_line[j].strip()
            data = data_l.split()

            j+=1
            if(data[0]=='v'):
                label_freq[data[2]] = label_freq.get(data[2],0) + 1
                temp_node_label[data[1]] = data[2]
            elif(data[0]=='e'):
                edge_freq[int(data[3])] = edge_freq.get(int(data[3]),0) + 1
                label_degree[temp_node_label[data[1]]] = label_degree.get(temp_node_label[data[1]],0) + 1
                label_degree[temp_node_label[data[2]]] = label_degree.get(temp_node_label[data[2]],0) + 1

            else:
                temp_node_label = dict()

    # print("Label freq ",label_freq)
    # print("Edge freq ",edge_freq)
    # print("Label degree ",label_degree)
    

    no_edge_label = 0
    while(no_edge_label in edge_freq.keys()):
        no_edge_label += 1
    

    print("No edge label is ",no_edge_label)

    freq_label = []
    average_degree = dict()

    for key in label_freq.keys():
        freq_label.append((key,label_freq[key]))

    for key in label_degree.keys():
        average_degree[key] = label_degree[key]/label_freq[key]
    
    freq_label.sort(key = lambda x: x[1],reverse=True)


    most_freq_label_freq = freq_label[0][1]
    prune_label = -1

    for i in range(len(freq_label)):
        if ( freq_label[i][1] >0.7*most_freq_label_freq):
            if( average_degree[freq_label[i][0]] < 4):
                prune_label = freq_label[i][0]
                break

    
    print("pruning nodes with label ",prune_label)
    with open('./data/graph_0.txt','w') as graph_0, open ('./data/graph_1.txt','w') as graph_1:
        with open(raw_label_file,'r') as f1 , open(raw_graph_file,'r') as f2 :
            label_line = f1.readlines()
            graph_line = f2.readlines()

            i = 0 
            j = 1

            while ( i < len(label_line)):
                label = int(label_line[i][0])
                i+=1
                graph_struct = []

                while ( j < len(graph_line)):
                    if(graph_line[j][0]=='#'):
                        break
                    else:
                        graph_struct.append(graph_line[j])
                        j+=1

                formatted_graph_struct = format_algo(graph_struct,graph_id,prune_label,no_edge_label)

                graph_id += 1
                j+=1
                if ( label == 0):
                    graph_0_count += 1
                    graph_0.writelines(formatted_graph_struct)
                elif ( label == 1) :
                    graph_1_count += 1
                    graph_1.writelines(formatted_graph_struct)
                else:
                    raise ValueError("Graph label not 0 or 1 !")
    

    with open('./data/graph_0_count.txt','w') as count_file:
        count_file.write(str(graph_0_count))
    with open('./data/graph_1_count.txt','w') as count_file:
        count_file.write(str(graph_1_count))


 
def distinct_graph_label_txt_default(raw_label_file,raw_graph_file, format_algo ):
    graph_id = 0
    graph_0_count = 0
    graph_1_count = 0
    label_freq = dict()
    edge_freq = dict()
    label_degree = dict()
    temp_node_label = dict()

    with open(raw_graph_file,'r') as f2 :
     
        graph_line = f2.readlines()
        j = 1
        while ( j < len(graph_line)):
            data_l = graph_line[j].strip()
            data = data_l.split()

            j+=1
            if(data[0]=='v'):
                label_freq[data[2]] = label_freq.get(data[2],0) + 1
                temp_node_label[data[1]] = data[2]
            elif(data[0]=='e'):
                edge_freq[int(data[3])] = edge_freq.get(int(data[3]),0) + 1
                label_degree[temp_node_label[data[1]]] = label_degree.get(temp_node_label[data[1]],0) + 1
                label_degree[temp_node_label[data[2]]] = label_degree.get(temp_node_label[data[2]],0) + 1

            else:
                temp_node_label = dict()

    # print("Label freq ",label_freq)
    # print("Edge freq ",edge_freq)
    # print("Label degree ",label_degree)
    

    no_edge_label = 0
    while(no_edge_label in edge_freq.keys()):
        no_edge_label += 1
    

    print("No edge label is ",no_edge_label)

    freq_label = []
    average_degree = dict()

    for key in label_freq.keys():
        freq_label.append((key,label_freq[key]))

    for key in label_degree.keys():
        average_degree[key] = label_degree[key]/label_freq[key]
    
    freq_label.sort(key = lambda x: x[1],reverse=True)


    most_freq_label_freq = freq_label[0][1]
    prune_label = -1

    for i in range(len(freq_label)):
        if ( freq_label[i][1] >0.7*most_freq_label_freq):
            if( average_degree[freq_label[i][0]] < 4):
                prune_label = freq_label[i][0]
                break

    
    print("pruning nodes with label ",prune_label)
    with open('./data/graph_0.txt','w') as graph_0, open ('./data/graph_1.txt','w') as graph_1 ,open ('./data/processed_graph.txt','w') as c_graph:
        with open(raw_label_file,'r') as f1 , open(raw_graph_file,'r') as f2 :
            label_line = f1.readlines()
            graph_line = f2.readlines()

            i = 0 
            j = 1

            while ( i < len(label_line)):
                label = int(label_line[i][0])
                i+=1
                graph_struct = []

                while ( j < len(graph_line)):
                    if(graph_line[j][0]=='#'):
                        break
                    else:
                        graph_struct.append(graph_line[j])
                        j+=1

                formatted_graph_struct = format_algo(graph_struct,graph_id,prune_label,no_edge_label)

                graph_id += 1
                j+=1
                c_graph.writelines(formatted_graph_struct)

def create_dummy_labels(input_graph_file, output_label_file):
    graph_count = 0
    with open(input_graph_file, 'r') as infile:
        for line in infile:

            if line.strip() == '#':
                graph_count += 1


    with open(output_label_file, 'w') as outfile:
        for _ in range(graph_count):
            outfile.write("69\n")

    print(f"Created {output_label_file} with {graph_count} dummy labels (0).")


def main():
    if len(sys.argv) < 2:
        raise ValueError("Not enough arguments")


    label_file = sys.argv[2]
    graph_file = sys.argv[1]

    if(label_file == "default"):
        default_label_file = "./data/labels_dummy.txt"
        create_dummy_labels(graph_file, default_label_file)
        distinct_graph_label_txt_default(default_label_file,graph_file,apply_gaston)
    else:   
        distinct_graph_label_txt(label_file,graph_file,apply_gaston)




if __name__ == '__main__':
    main()


