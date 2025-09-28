#!/usr/bin/env python3

import sys
import numpy as np
import pandas as pd
import os
from igraph import Graph
import logging

def setup_logging():
    """
    Configures the logging settings.
    """
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s: %(message)s')

def replace_edge_labels_in_file(file_path, old_label=9, new_label=2):
    """
    Replaces all occurrences of old_label with new_label in edge labels of the graph file.

    Args:
        file_path (str): Path to the graph file.
        old_label (int): The edge label to be replaced. Default is 9.
        new_label (int): The new edge label. Default is 2.
    """
    temp_file = file_path + '.tmp'
    replacements = 0
    try:
        with open(file_path, 'r') as infile, open(temp_file, 'w') as outfile:
            for line_num, line in enumerate(infile, 1):
                stripped_line = line.strip()
                if stripped_line.startswith('e '):
                    tokens = stripped_line.split()
                    if len(tokens) >= 4:
                        try:
                            current_label = int(tokens[3])
                            if current_label == old_label:
                                tokens[3] = str(new_label)
                                replacements += 1
                                logging.debug(f"Line {line_num}: Replaced edge label {old_label} with {new_label}.")
                        except ValueError:
                            logging.warning(f"Line {line_num}: Non-integer edge label. Skipping replacement.")
                    else:
                        logging.warning(f"Line {line_num}: Malformed edge line. Skipping replacement.")
                # Write the (possibly modified) line to the temp file
                outfile.write(line)
        # Replace the original file with the temp file
        os.replace(temp_file, file_path)
        logging.info(f"Edge label replacement complete. {replacements} replacements made in '{file_path}'.")
    except FileNotFoundError:
        logging.error(f"Error: The file '{file_path}' does not exist.")
        sys.exit(1)
    except PermissionError:
        logging.error(f"Error: Permission denied when accessing '{file_path}' or '{temp_file}'.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An unexpected error occurred during edge label replacement: {e}")
        sys.exit(1)

