import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import os
from torch_geometric.datasets import TUDataset
from torch_geometric.utils import to_networkx
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from experiment_a.helper_task07 import weisfeiler_lehman_hash_structural, find_isomorphic_groups_structural

# Find all groups of graphs that the WL test considers isomorphic
def get_all_isomorphic_groups(dataset):
    isomorphic_groups = find_isomorphic_groups_structural(dataset)
    # (largest first)
    sorted_groups = sorted(isomorphic_groups.items(), key=lambda x: len(x[1]), reverse=True)
    return sorted_groups

# structural properties
def compute_advanced_properties(G):
    properties = {}
    
    # Basic properties
    properties['num_nodes'] = G.number_of_nodes()
    properties['num_edges'] = G.number_of_edges()
    properties['degree_sequence'] = sorted([d for n, d in G.degree()])
    
    # Cycle information
    try:
        cycles = nx.cycle_basis(G)
        properties['cycle_lengths'] = sorted([len(c) for c in cycles])
        properties['num_cycles'] = len(cycles)
    except:
        properties['cycle_lengths'] = []
        properties['num_cycles'] = 0
    
    # Triangle counts
    try:
        G_undirected = G.to_undirected() if G.is_directed() else G
        triangles = sum(nx.triangles(G_undirected).values()) // 3
        properties['triangle_count'] = triangles
    except Exception as e:
        properties['triangle_count'] = 0
    
    # 2-hop neighborhood analysis
    two_hop_sequences = {}
    for node in G.nodes():
        neighbors = set(G.neighbors(node))
        two_hop = set()

        for n in neighbors:
            two_hop.update(G.neighbors(n))
       
        two_hop -= {node} | neighbors

        if two_hop:
            two_hop_sequences[node] = sorted([G.degree(n) for n in two_hop])
    
    two_hop_distribution = sorted([tuple(seq) for seq in two_hop_sequences.values()])
    properties['two_hop_distribution'] = two_hop_distribution
    
    # Spectral properties
    try:
        A = nx.to_numpy_array(G)
        eigenvalues = np.sort(np.real(np.linalg.eigvals(A)))
        properties['eigenvalues'] = list(eigenvalues)
    except:
        properties['eigenvalues'] = []
    
    return properties


def compare_properties_detailed(props1, props2):
    differences = {}
    
    for prop in props1:
        if prop in props2 and props1[prop] != props2[prop]:
            if prop == 'eigenvalues' and len(props1[prop]) > 0 and len(props2[prop]) > 0:
                # eigenvalue differences 
                eig1 = props1[prop][:5] if len(props1[prop]) >= 5 else props1[prop]
                eig2 = props2[prop][:5] if len(props2[prop]) >= 5 else props2[prop]
                differences[prop] = {
                    'graph1': eig1,
                    'graph2': eig2
                }
            elif prop == 'cycle_lengths':
                differences[prop] = {
                    'graph1': props1[prop],
                    'graph2': props2[prop]
                }
            elif prop == 'two_hop_distribution':
                # too complex to display
                differences[prop] = "Different 2-hop neighborhood structures"
            else:
                differences[prop] = {
                    'graph1': props1[prop],
                    'graph2': props2[prop]
                }
    
    return differences

def verify_isomorphism(G1, G2):
    if G1.number_of_nodes() != G2.number_of_nodes() or G1.number_of_edges() != G2.number_of_edges():
        return False, "Different number of nodes or edges", None
    
    # Compare
    props1 = compute_advanced_properties(G1)
    props2 = compute_advanced_properties(G2)
    
    differences = compare_properties_detailed(props1, props2)
    
    if differences:
        return False, differences, None
    
    # If no differences found: trying explicit isomorphism
    try:
        matcher = nx.isomorphism.GraphMatcher(G1, G2)
        is_isomorphic = matcher.is_isomorphic()
        
        if is_isomorphic:
            mapping = matcher.mapping
            return True, "Graphs are isomorphic", mapping
        else:
            return False, "No isomorphism found by VF2 algorithm", None
    except Exception as e:
        return False, f"Error in isomorphism check: {str(e)}", None

