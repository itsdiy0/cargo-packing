import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models import Container, Cylinder
from solvers import CargoPackingSolver
from algorithms import GreedyAlgorithm, RandomSearch, GreedyPlacer
from utils import load_instance_from_file
import time

def compare_all_algorithms(instance_file, show_results=True):
    """
    Compare GA, Greedy, and Random Search on an instance
    """
    print("=" * 70)
    print(f"ALGORITHM COMPARISON: {instance_file}")
    print("=" * 70)
    
    container, cylinders = load_instance_from_file(instance_file)
    placer = GreedyPlacer(step_size=0.3)
    
    print(f"\nContainer: {container}")
    print(f"Cylinders: {len(cylinders)}")
    print()
    
    results = {}
    
    # 1. Genetic Algorithm
    print("\n" + "-" * 70)
    print("1. GENETIC ALGORITHM")
    print("-" * 70)
    start_time = time.time()
    
    ga_solver = CargoPackingSolver(
        container=container,
        cylinders=cylinders,
        population_size=100,
        mutation_rate=0.05,
        step_size=0.3
    )
    ga_solution = ga_solver.solve(max_generations=200, verbose=False, use_local_search=True)
    ga_time = time.time() - start_time
    
    results['Genetic Algorithm'] = {
        'solution': ga_solution,
        'fitness': ga_solution.fitness if ga_solution else 0,
        'time': ga_time,
        'valid': ga_solution.fitness > 0 if ga_solution else False
    }
    
    print(f"Time: {ga_time:.2f}s")
    print(f"Fitness: {results['Genetic Algorithm']['fitness']:.2f}")
    print(f"Valid: {results['Genetic Algorithm']['valid']}")
    
    # 2. Greedy Algorithm
    print("\n" + "-" * 70)
    print("2. GREEDY ALGORITHM")
    print("-" * 70)
    start_time = time.time()
    
    greedy_solver = GreedyAlgorithm(cylinders, container, placer)
    greedy_results = greedy_solver.solve_all_strategies(verbose=False)
    greedy_time = time.time() - start_time
    
    best_greedy = max(greedy_results.items(), key=lambda x: x[1]['fitness'])
    
    results['Greedy Algorithm'] = {
        'solution': best_greedy[1]['solution'],
        'fitness': best_greedy[1]['fitness'],
        'time': greedy_time,
        'valid': best_greedy[1]['fitness'] > 0,
        'best_strategy': best_greedy[0]
    }
    
    print(f"Best strategy: {best_greedy[0]}")
    print(f"Time: {greedy_time:.2f}s")
    print(f"Fitness: {results['Greedy Algorithm']['fitness']:.2f}")
    print(f"Valid: {results['Greedy Algorithm']['valid']}")
    
    # 3. Random Search
    print("\n" + "-" * 70)
    print("3. RANDOM SEARCH")
    print("-" * 70)
    start_time = time.time()
    
    random_solver = RandomSearch(cylinders, container, placer)
    random_solution = random_solver.solve(num_trials=1000, verbose=False)
    random_time = time.time() - start_time
    
    stats = random_solver.get_statistics()
    
    results['Random Search'] = {
        'solution': random_solution,
        'fitness': random_solution.fitness if random_solution else 0,
        'time': random_time,
        'valid': random_solution.fitness > 0 if random_solution else False,
        'success_rate': stats['success_rate']
    }
    
    print(f"Trials: 1000")
    print(f"Success rate: {stats['success_rate']*100:.1f}%")
    print(f"Time: {random_time:.2f}s")
    print(f"Fitness: {results['Random Search']['fitness']:.2f}")
    print(f"Valid: {results['Random Search']['valid']}")
    
    # Summary
    print("\n" + "=" * 70)
    print("COMPARISON SUMMARY")
    print("=" * 70)
    print(f"{'Algorithm':<20} {'Fitness':>10} {'Time (s)':>10} {'Valid':>8}")
    print("-" * 70)
    
    for name, result in results.items():
        valid_str = "Yes" if result['valid'] else "No"
        print(f"{name:<20} {result['fitness']:>10.2f} {result['time']:>10.2f} {valid_str:>8}")
    
    best_algo = max(results.items(), key=lambda x: x[1]['fitness'])
    fastest_algo = min(results.items(), key=lambda x: x[1]['time'])
    
    print("-" * 70)
    print(f"Best fitness: {best_algo[0]} ({best_algo[1]['fitness']:.2f})")
    print(f"Fastest: {fastest_algo[0]} ({fastest_algo[1]['time']:.2f}s)")
    print("=" * 70)
    
    return results


def compare_multiple_instances():
    """
    Compare algorithms across multiple instances
    """
    instances = [
        "data/reference/instance_01.txt",
        "data/reference/instance_02.txt",
        "data/challenging/instance_01.txt",
        "data/challenging/instance_04.txt"
    ]
    
    all_results = {}
    
    for instance in instances:
        results = compare_all_algorithms(instance, show_results=True)
        all_results[instance] = results
        print("\n\n")
    
    # Overall summary
    print("=" * 70)
    print("OVERALL SUMMARY ACROSS ALL INSTANCES")
    print("=" * 70)
    
    algo_names = ['Genetic Algorithm', 'Greedy Algorithm', 'Random Search']
    
    for algo in algo_names:
        wins = sum(1 for results in all_results.values() 
                   if max(results.items(), key=lambda x: x[1]['fitness'])[0] == algo)
        avg_fitness = sum(results[algo]['fitness'] for results in all_results.values()) / len(all_results)
        avg_time = sum(results[algo]['time'] for results in all_results.values()) / len(all_results)
        
        print(f"\n{algo}:")
        print(f"  Wins: {wins}/{len(instances)}")
        print(f"  Avg fitness: {avg_fitness:.2f}")
        print(f"  Avg time: {avg_time:.2f}s")


if __name__ == "__main__":
    compare_multiple_instances()