def parse_graphs(file_path):
    """
    Parses the graphs from the given file, which has lines like:
        t # <graph_id>
        v <node_id> <node_label>
        e <node_id1> <node_id2> <edge_label>

    Returns a list of dicts, where each dict has:
        {
          'id': <graph_id>,
          'nodes': {node_id: node_label, ...},
          'edges': set((n1, n2, edge_label), ...)
        }
    We store edges in canonical form (min(n1,n2), max(n1,n2), label)
    to avoid duplication and directionality issues.
    """
    graphs = []
    current_graph = None

    logging.info(f"Parsing graphs from file: {file_path}")
    with open(file_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            tokens = line.split()
            if tokens[0] == 't':
                # Start a new graph
                if current_graph is not None:
                    graphs.append(current_graph)
                    logging.debug(f"Added Graph ID {current_graph['id']} with {len(current_graph['nodes'])} nodes and {len(current_graph['edges'])} edges.")
                try:
                    graph_id = int(tokens[2])
                except (IndexError, ValueError):
                    logging.warning(f"Line {line_num}: Invalid graph ID. Skipping this graph.")
                    current_graph = None
                    continue
                current_graph = {
                    'id': graph_id,
                    'nodes': {},
                    'edges': set()
                }
                logging.debug(f"Line {line_num}: Starting new graph with ID: {graph_id}")

            elif tokens[0] == 'v':
                # v <node_id> <node_label>
                if len(tokens) < 3:
                    logging.warning(f"Line {line_num}: Malformed node line. Skipping.")
                    continue
                try:
                    node_id = int(tokens[1])
                    node_label = int(tokens[2])
                except ValueError:
                    logging.warning(f"Line {line_num}: Non-integer node ID or label. Skipping.")
                    continue
                if current_graph is not None:
                    current_graph['nodes'][node_id] = node_label
                    logging.debug(f"Line {line_num}: Added node: ID={node_id}, Label={node_label}")
                else:
                    logging.warning(f"Line {line_num}: Node defined outside of a graph. Skipping.")

            elif tokens[0] == 'e':
                # e <node_id1> <node_id2> <edge_label>
                if len(tokens) < 4:
                    logging.warning(f"Line {line_num}: Malformed edge line. Skipping.")
                    continue
                try:
                    n1 = int(tokens[1])
                    n2 = int(tokens[2])
                    e_label = int(tokens[3])
                except ValueError:
                    logging.warning(f"Line {line_num}: Non-integer edge components. Skipping.")
                    continue
                if current_graph is not None:
                    edge = (min(n1, n2), max(n1, n2), e_label)
                    current_graph['edges'].add(edge)
                    logging.debug(f"Line {line_num}: Added edge: {edge}")
                else:
                    logging.warning(f"Line {line_num}: Edge defined outside of a graph. Skipping.")

    # Add the last graph if any
    if current_graph is not None:
        graphs.append(current_graph)
        logging.debug(f"Added Graph ID {current_graph['id']} with {len(current_graph['nodes'])} nodes and {len(current_graph['edges'])} edges.")

    logging.info(f"Total graphs parsed from {file_path}: {len(graphs)}\n")
    return graphs

def build_igraph_graph(graph_dict):
    """
    Converts a parsed graph dictionary to an igraph Graph object with attributes.

    Args:
        graph_dict (dict): Dictionary with keys 'id', 'nodes', 'edges'

    Returns:
        Graph: igraph Graph object
    """
    # Create an empty graph
    G = Graph(directed=False)

    # Add vertices
    node_ids = sorted(graph_dict['nodes'].keys())
    G.add_vertices(len(node_ids))

    # Map original node IDs to igraph vertex indices
    node_map = {original_id: idx for idx, original_id in enumerate(node_ids)}

    # Assign node labels as attributes
    labels = [graph_dict['nodes'][nid] for nid in node_ids]
    G.vs["label"] = labels

    # Add edges with labels
    edge_tuples = []
    edge_labels = []
    for (n1, n2, label) in graph_dict['edges']:
        if n1 in node_map and n2 in node_map:
            edge_tuples.append((node_map[n1], node_map[n2]))
            edge_labels.append(label)
        else:
            logging.warning(f"Edge ({n1}, {n2}) with label {label} references undefined nodes.")

    G.add_edges(edge_tuples)
    G.es["label"] = edge_labels

    return G

def vertex_compat(g1, g2, v1, v2):
    """
    Determines if two vertices from different graphs are compatible based on their labels.
    
    Args:
        g1 (Graph): The main graph.
        g2 (Graph): The subgraph.
        v1 (int): Vertex index in the main graph.
        v2 (int): Vertex index in the subgraph.
    
    Returns:
        bool: True if vertices are compatible, False otherwise.
    """
    return g1.vs[v1]["label"] == g2.vs[v2]["label"]

def edge_compat(g1, g2, e1, e2):
    """
    Determines if two edges from different graphs are compatible based on their labels.
    
    Args:
        g1 (Graph): The main graph.
        g2 (Graph): The subgraph.
        e1 (int): Edge index in the main graph.
        e2 (int): Edge index in the subgraph.
    
    Returns:
        bool: True if edges are compatible, False otherwise.
    """
    return g1.es[e1]["label"] == g2.es[e2]["label"]

def is_subgraph_isomorphic(target_graph, pattern_graph, graph_id, subgraph_id):
    """
    Checks if the pattern_graph is isomorphic to a subgraph of target_graph using igraph.

    Args:
        target_graph (Graph): igraph Graph object (main graph).
        pattern_graph (Graph): igraph Graph object (subgraph).
        graph_id (int): ID of the main graph.
        subgraph_id (int): ID of the subgraph.

    Returns:
        bool: True if pattern_graph is isomorphic to a subgraph of target_graph, False otherwise.
    """
    try:
        is_iso = target_graph.subisomorphic_vf2(pattern_graph,
                                               node_compat_fn=vertex_compat,
                                               edge_compat_fn=edge_compat)
    except Exception as e:
        logging.error(f"Error during subgraph isomorphism check between Graph {graph_id} and Subgraph {subgraph_id}: {e}")
        return False

    # if is_iso:
    #     #logging.debug(f"Graph {graph_id} contains Subgraph {subgraph_id}")
    # else:
    #     #logging.debug(f"Graph {graph_id} does NOT contain Subgraph {subgraph_id}")

    return is_iso

def main():
    setup_logging()

    if len(sys.argv) != 4:
        logging.error("Usage: python convert_igraph_corrected.py <path_graphs> <path_subgraphs> <path_features>")
        sys.exit(1)

    path_graphs = sys.argv[1]
    path_subgraphs = sys.argv[2]
    path_features = sys.argv[3]

    # Optional: Replace edge labels from 9 to 2 in main graphs
    # Uncomment the following lines if you need to perform edge label replacement
    # logging.info("=== Replacing edge labels from 9 to 2 in main graphs ===")
    # replace_edge_labels_in_file(path_graphs, old_label=9, new_label=2)
    # logging.info()

    # 1. Parse graphs
    logging.info("=== Parsing Main Graphs ===")
    graphs_data = parse_graphs(path_graphs)
    logging.info(f"Parsed {len(graphs_data)} main graphs.\n")

    logging.info("=== Parsing Subgraphs ===")
    subgraphs_data = parse_graphs(path_subgraphs)
    logging.info(f"Parsed {len(subgraphs_data)} discriminative subgraphs.\n")

    # 2. Convert to igraph objects
    logging.info("=== Converting Main Graphs to igraph Objects ===")
    ig_graphs = [build_igraph_graph(gd) for gd in graphs_data]
    logging.info("=== Converting Subgraphs to igraph Objects ===")
    ig_subgraphs = [build_igraph_graph(sd) for sd in subgraphs_data]

    num_graphs = len(ig_graphs)
    num_subgraphs = len(ig_subgraphs)

    logging.info(f"\nLoaded {num_graphs} main graphs and {num_subgraphs} discriminative subgraphs.\n")

    # 3. Build feature matrix
    logging.info("=== Building Feature Matrix ===")
    features = np.zeros((num_graphs, num_subgraphs), dtype=np.int32)

    for i, bigG in enumerate(ig_graphs):
        graph_id = graphs_data[i]['id']
        for j, subG in enumerate(ig_subgraphs):
            subgraph_id = subgraphs_data[j]['id']
            if is_subgraph_isomorphic(bigG, subG, graph_id, subgraph_id):
                features[i, j] = 1
                #logging.info(f"Graph {graph_id} contains Subgraph {subgraph_id}")
        # Progress update every 10 graphs or at the end
        if (i + 1) % 1000 == 0 or i + 1 == num_graphs:
            logging.info(f"Processed {i + 1}/{num_graphs} graphs.")

    logging.info(f"Feature matrix constructed with shape: {features.shape}")

    # 4. Save the feature matrix as .npy
    logging.info(f"Saving feature matrix to '{path_features}' as .npy...")
    np.save(path_features, features)
    logging.info(f"Features saved to {path_features} (npy format).")

    # 5. Save the feature matrix as .csv
    csv_output = os.path.splitext(path_features)[0] + ".csv"
    logging.info(f"Saving feature matrix to '{csv_output}' as .csv...")

    # Convert to pandas DataFrame
    df = pd.DataFrame(features)
    # Name the columns as Subgraph_1, Subgraph_2, ..., Subgraph_N
    df.columns = [f"Subgraph_{j+1}" for j in range(num_subgraphs)]
    # Add an index column for Graph IDs starting from 1
    df.index += 1
    df.index.name = "Graph_ID"

    # Save to CSV
    df.to_csv(csv_output)
    logging.info(f"Features saved to {csv_output} (csv format).")

    # 6. Save subgraph counts to a separate text file
    counts_output = os.path.splitext(path_features)[0] + "_subgraph_counts.txt"
    logging.info(f"Saving subgraph counts to '{counts_output}' as a text file...")

    # Calculate counts for each subgraph
    subgraph_counts = features.sum(axis=0)

    # Write counts to the text file
    with open(counts_output, 'w') as f:
        for j, count in enumerate(subgraph_counts, 1):
            f.write(f"Subgraph_{j}: {count}\n")
    logging.info(f"Subgraph counts saved to {counts_output}.")

if __name__ == "__main__":
    main()
