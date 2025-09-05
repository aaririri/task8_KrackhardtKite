# Experiment A: Graph Isomorphism Robustness

This experiment explores how small perturbations affect graph isomorphism relationships detected by the Weisfeiler-Lehman (WL) test.

## Overview

The WL test is a powerful heuristic for graph isomorphism detection. This experiment tests its robustness to minimal structural changes by perturbing graphs with single edge modifications.

## Methodology

1. **Dataset**: AIDS molecular dataset
2. **Baseline**: Largest isomorphic group (25 graphs) identified by WL test
3. **Perturbation**: For each graph, created 10 perturbed copies, each with exactly one change:
   - Either adding one random non-existent edge
   - Or removing one existing edge
4. **Testing**: Applied WL test to the combined collection of original and perturbed graphs (275 total)

## Key Findings

- **Original Group Integrity**: The original 25 graphs remained isomorphic to each other
- **Perturbation Sensitivity**: All 250 perturbations broke isomorphism with the original group (0% preservation rate)
- **New Isomorphic Groups**: 64 distinct isomorphic groups were identified
- **Perturbation Patterns**:
  - Edge removals tended to form larger isomorphic groups with each other
  - Edge additions typically formed smaller isomorphic groups (mostly pairs)

## Conclusion

The WL test shows high sensitivity to single edge modifications. While the original isomorphic relationships remained intact among unmodified graphs, no perturbed graph maintained isomorphism with the original group. This suggests that the structural patterns identified by the WL test are precisely defined and easily disrupted by minimal changes.

## Running the Experiment

```python
python exp_a.py
```

Results are saved to `result_exp_a.txt`.