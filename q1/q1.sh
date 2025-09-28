#!/bin/bash

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <path_apriori_executable> <path_fp_executable> <path_dataset> <path_out>"
    exit 1
fi

APRIORI_EXEC=$1
FP_EXEC=$2
DATASET=$3
OUT_DIR=$4

SUPPORT_THRESHOLDS=(90 50 25 10 5)
TIMEOUT_LIMIT=3600

mkdir -p "$OUT_DIR"

TEXT_FILE="$OUT_DIR/runtime_results.txt"
echo "Support Threshold | Apriori Time (s) | FP-Tree Time (s)" > "$TEXT_FILE"
echo "-----------------------------------------------------" >> "$TEXT_FILE"

for SUPPORT in "${SUPPORT_THRESHOLDS[@]}"; do
    APRIORI_OUT="$OUT_DIR/ap${SUPPORT}"
    FP_OUT="$OUT_DIR/fp${SUPPORT}"

    echo "Running Apriori with support = $SUPPORT%"
    START_TIME=$(date +%s.%N)
    

    timeout $TIMEOUT_LIMIT $APRIORI_EXEC -s$SUPPORT "$DATASET" "$APRIORI_OUT"
    EXIT_CODE=$?
    END_TIME=$(date +%s.%N)
    touch "$APRIORI_OUT"
    touch "$FP_OUT"

    if [ $EXIT_CODE -eq 124 ]; then
        echo "Apriori timed out for support $SUPPORT%. Setting time to $TIMEOUT_LIMIT seconds."
        APRIORI_TIME=$TIMEOUT_LIMIT
    elif [ $EXIT_CODE -ne 0 ]; then
     	echo "ERROR"
	rm -rf "$APRIORI_OUT"
	touch "$APRIORI_OUT" 
	APRIORI_TIME=$(echo "$END_TIME - $START_TIME" | bc)
    else
        APRIORI_TIME=$(echo "$END_TIME - $START_TIME" | bc)
    fi

    echo "Running FP-tree with support = $SUPPORT%"
    START_TIME=$(date +%s.%N)


    timeout $TIMEOUT_LIMIT $FP_EXEC -s$SUPPORT "$DATASET" "$FP_OUT"
    EXIT_CODE=$?
    END_TIME=$(date +%s.%N)

    if [ $EXIT_CODE -eq 124 ]; then
        echo "FP-tree timed out for support $SUPPORT%. Setting time to $TIMEOUT_LIMIT seconds."
        FP_TIME=$TIMEOUT_LIMIT
    elif [ $EXIT_CODE -ne 0 ]; then
	echo "ERROR"
	rm -rf "$FP_OUT"
	touch "$FP_OUT"
	FP_TIME=$(echo "$END_TIME - $START_TIME" | bc)
    else
        FP_TIME=$(echo "$END_TIME - $START_TIME" | bc)
    fi

    

    echo "$SUPPORT | $APRIORI_TIME | $FP_TIME" >> "$TEXT_FILE"
done

echo "Processing complete. Generating plot..."


python3 "helper.py" "$TEXT_FILE"
rm -rf "$TEXT_FILE"
echo "Plot saved in $OUT_DIR."
