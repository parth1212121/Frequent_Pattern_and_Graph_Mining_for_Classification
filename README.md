# Frequent Pattern and Subgraph Mining (COL761 Assignment 1)

This repository contains implementations and experiments for **Frequent Itemset Mining**, **Frequent Subgraph Mining**, and **Graph Classification**, as part of the COL761 (Data Mining) course assignment.

---

## 📖 Project Components

### 1️⃣ Frequent Itemset Mining
- Implemented and compared **Apriori** and **FP-Growth** algorithms.  
- Dataset: `webdocs.dat`  
- Experiments conducted at support thresholds: 5%, 10%, 25%, 50%, 90%.  
- **Observations**:
  - Apriori struggles at low support (timeouts at 5%).  
  - FP-Growth is significantly faster and memory-efficient at low supports.  
  - At high support (50%, 90%), both perform similarly.  
- Script: `q1.sh` automates runs and generates runtime plots.

---

### 2️⃣ Frequent Subgraph Mining
- Applied **gSpan**, **FSG (PAFI)**, and **Gaston** on the Yeast dataset.  
- Support thresholds tested: 5%, 10%, 25%, 50%, 95%.  
- **Observations**:
  - Gaston outperforms others at low thresholds due to efficient edge-centric approach.  
  - gSpan is faster than FSG at low support but slower than Gaston.  
  - At high support, all perform similarly.  
- Script: `q2.sh` automates conversion, runs algorithms, logs runtimes, and plots results.

---

### 3️⃣ Graph Classification
- Focused on **molecular graph classification** for binary tasks (Mutagenicity, NCI-H23 datasets).  
- Pipeline:
  1. **Graph Preprocessing**: Remove redundancies, prune hydrogens, normalize edge labels.  
  2. **Subgraph Mining**: Use Gaston to extract frequent subgraphs from class 0 and class 1 separately.  
  3. **Feature Vector Construction**: Select top-100 discriminative subgraphs, build binary vectors.  
  4. **Classification**: Train given ML classifier on extracted features.  
- Scripts:
  - `identify.sh` → end-to-end pipeline for extracting discriminative subgraphs.  
  - Helper scripts (`convert.py`, `final_subgraph.py`, `super_rem2.py`, etc.) handle graph conversion and edge normalization.  
- **Observations**:
  - Removing redundant nodes improves efficiency.  
  - Discriminative subgraphs improve generalization.  
  - Subgraph isomorphism is costly → runtime bottleneck.  

---

## ⚙️ Usage

### Frequent Itemset Mining
```bash
bash q1.sh <path_apriori_exe> <path_fp_exe> <path_dataset> <out_dir>
```

### Frequent Subgraph Mining
```bash
bash q2.sh <gspan_exe> <fsg_exe> <gaston_exe> <raw_dataset> <out_dir>
```

### Graph Classification
```bash
bash identify.sh <train_graphs> <train_labels> <output_subgraphs>
```

---

## 📊 Results Summary
- **Itemset Mining**: FP-Growth dominates at low support; Apriori fails at 5%.  
- **Subgraph Mining**: Gaston is fastest, FSG the slowest at low support.  
- **Graph Classification**: Achieved effective binary classification using top-100 discriminative subgraphs.  

---

## 👥 Contributors
- Daksh Dhaker (2022CS51264)  
- Parth Verma (2022CS11936)  
- Umang Tripathi (2022CS51134)  
