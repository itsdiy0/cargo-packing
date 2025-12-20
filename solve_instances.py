import os
from utils import load_instance_from_file, save_solution_to_file
from solvers import CargoPackingSolver

def solve_instance_from_file(input_filepath, output_filepath, 
                             population_size=150, 
                             mutation_rate=0.05, 
                             step_size=0.3, 
                             max_generations=500,
                             use_local_search=True,
                             verbose=True):
    if verbose:
        print(f"\nLoading instance: {input_filepath}")
    
    container, cylinders = load_instance_from_file(input_filepath)
    
    if verbose:
        print(f"Container: {container}")
        print(f"Number of cylinders: {len(cylinders)}")
    
    solver = CargoPackingSolver(
        container=container,
        cylinders=cylinders,
        population_size=population_size,
        mutation_rate=mutation_rate,
        step_size=step_size
    )
    
    best_solution = solver.solve(
        max_generations=max_generations, 
        verbose=verbose,
        use_local_search=use_local_search,
        local_search_method='hill_climbing'
    )
    
    if best_solution is None:
        print(f"FAILED: No valid solution found for {input_filepath}")
        return None
    
    details = solver.get_solution_details(best_solution)
    
    save_solution_to_file(output_filepath, best_solution, container, cylinders, 
                          best_solution.fitness, details)
    
    if verbose:
        solver.print_solution(best_solution)
        print(f"Solution saved to: {output_filepath}")
    
    return solver

def solve_all_reference_instances():
    """
    Solve all reference instances
    """
    print("=" * 60)
    print("SOLVING REFERENCE INSTANCES")
    print("=" * 60)
    
    reference_dir = "data/reference"
    solutions_dir = "data/solutions/reference"
    
    os.makedirs(solutions_dir, exist_ok=True)
    
    instance_files = sorted([f for f in os.listdir(reference_dir) if f.endswith('.txt')])
    
    results = []
    
    for instance_file in instance_files:
        input_path = os.path.join(reference_dir, instance_file)
        output_path = os.path.join(solutions_dir, instance_file.replace('.txt', '_solution.txt'))
        
        solver = solve_instance_from_file(
            input_path, 
            output_path,
            population_size=150,
            mutation_rate=0.05,
            step_size=0.3,
            max_generations=300,
            verbose=True
        )
        
        results.append({
            'instance': instance_file,
            'solver': solver,
            'success': solver is not None
        })
    
    print("\n" + "=" * 60)
    print("REFERENCE INSTANCES SUMMARY")
    print("-" * 60)
    for result in results:
        status = "SOLVED" if result['success'] else "FAILED"
        print(f"{result['instance']}: {status}")
    
    return results


def solve_all_challenging_instances():
    """
    Solve all challenging instances
    """
    print("SOLVING CHALLENGING INSTANCES")
    print("-" * 60)
    
    challenging_dir = "data/challenging"
    solutions_dir = "data/solutions/challenging"
    
    os.makedirs(solutions_dir, exist_ok=True)
    
    instance_files = sorted([f for f in os.listdir(challenging_dir) if f.endswith('.txt')])
    
    results = []
    
    for instance_file in instance_files:
        input_path = os.path.join(challenging_dir, instance_file)
        output_path = os.path.join(solutions_dir, instance_file.replace('.txt', '_solution.txt'))
        
        solver = solve_instance_from_file(
            input_path, 
            output_path,
            population_size=200,
            mutation_rate=0.1,
            step_size=0.2,
            max_generations=500,
            verbose=True
        )
        
        results.append({
            'instance': instance_file,
            'solver': solver,
            'success': solver is not None
        })
    
    
    print("CHALLENGING INSTANCES SUMMARY")
    print("-" * 60)
    for result in results:
        status = "SOLVED" if result['success'] else "FAILED"
        print(f"{result['instance']}: {status}")
    
    
    return results


if __name__ == "__main__":
    solve_all_reference_instances()
    solve_all_challenging_instances()