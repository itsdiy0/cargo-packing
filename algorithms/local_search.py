import copy

def hill_climbing(dna, cylinders, container, placer, max_iterations=50, verbose=False):
    """
    Hill climbing local search with swap operations
    
    Args:
        dna: DNA object to improve
        cylinders: List of Cylinder objects
        container: Container object
        placer: GreedyPlacer object
        max_iterations: Maximum number of improvement rounds
        verbose: Print progress
        
    Returns:
        Improved DNA object
    """
    initial_fitness = dna.fitness
    if verbose:
        print(f"Starting local search with fitness: {initial_fitness:.2f}")
    
    improved = True
    iteration = 0
    
    while improved and iteration < max_iterations:
        improved = False
        iteration += 1
        
        best_swap = None
        best_fitness = dna.fitness
        
        for i in range(len(dna.genes)):
            for j in range(i + 1, len(dna.genes)):
                test_dna = dna.copy()
                test_dna.genes[i], test_dna.genes[j] = test_dna.genes[j], test_dna.genes[i]
                
                test_dna.calculate_fitness(cylinders, container, placer)
                
                if test_dna.fitness > best_fitness:
                    best_fitness = test_dna.fitness
                    best_swap = (i, j)
                    improved = True
        
        if improved and best_swap:
            i, j = best_swap
            dna.genes[i], dna.genes[j] = dna.genes[j], dna.genes[i]
            dna.fitness = best_fitness
            
            if verbose:
                print(f"  Iteration {iteration}: Swapped positions {i} and {j}, fitness: {best_fitness:.2f}")
    
    dna.calculate_fitness(cylinders, container, placer)
    
    if verbose:
        improvement = dna.fitness - initial_fitness
        print(f"Local search complete: {initial_fitness:.2f} -> {dna.fitness:.2f} (improvement: {improvement:.2f})")
    
    return dna


def simulated_annealing(dna, cylinders, container, placer, 
                        initial_temp=100, cooling_rate=0.95, 
                        max_iterations=1000, verbose=False):
    """
    Simulated annealing local search
    
    Args:
        dna: DNA object to improve
        cylinders: List of Cylinder objects
        container: Container object
        placer: GreedyPlacer object
        initial_temp: Starting temperature
        cooling_rate: How fast to cool (0.9-0.99)
        max_iterations: Maximum iterations
        verbose: Print progress
        
    Returns:
        Improved DNA object
    """
    import random
    import math
    
    initial_fitness = dna.fitness
    if verbose:
        print(f"Starting simulated annealing with fitness: {initial_fitness:.2f}")
    
    current_solution = dna.copy()
    best_solution = dna.copy()
    
    temperature = initial_temp
    
    for iteration in range(max_iterations):
        i = random.randint(0, len(current_solution.genes) - 1)
        j = random.randint(0, len(current_solution.genes) - 1)
        
        if i == j:
            continue
        
        test_solution = current_solution.copy()
        test_solution.genes[i], test_solution.genes[j] = test_solution.genes[j], test_solution.genes[i]
        test_solution.calculate_fitness(cylinders, container, placer)
        
        delta = test_solution.fitness - current_solution.fitness
        
        if delta > 0:
            current_solution = test_solution
            if test_solution.fitness > best_solution.fitness:
                best_solution = test_solution.copy()
                if verbose and iteration % 100 == 0:
                    print(f"  Iteration {iteration}: New best fitness: {best_solution.fitness:.2f}")
        else:
            acceptance_prob = math.exp(delta / temperature) if temperature > 0 else 0
            if random.random() < acceptance_prob:
                current_solution = test_solution
        
        temperature *= cooling_rate
        
        if temperature < 0.01:
            break
    
    if verbose:
        improvement = best_solution.fitness - initial_fitness
        print(f"Simulated annealing complete: {initial_fitness:.2f} -> {best_solution.fitness:.2f} (improvement: {improvement:.2f})")
    
    return best_solution


def iterated_local_search(dna, cylinders, container, placer, 
                          num_restarts=5, verbose=False):
    """
    Iterated local search: Run hill climbing multiple times with perturbations
    
    Args:
        dna: DNA object to improve
        cylinders: List of Cylinder objects
        container: Container object
        placer: GreedyPlacer object
        num_restarts: Number of times to restart with perturbation
        verbose: Print progress
        
    Returns:
        Best improved DNA object
    """
    import random
    
    initial_fitness = dna.fitness
    if verbose:
        print(f"Starting iterated local search with fitness: {initial_fitness:.2f}")
    
    best_solution = dna.copy()
    current_solution = dna.copy()
    
    for restart in range(num_restarts):
        current_solution = hill_climbing(current_solution, cylinders, container, placer, 
                                        max_iterations=20, verbose=False)
        
        if current_solution.fitness > best_solution.fitness:
            best_solution = current_solution.copy()
            if verbose:
                print(f"  Restart {restart + 1}: New best fitness: {best_solution.fitness:.2f}")
        
        if restart < num_restarts - 1:
            current_solution = best_solution.copy()
            num_swaps = random.randint(2, 4)
            for _ in range(num_swaps):
                i = random.randint(0, len(current_solution.genes) - 1)
                j = random.randint(0, len(current_solution.genes) - 1)
                current_solution.genes[i], current_solution.genes[j] = current_solution.genes[j], current_solution.genes[i]
    
    if verbose:
        improvement = best_solution.fitness - initial_fitness
        print(f"Iterated local search complete: {initial_fitness:.2f} -> {best_solution.fitness:.2f} (improvement: {improvement:.2f})")
    
    return best_solution


def compare_local_search_methods(dna, cylinders, container, placer):
    """
    Compare all local search methods
    
    Returns:
        dict with results from each method
    """
    print("Comparing local search methods...")
    print(f"Initial fitness: {dna.fitness:.2f}\n")
    
    results = {}
    
    print("1. Hill Climbing:")
    hc_solution = hill_climbing(dna.copy(), cylinders, container, placer, verbose=True)
    results['hill_climbing'] = {
        'solution': hc_solution,
        'fitness': hc_solution.fitness,
        'improvement': hc_solution.fitness - dna.fitness
    }
    print()
    
    print("2. Simulated Annealing:")
    sa_solution = simulated_annealing(dna.copy(), cylinders, container, placer, verbose=True)
    results['simulated_annealing'] = {
        'solution': sa_solution,
        'fitness': sa_solution.fitness,
        'improvement': sa_solution.fitness - dna.fitness
    }
    print()
    
    print("3. Iterated Local Search:")
    ils_solution = iterated_local_search(dna.copy(), cylinders, container, placer, verbose=True)
    results['iterated_local_search'] = {
        'solution': ils_solution,
        'fitness': ils_solution.fitness,
        'improvement': ils_solution.fitness - dna.fitness
    }
    print()
    
    print("=" * 60)
    print("COMPARISON SUMMARY")
    print("=" * 60)
    for method, result in results.items():
        print(f"{method:25s}: {result['fitness']:8.2f} (improvement: {result['improvement']:+6.2f})")
    print("=" * 60)
    
    best_method = max(results.items(), key=lambda x: x[1]['fitness'])
    print(f"\nBest method: {best_method[0]} with fitness {best_method[1]['fitness']:.2f}")
    
    return results