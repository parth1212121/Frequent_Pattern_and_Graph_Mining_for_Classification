#!/usr/bin/env python3

def parse_graphs(filename):
    """
    Reads the file line by line and groups them into graphs,
    each starting with a line containing exactly '#'.
    
    Returns a list of graphs, where each graph is a list of lines (including '#').
    """
    graphs = []
    current_graph = []

    with open(filename, 'r') as infile:
        for line in infile:
            line = line.rstrip('\n')  # remove trailing newline

            # If we see a line that is exactly '#', it starts a new graph
            if line.strip() == "#":
                # If there's a current graph already in progress, store it
                if current_graph:
                    graphs.append(current_graph)
                # Start a new graph with this '#' line
                current_graph = [line]
            else:
                # Otherwise, just add the line to the current graph
                if line.strip():
                    current_graph.append(line)

        # If there's a graph in progress at the end, add it
        if current_graph:
            graphs.append(current_graph)
    
    return graphs

def process_graph(graph_lines):
    """
    Takes the lines for one graph, returns a *new* list of lines
    where edges are deduplicated and normalized (X < Y).
    """
    processed_lines = []
    seen_edges = set()  # to store tuples of the form (min, max, label)
    
    for line in graph_lines:
        # If it's an edge line: "e X Y Z"
        if line.startswith("e "):
            parts = line.split()
            # Expecting format: e X Y Z
            if len(parts) == 4:
                _, x_str, y_str, z_str = parts
                x = int(x_str)
                y = int(y_str)
                z = z_str  # keep the label as a string
                
                # Ensure (x, y) is ordered
                if x > y:
                    x, y = y, x  # swap so x < y

                # Check if we've seen this edge in the set
                edge_tuple = (x, y, z)
                if edge_tuple not in seen_edges:
                    # Not seen, so we add it and write it out
                    seen_edges.add(edge_tuple)
                    processed_lines.append(f"e {x} {y} {z}")
                # If it's already in seen_edges, skip it (duplicate)
            else:
                # If the edge line doesn't match the expected format,
                # just keep it as-is or decide how to handle
                processed_lines.append(line)
        else:
            # For everything else (including the '#' line and 'v' lines), keep as-is
            processed_lines.append(line)
    
    return processed_lines

def write_graphs(filename, graphs):
    """
    Writes the given list of *already-processed* graphs to a file.
    Each graph is a list of lines, and each graph starts with '#'.
    """
    with open(filename, 'w') as outfile:
        for i, graph_lines in enumerate(graphs):
            for line in graph_lines:
                outfile.write(line + "\n")

def main(input_file, output_file):
    # 1. Parse the entire input into a list of graphs
    graphs = parse_graphs(input_file)
    
    # 2. Process each graph to remove duplicates and normalize edges (X<Y)
    processed_graphs = []
    for graph in graphs:
        new_graph = process_graph(graph)
        processed_graphs.append(new_graph)
    
    # 3. Write the processed graphs to the output file
    write_graphs(output_file, processed_graphs)
    print(f"Processed graphs written to {output_file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python remove_duplicates.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    main(input_file, output_file)