# groups identified isomorphic by WL test
def analyze_isomorphic_group(dataset, group_indices):
    graphs = [to_networkx(dataset[idx], node_attrs=['x']) for idx in group_indices]
    
    results = {
        'size': len(graphs),
        'indices': group_indices,
        'all_truly_isomorphic': True,
        'isomorphic_pairs': [],
        'non_isomorphic_pairs': [],
        'detailed_analysis': [],
        'isomorphism_mappings': []
    }
    
    analyzed_pairs = 0
    max_detailed_pairs = 5
    
    # Check all pairs
    for i in range(len(graphs)):
        for j in range(i+1, len(graphs)):
            is_iso, reason, mapping = verify_isomorphism(graphs[i], graphs[j])
            
            if is_iso:
                results['isomorphic_pairs'].append((group_indices[i], group_indices[j]))
                
                if len(results['isomorphism_mappings']) < 3:
                    results['isomorphism_mappings'].append({
                        'pair': (group_indices[i], group_indices[j]),
                        'mapping': mapping
                    })
            else:
                results['all_truly_isomorphic'] = False
                results['non_isomorphic_pairs'].append((group_indices[i], group_indices[j]))
                
                if analyzed_pairs < max_detailed_pairs:
                    results['detailed_analysis'].append({
                        'pair': (group_indices[i], group_indices[j]),
                        'differences': reason
                    })
                    analyzed_pairs += 1
    
    return results

############################
#### helper func for visuals
############################
def visualize_graph_pair(dataset, idx1, idx2, title, save_path=None):
    G1 = to_networkx(dataset[idx1], node_attrs=['x'])
    G2 = to_networkx(dataset[idx2], node_attrs=['x'])
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    pos1 = nx.spring_layout(G1, seed=42)
    pos2 = nx.spring_layout(G2, seed=42)
    
    nx.draw_networkx(G1, pos1, ax=ax1, with_labels=True, node_color='lightblue',
                    node_size=500, font_size=10, font_weight='bold')
    ax1.set_title(f"Graph {idx1}")
    ax1.axis('off')
    
    nx.draw_networkx(G2, pos2, ax=ax2, with_labels=True, node_color='lightgreen',
                    node_size=500, font_size=10, font_weight='bold')
    ax2.set_title(f"Graph {idx2}")
    ax2.axis('off')
    
    fig.suptitle(title)
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def visualize_isomorphism_mapping(dataset, idx1, idx2, mapping, save_path=None):
    G1 = to_networkx(dataset[idx1], node_attrs=['x'])
    G2 = to_networkx(dataset[idx2], node_attrs=['x'])
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    pos1 = nx.spring_layout(G1, seed=42)

    pos2 = {}
    for node in G2.nodes():
        # Find corresponding node in G1
        for n1, n2 in mapping.items():
            if n2 == node:
                pos2[node] = pos1[n1]
                break
        # If no mapping found, place randomly
        if node not in pos2:
            pos2[node] = pos1[node] if node in pos1 else (np.random.rand(2) * 2 - 1)
    
    nx.draw_networkx(G1, pos1, ax=ax1, with_labels=True, node_color='lightblue',
                    node_size=500, font_size=10, font_weight='bold')
    ax1.set_title(f"Graph {idx1}")
    ax1.axis('off')
    
    nx.draw_networkx(G2, pos2, ax=ax2, with_labels=True, node_color='lightgreen',
                    node_size=500, font_size=10, font_weight='bold')
    ax2.set_title(f"Graph {idx2}")
    ax2.axis('off')
    
    fig.suptitle(f"Isomorphism Mapping Between Graphs {idx1} and {idx2}")
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


### MAIN EXPERIMENT FUNCTION
def run_experiment_b(dataset, groups_to_analyze=2):

    output_dir = "experiment_b_results"
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all isomorphic groups identified by WL test
    all_groups = get_all_isomorphic_groups(dataset)
    
    print(f"Found {len(all_groups)} isomorphic groups using WL test")
    
    results = {
        'total_groups': len(all_groups),
        'analyzed_groups': [],
        'found_wl_fakes': False
    }
    
    # Analyze the specified number of largest groups
    for i, (hash_val, group_indices) in enumerate(all_groups[:groups_to_analyze]):
        print(f"Analyzing group {i+1} with {len(group_indices)} graphs...")
        
        if len(group_indices) < 2:
            print("Skipping group with fewer than 2 graphs")
            continue
            
        group_results = analyze_isomorphic_group(dataset, group_indices)
        results['analyzed_groups'].append(group_results)
        
        if not group_results['all_truly_isomorphic']:
            results['found_wl_fakes'] = True
            
            # Visualize a few non-isomorphic pairs
            for j, pair in enumerate(group_results['non_isomorphic_pairs'][:3]):
                visualize_graph_pair(dataset, pair[0], pair[1], 
                                    f"Non-isomorphic Pair Misclassified by WL Test",
                                    f"{output_dir}/group{i+1}_non_isomorphic_pair_{j+1}.png")
        
        # Visualize isomorphism mappings for truly isomorphic graphs
        for j, mapping_info in enumerate(group_results['isomorphism_mappings']):
            pair = mapping_info['pair']
            mapping = mapping_info['mapping']
            visualize_isomorphism_mapping(dataset, pair[0], pair[1], mapping,
                                        f"{output_dir}/group{i+1}_isomorphic_mapping_{j+1}.png")
    
    save_enhanced_results(results, output_dir)
    return results


