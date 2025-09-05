import random
import networkx as nx
from collections import defaultdict
import copy
from torch_geometric.datasets import TUDataset
from torch_geometric.utils import to_networkx
from helper_task07 import weisfeiler_lehman_hash_structural, find_isomorphic_groups_structural
import random
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import copy
from torch_geometric.datasets import TUDataset
from torch_geometric.utils import to_networkx


def get_largest_iso_group(dataset):
    isomorphic_groups = find_isomorphic_groups_structural(dataset)
    largest_groups = max(isomorphic_groups.values(), key=len, default=[])
    return largest_groups


def perturb_graph(G):
    # randomy perturbs by either adding and edge or removing and edge

    G_perturbed = copy.deepcopy(G)

    perturbation_type = random.choice(['add', 'remove'])
    perturbation_info = {}

    if perturbation_type == 'add':
        nodes = list(G.nodes())
        possible_edges = [(u,v) for u in nodes for v in nodes if u<v] 
        existing_edges = list(G.edges())
        non_existing_edges = [edge for edge in possible_edges if edge not in existing_edges]
        
        if not non_existing_edges:
            perturbation_type = 'remove'
        else:
            new_edge = random.choice(non_existing_edges)
            G_perturbed.add_edge(*new_edge)
            perturbation_info = {
                'type': 'add',
                'edge': new_edge
                }
            return G_perturbed, perturbation_info
        
    if perturbation_type == 'remove':
        edge_to_remove = random.choice(list(G.edges()))
        G_perturbed.remove_edge(*edge_to_remove)
        perturbation_info = {
            'type': 'remove',
            'edge': edge_to_remove
        }
        
        return G_perturbed, perturbation_info # returns a tuple
    



def run_experiment_a(dataset, group_indices:list, num_perturbations=10):
    # testing robustness of isomorphic groups to perturbations.
    
    original_graphs = [to_networkx(dataset[idx], node_attrs=['x']) for idx in group_indices]
    
    # perturbed copies
    all_graphs = []
    graph_origins = []  # Keep track of which original graph each perturbed copy came from
    all_perturbation_info = []
    
    # adding the original graphs
    for i, graph in enumerate(original_graphs):
        all_graphs.append(graph)
        graph_origins.append(('original', i))
        all_perturbation_info.append(None)
    
    # add perturbed copies
    for i, graph in enumerate(original_graphs):
        for j in range(num_perturbations):
            perturbed, perturbation_info = perturb_graph(graph)
            all_graphs.append(perturbed)
            graph_origins.append(('perturbed', i, j))
            all_perturbation_info.append(perturbation_info)
    
    # WL test on the combined collection
    graph_hashes = {}
    for i, G in enumerate(all_graphs):
        graph_hashes[i] = weisfeiler_lehman_hash_structural(G)
    
    # Group by hashes
    hash_groups = defaultdict(list)
    for i, hash_val in graph_hashes.items():
        hash_groups[hash_val].append(i)
    
    # Filter to only include groups with more than one graph
    isomorphic_groups = {h: indices for h, indices in hash_groups.items() if len(indices) > 1}
    
    results = {
        'total_graphs': len(all_graphs),
        'original_size': len(original_graphs),
        'total_isomorphic_groups': len(isomorphic_groups),
        'groups': []
    }
    
    # For each isomorphic group found
    for hash_val, indices in isomorphic_groups.items():
        group_info = {
            'size': len(indices),
            'original_graphs': [],
            'perturbed_graphs': [],
            'perturbation_info': []
        }
        
        # Categorize
        for idx in indices:
            origin = graph_origins[idx]
            if origin[0] == 'original':
                group_info['original_graphs'].append(origin[1])
            else:  # perturbed
                original_idx = origin[1]
                perturb_idx = origin[2]
                group_info['perturbed_graphs'].append((original_idx, perturb_idx))
                group_info['perturbation_info'].append(all_perturbation_info[idx])
        
        results['groups'].append(group_info)
    
    # how many original isomorphic relationships were broken
    original_group_remained_intact = any(
        len(group['original_graphs']) == len(original_graphs) 
        for group in results['groups']
    )
    
    results['original_group_intact'] = original_group_remained_intact
    
    return results


def main():
    dataset = TUDataset(root='/tmp/AIDS', name='AIDS', use_node_attr=True)
    print(f"Loaded {len(dataset)} graphs from AIDS dataset")
    
    largest_group = get_largest_iso_group(dataset)
    print(f"Largest isomorphic group has {len(largest_group)} graphs")
    
    results = run_experiment_a(dataset, largest_group)
    
    print("\nExperiment A Results:")
    print(f"Total graphs: {results['total_graphs']}")
    print(f"Original group size: {results['original_size']}")
    print(f"Total isomorphic groups found: {results['total_isomorphic_groups']}")
    print(f"Original group remained intact: {results['original_group_intact']}")
    

if __name__ == "__main__":
    main()