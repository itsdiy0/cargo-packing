import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models import Container, Cylinder
from solvers import CargoPackingSolver
from algorithms import compare_local_search_methods
from utils import load_instance_from_file

def test_local_search_on_instance(instance_file):
    print("=" * 60)
    print(f"Testing Local Search on {instance_file}")
    print("=" * 60)
    
    container, cylinders = load_instance_from_file(instance_file)
    
    print(f"Container: {container}")
    print(f"Cylinders: {len(cylinders)}\n")
    
    print("Running GA to find initial solution...")
    solver = CargoPackingSolver(
        container=container,
        cylinders=cylinders,
        population_size=100,
        mutation_rate=0.05,
        step_size=0.3
    )
    
    best_solution = solver.solve(max_generations=200, verbose=False)
    
    if best_solution is None:
        print("GA failed to find valid solution")
        return
    
    print(f"GA found solution with fitness: {best_solution.fitness:.2f}\n")
    
    results = compare_local_search_methods(
        best_solution,
        cylinders,
        container,
        solver.placer
    )
    
    return results


def test_ga_with_local_search():
    print("\n" + "=" * 60)
    print("Testing GA with Integrated Local Search")
    print("=" * 60)
    
    instance_file = "data/challenging/instance_01.txt"
    container, cylinders = load_instance_from_file(instance_file)
    
    print(f"Instance: {instance_file}")
    print(f"Container: {container}")
    print(f"Cylinders: {len(cylinders)}\n")
    
    print("1. GA without local search:")
    solver1 = CargoPackingSolver(
        container=container,
        cylinders=cylinders,
        population_size=150,
        mutation_rate=0.05,
        step_size=0.3
    )
    
    solution1 = solver1.solve(max_generations=200, verbose=False, use_local_search=False)
    print(f"   Fitness: {solution1.fitness:.2f}\n")
    
    print("2. GA with hill climbing:")
    solver2 = CargoPackingSolver(
        container=container,
        cylinders=cylinders,
        population_size=150,
        mutation_rate=0.05,
        step_size=0.3
    )
    
    solution2 = solver2.solve(max_generations=200, verbose=False, use_local_search=True, local_search_method='hill_climbing')
    print(f"   Final fitness: {solution2.fitness:.2f}")
    improvement = solution2.fitness - solution1.fitness
    print(f"   Improvement: {improvement:+.2f} ({improvement/solution1.fitness*100:+.2f}%)\n")


if __name__ == "__main__":
    test_local_search_on_instance("data/reference/instance_02.txt")
    test_local_search_on_instance("data/challenging/instance_01.txt")
    test_ga_with_local_search()