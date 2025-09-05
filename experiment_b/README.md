# Experiment B: Validating WL Test Results

This experiment investigates the limitations of the Weisfeiler-Lehman (WL) test for graph isomorphism detection by verifying whether graphs identified as isomorphic by the test are truly isomorphic.

## Overview

The 1-WL test is widely used for graph isomorphism testing, but it has known theoretical limitations. This experiment explores these limitations by examining the AIDS molecular dataset to find "WL-fakes" - non-isomorphic graphs that the WL test incorrectly classifies as isomorphic.

## Methodology

1. **Identify WL-Isomorphic Groups**: Found 354 groups of graphs considered isomorphic by the WL test
2. **Select Larger Groups**: Analyzed the two largest groups (25 and 14 graphs respectively)
3. **Structural Analysis**: Calculated properties beyond what WL considers:
   - Spectral properties (eigenvalues of adjacency matrices)
   - Cycle counts and lengths
   - Triangle counts
   - 2-hop neighborhood degree sequences
4. **Isomorphism Verification**: For each pair, either:
   - Found distinguishing structural properties, or
   - Constructed explicit node-to-node isomorphism mappings

## Key Findings

### Group 1 (25 graphs):
- **Contains many "WL-fakes"**: 203 non-isomorphic pairs that WL couldn't distinguish
- **Primary distinguishing feature**: Spectral properties (eigenvalues)
- **Example difference**: Even subtle eigenvalue variations proved non-isomorphism
- **Confirmation**: These graphs look structurally similar locally but differ globally

### Group 2 (14 graphs):
- **All truly isomorphic**: All 91 possible pairs confirmed as isomorphic
- **Explicit mappings**: Found direct node-to-node correspondences for all pairs
- **Validation**: WL test correctly identified this group

## Conclusion

Our experiment confirms a fundamental limitation of the WL test: it cannot distinguish all non-isomorphic graphs. Specifically:

1. Spectral properties (eigenvalues) can reveal structural differences invisible to the WL test
2. The WL test focuses on local neighborhood structures and misses certain global properties
3. For the AIDS dataset, we found both examples of WL's limitations and cases where it worked correctly

This analysis aligns with theoretical results about the WL test's limitations, particularly for graphs with similar local structures but different global properties.

## Running the Experiment

```bash
python exp_b.py
```

Results and visualizations are saved in the `experiment_b_results` directory.