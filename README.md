# Cargo Container Loading

Evolutionary algorithm implementation for optimal cylinder packing in rectangular cargo containers.

## Problem Description

This project solves the cargo container loading problem: packing cylindrical containers of varying sizes and weights into a rectangular cargo space while satisfying:

- **Geometric constraints:** All cylinders within boundaries, no overlaps
- **Weight distribution:** Centre of mass within central 60% of container
- **Weight limit:** Total weight under maximum capacity
- **Loading order:** Cylinders loaded from rear, cannot be repositioned

---

## Installation

### Requirements
```bash
python >= 3.8
pip install -r requirements.txt
```

### Setup
```bash
# Clone repository
git clone https://github.com/itsdiy0/cargo-packing.git
cd cargo-packing

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

### Solve All Instances
```bash
python -m scripts.solve_instances
```

Solves all reference and challenging instances, saves solutions to `data/solutions/`.

### Generate Visualizations
```bash
python -m scripts.visualize_solutions
```

Creates PNG visualizations for all solved instances in `visualization/` directory.

### Compare Algorithms
```bash
python -m scripts.compare_algorithm
```

Compares GA, Greedy, and Random Search performance across test instances.

---

## Interactive Web Application 

An interactive web interface is provided for real-time visualization and algorithm comparison.

![webapp]([https://ibb.co/S4nV4Z70](https://i.ibb.co/5g8sgJxv/Screenshot-2026-01-13-at-15-25-00.png))

### Running the Web App

**Backend (Flask API):**
```bash
python -m api.app
```
Server runs on `http://localhost:5000`

**Frontend (React TypeScript):**
```bash
cd frontend
npm install
npm run dev
```
Application runs on `http://localhost:5173`

### Web App Features

- Custom container and cylinder configuration
- Real-time evolution visualization with streaming updates
- Algorithm selection (GA, Greedy, Random Search)
- Preset problem instances
- File upload for custom instances
- Live generation tracking and fitness display
- Interactive solution exploration
                    
---

## Algorithm Implementations

### 1. Genetic Algorithm

**Encoding:** Order-based permutation (placement sequence)  
**Selection:** Weighted selection (relay race method)  
**Crossover:** Order crossover (OX) preserving permutation validity  
**Mutation:** Swap mutation  
**Local Search:** Hill climbing with swap neighborhood  

**Parameters:**
- Population size: 100-150
- Mutation rate: 0.05
- Max generations: 200-500
- Step size: 0.3m

### 2. Greedy Algorithm

**Strategy:** Largest-first heuristic  
**Approach:** Sort cylinders by diameter, place at first valid position  
**Variants tested:** Largest-first, heaviest-first, smallest-first  

### 3. Random Search

**Approach:** Generate random placement orderings  
**Trials:** 1000 random permutations  
**Purpose:** Baseline performance comparison  

---

## Results Summary

### Reference Instances (3/3 solved)
- Instance 01: Fitness 10460.43, 4.19% density
- Instance 02: Fitness 10523.55, 7.26% density
- Instance 03: Fitness 10561.61, 10.32% density

### Challenging Instances (4/4 solved)
- Instance 01: Fitness 10672.37, 18.69% density
- Instance 02: Fitness 10586.55, 12.35% density
- Instance 03: Fitness 10734.13, 23.73% density (highest)
- Instance 04: Fitness 10724.05, 22.59% density

### Algorithm Performance
- **GA:** Best fitness on all instances (4/4 wins), avg 9.46s
- **Greedy:** 99.96% of GA quality, essentially instant (0.00s)
- **Random:** Competitive on simple instances, 42% success rate on hardest

---

## Key Files

**Main Scripts:**
- `solve_instances.py` - Solve all test instances
- `visualize_solutions.py` - Generate solution visualizations
- `scripts/compare_algorithm.py` - Algorithm comparison

**Core Implementation:**
- `models/dna.py` - Genetic encoding and operators
- `models/population.py` - Evolution management
- `algorithms/placer.py` - Greedy placement logic
- `solvers/ga_solver.py` - Main GA orchestration

**Results:**
- `data/solutions/` - All solution files with placement orders
- `visualizations/` - Generated PNG visualizations

