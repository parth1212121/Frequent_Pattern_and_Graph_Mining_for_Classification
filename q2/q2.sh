#!/usr/bin/env bash

###############################################################################
# q2.sh
# Usage:
#   bash q2.sh <gspan_exe> <fsg_exe> <gaston_exe> <raw_dataset> <out_dir>
###############################################################################

if [ $# -ne 5 ]; then
  echo "Usage: $0 <gspan_exe> <fsg_exe> <gaston_exe> <raw_dataset> <out_dir>"
  exit 1
fi

GSPAN_EXE=$1
FSG_EXE=$2
GASTON_EXE=$3
RAW_DATASET=$4
OUT_DIR=$5

mkdir -p "$OUT_DIR"

###############################################################################
# 1) APPLY THE MAP TO CREATE .gspan, .fsg, .gaston FILES
###############################################################################
echo "Applying universal map -> gSpan format..."
python3 *.py apply_gspan   "$RAW_DATASET" "$OUT_DIR/dataset.gspan"

echo "Applying universal map -> FSG format..."
python3 *.py apply_fsg     "$RAW_DATASET" "$OUT_DIR/dataset.fsg"

echo "Applying universal map -> Gaston format..."
python3 *.py apply_gaston  "$RAW_DATASET" "$OUT_DIR/dataset.gaston"

###############################################################################
# 2) PREPARE CSV LOGS FOR EACH ALGORITHM
###############################################################################
GSPAN_CSV="gspan_runtime.csv"
FSG_CSV="fsg_runtime.csv"
GASTON_CSV="gaston_runtime.csv"

echo "Support,Runtime" > "$GSPAN_CSV"
echo "Support,Runtime" > "$FSG_CSV"
echo "Support,Runtime" > "$GASTON_CSV"

# Adjust this to your actual number of graphs
TOTAL_GRAPHS=64110
TIMEOUT_LIMIT=3600  # Set timeout limit to 1 hour (3600 seconds)

###############################################################################
# 3) RUN GSPAN @ 10%, 25%, 50%, 95% WITH TIMEOUT
###############################################################################
for pct in 0.95 0.50 0.25 0.10 0.05 
do
  echo "=== Running gSpan at support=$pct ==="
  START=$(date +%s)

  timeout "$TIMEOUT_LIMIT" "$GSPAN_EXE" -f "$OUT_DIR/dataset.gspan" -s "$pct" -o
  EXIT_STATUS=$?

  END=$(date +%s)
  RUNTIME=$((END - START))

  # Convert support value (e.g., 0.05 -> 5)
  NAME=$(echo "$pct" | sed -e 's/^0\.//' -e 's/^0*//')
  GSPAN_OUT="$OUT_DIR/gspan${NAME}"

  if [ $EXIT_STATUS -eq 124 ]; then
    echo "gSpan execution timed out at support=$pct. Logging $TIMEOUT_LIMIT seconds."
    echo "$pct,$TIMEOUT_LIMIT" >> "$GSPAN_CSV"
    
    # Create an empty output file if timeout occurred
    touch "$GSPAN_OUT"
    rm -rf "$OUT_DIR/dataset.gspan.fp"
  elif [ $EXIT_STATUS -ne 0 ]; then
    echo "ERROR"
    echo "$pct,$RUNTIME" >> "$GSPAN_CSV"
    touch "$GSPAN_OUT"
    rm -rf "$OUT_DIR/dataset.gspan.fp"
  else
    echo "$pct,$RUNTIME" >> "$GSPAN_CSV"

    # Move the actual output file if execution was successful
    mv "$OUT_DIR/dataset.gspan.fp" "$GSPAN_OUT"
  fi




done

###############################################################################
# 4) RUN FSG @ 10%, 25%, 50%, 95% WITH TIMEOUT
############################################################################### 

for s in 95 50 25 10 5
do
  echo "=== Running FSG at support=$s% ==="
  START=$(date +%s)

  timeout "$TIMEOUT_LIMIT" "$FSG_EXE" -s "$s" --minsize=0 "$OUT_DIR/dataset.fsg"
  EXIT_STATUS=$?

  END=$(date +%s)
  RUNTIME=$((END - START))

  FSG_OUT="$OUT_DIR/fsg${s}"

  if [ $EXIT_STATUS -eq 124 ]; then
    echo "FSG execution timed out at support=$s%. Logging $TIMEOUT_LIMIT seconds."
    echo "$s,$TIMEOUT_LIMIT" >> "$FSG_CSV"
    
    # Create an empty output file if timeout occurred
    touch "$FSG_OUT"
    rm "$OUT_DIR/dataset.fp"

  elif [ $EXIT_STATUS -ne 0 ]; then
    echo "ERROR"
    echo "$s,$RUNTIME" >> "$FSG_CSV"
    touch "$FSG_OUT"
    rm "$OUT_DIR/dataset.fp"

  else
    echo "$s,$RUNTIME" >> "$FSG_CSV"

    # Move the actual output file if execution was successful
    mv "$OUT_DIR/dataset.fp" "$FSG_OUT"
  fi
done

###############################################################################
# 5) RUN GASTON @ 10%, 25%, 50%, 95% WITH TIMEOUT
###############################################################################
for pct in 95 50 25 10 5
do
  minSup=$(((TOTAL_GRAPHS * pct + 99) / 100))  ## effectively performing ceiling function

  echo "=== Running Gaston at $pct% => minSup=$minSup ==="
  GASTON_OUT="$OUT_DIR/gaston${pct}"

  START=$(date +%s)
  timeout "$TIMEOUT_LIMIT" "$GASTON_EXE" "$minSup" "$OUT_DIR/dataset.gaston" "$GASTON_OUT"
  EXIT_STATUS=$?

  END=$(date +%s)
  RUNTIME=$((END - START))

  if [ $EXIT_STATUS -eq 124 ]; then
    echo "Gaston execution timed out at $pct%. Logging $TIMEOUT_LIMIT seconds."
    echo "$pct,$TIMEOUT_LIMIT" >> "$GASTON_CSV"

    # Create an empty output file if timeout occurred
    rm "$GASTON_OUT"
    touch "$GASTON_OUT"

  elif [ $EXIT_STATUS -ne 0 ]; then
    echo "ERROR"
    echo "$pct,$RUNTIME" >> "$GASTON_CSV"
    rm "$GASTON_OUT"
    touch "$GASTON_OUT"


  else
    echo "$pct,$RUNTIME" >> "$GASTON_CSV"

    
  fi
done


###############################################################################
# 6) GENERATE THE RUNTIME PLOT
###############################################################################
python3 *.py plot "$GSPAN_CSV" "$FSG_CSV" "$GASTON_CSV" "$OUT_DIR/plot.png"

rm "$OUT_DIR/dataset.gspan" "$OUT_DIR/dataset.fsg" "$OUT_DIR/dataset.gaston"

echo "All done!"
echo "Check '$OUT_DIR' for results."
