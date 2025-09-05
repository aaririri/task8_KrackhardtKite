```markdown
# Graph Isomorphism Testing - WL Test Experiments

This repository contains experiments exploring the Weisfeiler-Lehman (WL) test for graph isomorphism. Building on previous analysis of the AIDS dataset, we investigate the robustness of graph isomorphism under small perturbations (Experiment A) and validate the accuracy of WL test results (Experiment B).

## Directory Structure

```
task8/
├── experiment_a/           # Noise and robustness analysis
│   ├── exp_a.py            # Implementation for testing perturbation effects
│   ├── helper_task07.py    # WL test implementation from previous task
│   ├── result_exp_a.txt    # Detailed experiment results
│   └── README.md           # Specific documentation for Experiment A
├── experiment_b/           # WL test validation
│   ├── exp_b.py            # Basic implementation for validating WL results
│   ├── exp_b.py   # Enhanced analysis with visualizations
│   ├── experiment_b_results/  # Output directory with visualizations
│   └── README.md           # Specific documentation for Experiment B
├── report.pdf              # LaTeX report Report
└── requirements.txt        # Dependencies
```

## Experiments

- [Experiment A: Noise and Robustness](experiment_a/) - Investigates how single edge modifications affect graph isomorphism relationships.
- [Experiment B: Validating WL Test Results](experiment_b/) - Determines if graphs identified as isomorphic by the WL test are truly isomorphic.

## Installation

```bash
pip install -r requirements.txt
```

Run experiments:
```bash
python experiment_a/exp_a.py
python experiment_b/exp_b.py
```
