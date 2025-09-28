#!/usr/bin/env python3

import sys
import random

def parse_graphs(filename):
    """
    Reads the file line by line and groups them into graphs.
    Each graph starts with a line containing '#'.
    Returns a list of 'graphs', where each graph is a list of lines (including the '#' line).
    """
    graphs = []
    current_graph = []

    with open(filename, 'r') as f:
        for line in f:
            line = line.rstrip()
            # When we encounter '#', that means a new graph is starting
            if line == "#":
                # If current_graph is not empty, push it and start a new one
                if current_graph:
                    graphs.append(current_graph)
                # Start a fresh graph with this '#' line
                current_graph = [line]
            else:
                # Keep adding lines to current graph
                if line:  # skip empty lines if you do not want them
                    current_graph.append(line)

        # If there's a graph collected at the end, add it too
        if current_graph:
            graphs.append(current_graph)

    return graphs

def write_graphs(filename, graphs):
    """
    Writes a list of graphs to a file. Each graph is a list of lines.
    """
    with open(filename, 'w') as f:
        for graph in graphs:
            for line in graph:
                f.write(line + "\n")

def split_data(graphs, labels, train_ratio=0.8):
    """
    Shuffle and split graphs + labels into train and test sets with given ratio.
    """
    if len(graphs) != len(labels):
        raise ValueError("Number of graphs must match number of labels.")

    indices = list(range(len(graphs)))
    random.shuffle(indices)

    train_size = int(train_ratio * len(graphs))
    train_indices = indices[:train_size]
    test_indices = indices[train_size:]

    # Gather train/test sets
    train_graphs = [graphs[i] for i in train_indices]
    train_labels = [labels[i] for i in train_indices]
    test_graphs  = [graphs[i] for i in test_indices]
    test_labels  = [labels[i] for i in test_indices]

    return train_graphs, train_labels, test_graphs, test_labels

def main(graph_file, label_file, train_ratio=0.8):
    # 1. Parse graphs from the graph_file
    graphs = parse_graphs(graph_file)

    # 2. Read labels from label_file
    with open(label_file, 'r') as f:
        labels = [line.strip() for line in f if line.strip()]

    # 3. Split into train & test
    train_graphs, train_labels, test_graphs, test_labels = split_data(graphs, labels, train_ratio)

    # 4. Write the splits to disk
    write_graphs("train_graphs.txt", train_graphs)
    with open("train_labels.txt", 'w') as f:
        for lbl in train_labels:
            f.write(str(lbl) + "\n")

    write_graphs("test_graphs.txt", test_graphs)
    with open("test_labels.txt", 'w') as f:
        for lbl in test_labels:
            f.write(str(lbl) + "\n")

    print("Data split complete!")
    print(f"  Train set: {len(train_graphs)} graphs, saved to train_graphs.txt + train_labels.txt")
    print(f"  Test set:  {len(test_graphs)} graphs, saved to test_graphs.txt + test_labels.txt")

if __name__ == "__main__":
    # Basic usage: python split_graphs.py <graphs_file> <labels_file> <optional_train_ratio>
    if len(sys.argv) < 3:
        print("Usage: python split_graphs.py <graphs_file> <labels_file> [<train_ratio>]")
        sys.exit(1)

    graph_file = sys.argv[1]
    label_file = sys.argv[2]
    if len(sys.argv) > 3:
        train_ratio = float(sys.argv[3])
    else:
        train_ratio = 0.8  # default

    main(graph_file, label_file, train_ratio)
