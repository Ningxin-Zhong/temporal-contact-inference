# Temporal Contact Inference System

## Overview
This project develops a Python-based system for temporal contact inference under incomplete observational data.

It models structured interactions between individuals over time and applies constraint-based reasoning to infer latent states and reconstruct possible transmission processes.

---

## Problem Setting
In many real-world scenarios, observations are partial, noisy, and time-dependent. This project explores how to infer hidden state transitions (e.g., infection status) from:

- Sparse testing results
- Structured contact interactions
- Temporal constraints

The goal is to deduce consistent explanations of system dynamics without relying on probabilistic assumptions.

---

## Approach

### Structured Interaction Modelling
- Individuals are represented within daily contact groups
- Each group encodes local interaction structure
- Time is discretised into sequential units (AM/PM per day)

Rather than explicitly constructing graph objects, interactions are modelled implicitly through grouped relationships and propagated constraints.

---

### Constraint-Based Reasoning
Each individual is assigned a state:
- **H** (Human)
- **V** (Vampire)
- **U** (Unknown)

Inference is driven by deterministic rules:
- Forward propagation of irreversible states
- Backward propagation of confirmed states
- Consistency constraints across time and interactions

---

### Temporal Inference
The system integrates multiple sources of information:
- Test results (ground truth signals)
- Contact interactions (possible transmission events)
- Logical constraints (state consistency)

This enables:
- Narrowing of possible transition windows
- Identification of feasible transmission pathways
- Elimination of inconsistent hypotheses

---

### Iterative Refinement
Inference is performed iteratively until convergence:

- Constraints are repeatedly applied
- State uncertainty is progressively reduced
- A fixed point is reached when no further updates occur

This process resembles constraint propagation in partially observed dynamic systems.

---

## Outputs
The system produces:

- Inferred state trajectories over time
- Estimated transition (infection) windows
- Sets of potential transmission sources
- Classification of individuals based on inferred roles

---

## Example Usage

```bash
python contact.py input.txt
