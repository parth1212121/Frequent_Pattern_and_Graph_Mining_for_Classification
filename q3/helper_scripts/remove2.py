#!/usr/bin/env python3
import os
import sys

def reindex_and_remove_reversed_edges(input_file, output_file):
    graph_index = 0  # Start numbering graphs at 0
    
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            line = line.rstrip()
            
            # Skip empty lines to avoid extra blank lines in output
            if not line:
                continue

            # If the line indicates the start of a graph, e.g., "t # 7"
            if line.startswith("t #"):
                # Rewrite to "t # <graph_index>"
                new_line = f"t # {graph_index}"
                outfile.write(new_line + "\n")
                graph_index += 1  # Increment for the next graph
                continue
            
            # If the line starts with "e ", check for reversed edges
            if line.startswith("e "):
                parts = line.split()
                # Format is "e X Y Z"
                if len(parts) == 4:
                    x = int(parts[1])
                    y = int(parts[2])
                    # If X > Y, skip the line (remove it)
                    if x > y:
                        continue
                    # Otherwise, keep it
                    outfile.write(line + "\n")
                else:
                    # If the format isn't exactly 4 parts, keep it as-is
                    outfile.write(line + "\n")
            else:
                # Keep all other lines (e.g., vertex lines) unchanged
                outfile.write(line + "\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    reindex_and_remove_reversed_edges(input_file, output_file)
    print(f"Processed file written to '{output_file}'.")
