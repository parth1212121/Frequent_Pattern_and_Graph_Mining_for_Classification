import matplotlib.pyplot as plt
import sys
import os

if len(sys.argv) != 2:
    print("Usage: python q1.py <path_to_runtime_results.txt>")
    sys.exit(1)

text_file = sys.argv[1]

support_thresholds = []
apriori_times = []
fp_tree_times = []

with open(text_file, 'r') as file:
    lines = file.readlines()[2:]

    for line in lines:
        parts = line.strip().split('|')
        if len(parts) == 3:
            support_thresholds.append(int(parts[0].strip()))
            apriori_times.append(float(parts[1].strip()))
            fp_tree_times.append(float(parts[2].strip()))

plt.figure(figsize=(10, 6))
plt.plot(support_thresholds, apriori_times, marker='o', linestyle='-', color='blue', label="Apriori")
plt.plot(support_thresholds, fp_tree_times, marker='s', linestyle='--', color='red', label="FP-Tree")

plt.xlabel("Support Threshold (%)")
plt.ylabel("Runtime (seconds)")
plt.title("Apriori vs FP-Tree Runtime Comparison")
plt.legend()
plt.grid(True)

plot_path = os.path.join(os.path.dirname(text_file), "plot.png")
plt.savefig(plot_path)

