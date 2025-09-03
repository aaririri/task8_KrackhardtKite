# AIDS Dataset

The **AIDS dataset** is a collection of graphs used for graph classification tasks.  
Each graph represents molecular structures where nodes correspond to atoms and edges correspond to bonds.  
The dataset is formatted following a standard convention used in many graph benchmark datasets.

---

## Dataset Structure

- **n** = total number of nodes  
- **m** = total number of edges  
- **N** = total number of graphs  

### File Info.

1. **`AIDS_A.txt`**  
   - Format: `m` lines  
   - Each line: `(row, col)` → represents an edge `(node_id, node_id)`  
   - Graphs are **undirected**, so each edge appears **twice** (once per direction).  
   - This file stores the **sparse block-diagonal adjacency matrix** for all graphs.

2. **`AIDS_graph_indicator.txt`**  
   - Format: `n` lines  
   - Column vector mapping each **node** to a **graph identifier**.  
   - The value in the *i-th line* is the `graph_id` of the node with `node_id = i`.

3. **`AIDS_graph_labels.txt`**  
   - Format: `N` lines  
   - Each line contains the **class label** for the corresponding graph.  
   - The *i-th line* is the label for the graph with `graph_id = i`.

4. **`AIDS_node_labels.txt`**  
   - Format: `n` lines  
   - Column vector of **node labels**.  
   - The *i-th line* corresponds to the label of the node with `node_id = i`.

5. **`AIDS_edge_labels.txt`**  
   - Format: `m` lines (same size as `AIDS_A.txt`)  
   - Contains **edge labels** for each entry in `AIDS_A.txt`.

6. **`AIDS_node_attributes.txt`**  
   - Format: `n` lines  
   - Each line is a **comma-separated attribute vector** for the corresponding node.  
   - The *i-th line* is the attribute vector for the node with `node_id = i`.

---

## Usage

- Each **graph** is constructed using:
  - The adjacency information from `AIDS_A.txt`  
  - The graph membership mapping from `AIDS_graph_indicator.txt`  
  - The labels/attributes from the respective label or attribute files  

- The dataset is suitable for:
  - **Graph classification** (using `AIDS_graph_labels.txt`)  
  - **Node classification** (using `AIDS_node_labels.txt`)  

---

## Notes

- **Graph IDs** are 1-based indices.  
- **Node IDs** are also 1-based and assigned consecutively across all graphs.  
- Since graphs are undirected, always ensure to treat `(u, v)` and `(v, u)` as the same edge.  

---

## Reference

> **Riesen, Kaspar, and Horst Bunke.**  
> "IAM graph database repository for graph based pattern recognition and machine learning."  
> Structural, Syntactic, and Statistical Pattern Recognition. Springer, 2008. pp. 287–297.

---
