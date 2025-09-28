#!/bin/bash

###############################################################################
# Usage:
#   bash convert.sh <path_graphs> <path_discriminative_subgraphs> <path_features>
#
# <path_graphs>:
#   Absolute or relative filepath to the dataset of graphs (train or test)
#   in the format:
#       t # <graph_id>
#       v <node_id> <node_label>
#       e <node_id1> <node_id2> <edge_label>
#       ...
#
# <path_discriminative_subgraphs>:
#   Absolute or relative filepath to the file containing the discriminative subgraphs
#   in the same format as above (or in an agreed-upon format).
#
# <path_features>:
#   Absolute or relative filepath to store the 2D NumPy array (presence/absence features).
#
# This script calls the Python script `convert.py` which:
#   - Parses all graphs
#   - Parses all subgraphs
#   - Runs subgraph isomorphism
#   - Produces a feature matrix of shape (#graphs, #discriminative_subgraphs)
#   - Saves it as a .npy file to <path_features>
###############################################################################

set -e  # Exit immediately if a command exits with a non-zero status

if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <path_graphs> <path_discriminative_subgraphs> <path_features>"
  exit 1
fi

PATH_GRAPHS="$1"
PATH_SUBGRAPHS="$2"
PATH_FEATURES="$3"

# Preprocess the input graphs

# python3 helper_scripts/graph_preprocessing.py "$PATH_GRAPHS"

# python3 helper_scripts/benzene_minus_to_9.py ./data/processed_graph.txt ./data/processed_graph2.txt
# python3 helper_scripts/remove_dup.py ./data/processed_graph2.txt ./data/processed_graph3.txt

#python3 super_rem_dup.py "$PATH_GRAPHS" ./data/modified_input_graphs.txt

python3 convert.py  "$PATH_GRAPHS" "default"

# Call the Python script
python3 helper_scripts/convert_igraph.py ./data/processed_graph.txt "$PATH_SUBGRAPHS" "$PATH_FEATURES"