##### HELPER TO SAVE RESULTS #####
def save_enhanced_results(results, output_dir):
    with open(f"{output_dir}/enhanced_results.txt", 'w') as f:
        f.write("EXPERIMENT B: VALIDATING WL TEST RESULTS\n")
        f.write("=======================================\n\n")
        
        f.write(f"Total isomorphic groups found by WL test: {results['total_groups']}\n")
        f.write(f"Groups analyzed in detail: {len(results['analyzed_groups'])}\n")
        f.write(f"Found WL-fakes (non-isomorphic graphs classified as isomorphic): {results['found_wl_fakes']}\n\n")
        
        for i, group in enumerate(results['analyzed_groups']):
            f.write(f"GROUP {i+1} ANALYSIS\n")
            f.write(f"Size: {group['size']} graphs\n")
            f.write(f"Graph indices: {group['indices'][:10]}... (and more)\n")
            f.write(f"All graphs truly isomorphic: {group['all_truly_isomorphic']}\n")
            f.write(f"Isomorphic pairs: {len(group['isomorphic_pairs'])}\n")
            f.write(f"Non-isomorphic pairs: {len(group['non_isomorphic_pairs'])}\n\n")
            
            if not group['all_truly_isomorphic']:
                f.write("DETAILED ANALYSIS OF NON-ISOMORPHIC PAIRS (WL-FAKES):\n")
                
                for j, analysis in enumerate(group['detailed_analysis']):
                    pair = analysis['pair']
                    differences = analysis['differences']
                    
                    f.write(f"Example {j+1}: Graphs {pair[0]} and {pair[1]}\n")
                    
                    if isinstance(differences, dict):
                        for prop, diff in differences.items():
                            if isinstance(diff, dict) and 'graph1' in diff and 'graph2' in diff:
                                f.write(f"  {prop}:\n")
                                f.write(f"    Graph {pair[0]}: {diff['graph1']}\n")
                                f.write(f"    Graph {pair[1]}: {diff['graph2']}\n")
                            else:
                                f.write(f"  {prop}: {diff}\n")
                    else:
                        f.write(f"  Reason: {differences}\n")
                    
                    f.write("\n")
            
            if group['all_truly_isomorphic'] and group['isomorphism_mappings']:
                f.write("EXAMPLE ISOMORPHISM MAPPINGS:\n")
                for j, mapping_info in enumerate(group['isomorphism_mappings']):
                    pair = mapping_info['pair']
                    mapping = mapping_info['mapping']
                    
                    f.write(f"Mapping between graphs {pair[0]} and {pair[1]}:\n")
                    f.write("  Node correspondences (showing first 10):\n")
                    
                    count = 0
                    for node1, node2 in mapping.items():
                        f.write(f"    Node {node1} → Node {node2}\n")
                        count += 1
                        if count >= 10:
                            break
                    
                    if len(mapping) > 10:
                        f.write(f"    ... and {len(mapping)-10} more mappings\n")
                    
                    f.write("\n")
            
            f.write("-" * 50 + "\n\n")
        
        f.write("CONCLUSION\n")
        f.write("==========\n\n")
        
        if results['found_wl_fakes']:
            f.write("The experiment confirms the theoretical limitation of the 1-WL test: it cannot distinguish all non-isomorphic graphs.\n\n")
            
            # Analyze what property differences were most common
            property_counts = defaultdict(int)
            for group in results['analyzed_groups']:
                if not group['all_truly_isomorphic']:
                    for analysis in group['detailed_analysis']:
                        differences = analysis['differences']
                        if isinstance(differences, dict):
                            for prop in differences:
                                property_counts[prop] += 1
            
            if property_counts:
                sorted_props = sorted(property_counts.items(), key=lambda x: x[1], reverse=True)
                f.write("Most common properties that distinguished 'WL-fake' pairs:\n")
                for prop, count in sorted_props:
                    f.write(f"  - {prop}: found in {count} non-isomorphic pairs\n")
        else:
            f.write("All analyzed WL-isomorphic groups were confirmed to be truly isomorphic.\n")
            f.write("This suggests that for this dataset, the WL test performs accurately in identifying isomorphic graphs.\n")


##################
## MAIN EXECUTION
#################
def main():
    # Load dataset
    dataset = TUDataset(root='/tmp/AIDS', name='AIDS', use_node_attr=True)
    print(f"Loaded {len(dataset)} graphs from AIDS dataset")
    
    # Run experiment
    results = run_experiment_b(dataset)
    
    print("\nExperiment B completed. Check the 'experiment_b_results' directory for detailed analysis.")

if __name__ == "__main__":
    main()