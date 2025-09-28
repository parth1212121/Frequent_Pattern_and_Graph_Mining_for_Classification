#!/usr/bin/env python3
import sys

def parse_graphs(filename):
    """
    Reads the file line by line and groups them into graphs.
    Each graph starts with a header line beginning with "t #".
    
    Returns a list of graphs, where each graph is a list of lines.
    """
    graphs = []
    current_graph = []
    with open(filename, 'r') as infile:
        for line in infile:
            line = line.rstrip('\n')
            # A new graph starts when a line starts with "t #"
            if line.startswith("t #"):
                # If we already have some lines collected for the current graph, save it.
                if current_graph:
                    graphs.append(current_graph)
                current_graph = [line]  # start new graph with the header line
            else:
                # Add nonempty lines to the current graph.
                if line.strip():
                    current_graph.append(line)
        if current_graph:
            graphs.append(current_graph)
    return graphs

def process_graph(graph_lines):
    """
    Processes a single graph (a list of lines) so that:
      - The header ("t # ...") is removed (it will be reinserted later).
      - Each edge line "e X Y Z" is normalized such that X < Y.
      - Within each graph, duplicate edges (after normalization) are removed.
    Other lines (e.g., vertex lines "v ...") are kept as-is.
    """
    processed_lines = []
    seen_edges = set()  # to store normalized edges as tuples (x, y, label)
    
    for line in graph_lines:
        # Skip the header line (it will be replaced with new indexing later)
        if line.startswith("t #"):
            continue

        # Process edge lines
        if line.startswith("e "):
            parts = line.split()
            if len(parts) == 4:
                # Unpack parts: "e", x, y, label
                _, x_str, y_str, z_str = parts
                x = int(x_str)
                y = int(y_str)
                # Normalize: if x > y, swap them
                if x > y:
                    x, y = y, x
                edge_tuple = (x, y, z_str)
                # Only add the edge if it hasn't been seen before in this graph
                if edge_tuple not in seen_edges:
                    seen_edges.add(edge_tuple)
                    processed_lines.append(f"e {x} {y} {z_str}")
                # If already seen, skip it (duplicate)
            else:
                # If the edge line doesn't have exactly four parts, keep it unchanged.
                processed_lines.append(line)
        else:
            # For vertex lines and any other lines, keep as-is.
            processed_lines.append(line)
    return processed_lines

def write_graphs(filename, graphs):
    """
    Writes a list of graphs to a file. Each graph is a list of lines.
    Graphs are written one after another.
    """
    with open(filename, 'w') as outfile:
        for graph in graphs:
            for line in graph:
                outfile.write(line + "\n")

def main(input_file, output_file):
    # 1. Parse the input file into graphs.
    raw_graphs = parse_graphs(input_file)
    
    processed_graphs = []
    # 2. Process each graph separately.
    for graph in raw_graphs:
        proc = process_graph(graph)
        processed_graphs.append(proc)
    
    # 3. Reindex the graphs: prepend a new header "t # <new_index>" for each graph.
    reindexed_graphs = []
    for idx, graph in enumerate(processed_graphs):
        new_header = f"t # {idx}"
        new_graph = [new_header] + graph
        reindexed_graphs.append(new_graph)
    
    # 4. Write the reindexed and processed graphs to the output file.
    write_graphs(output_file, reindexed_graphs)
    print(f"Processed graphs written to '{output_file}'.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python remove_duplicates.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    main(input_file, output_file)
