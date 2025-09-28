#!/usr/bin/env bash

###############################################################################
# q3.sh
# Usage:
#   bash  identify.sh <path_train_graphs> <path_train_labels> <path_discriminative_subgraphs> 

###############################################################################


if [ $# -ne 3 ]; then
  echo "Usage: $0 <path_train_graphs> <path_train_labels> <path_discriminative_subgraphs> "
  exit 1
fi


cd ./gaston-1.1 
make
cd ..

rm -rf ./data
mkdir data

PATH_TRAIN_GRAPHS=$1
PATH_TRAIN_LABELS=$2
PATH_DISCRIMINATIVE_SUBGRAPHS=$3

python3 convert.py  "$PATH_TRAIN_GRAPHS" "$PATH_TRAIN_LABELS"


TOTAL_GRAPHS_0=$(< ./data/graph_0_count.txt)
TOTAL_GRAPHS_1=$(< ./data/graph_1_count.txt)

pct=$((15+(10*(TOTAL_GRAPHS_0+TOTAL_GRAPHS_1))/(30000)))
echo "total graph_0     : $TOTAL_GRAPHS_0"
echo "total graph_1     : $TOTAL_GRAPHS_1"
minSup=$(((TOTAL_GRAPHS_0 * pct + 99) / 100))

python3 super_rem2.py ./data/graph_0.txt ./data/graph_0_mod.txt
python3 super_rem2.py ./data/graph_1.txt ./data/graph_1_mod.txt 

cd gaston-1.1
echo "=== Running Gaston at $pct% => minSup=$minSup for graph_0 ==="

./gaston $minSup ../data/graph_0_mod.txt  ../data/gaston_graph0_output.txt

#pct=$((16+(10*(TOTAL_GRAPHS_1))/(30000)))

minSup=$(((TOTAL_GRAPHS_1 * pct + 99) / 100))
echo "=== Running Gaston at $pct% => minSup=$minSup for graph_1 ==="
  
./gaston $minSup ../data/graph_1_mod.txt ../data/gaston_graph1_output.txt

echo "All subgraphs genertaed done!"

cd ..

python3 final_subgraph.py "$PATH_DISCRIMINATIVE_SUBGRAPHS"

cd gaston-1.1
make clean
cd ..


