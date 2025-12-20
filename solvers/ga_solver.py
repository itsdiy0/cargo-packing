import copy
from models import Population
from algorithms import GreedyPlacer
from utils import check_all_constraints, calculate_center_of_mass, calculate_packing_density

class CargoPackingSolver:
    # Genetic Algorithm for packing cylinders into a container
    def __init__(self, container, cylinders, population_size=100, mutation_rate=0.01, step_size=0.5):
        self.container = container
        self.cylinders = cylinders
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.placer = GreedyPlacer(step_size=step_size)
        
        self.population = Population(
            size=population_size,
            num_cylinders=len(cylinders),
            mutation_rate=mutation_rate,
            cylinders=cylinders,
            container=container,
            placer=self.placer
        )
        
        self.best_solution = None
        self.best_fitness = 0
        self.generation_history = []
    
    def solve(self, max_generations=100, target_fitness=None, verbose=True,use_local_search=False, local_search_method='hill_climbing'):
        # Main GA loop
        for gen in range(max_generations):
            self.population.calculate_fitness()
            
            stats = self.population.get_stats()
            self.generation_history.append(stats)
            
            current_best = self.population.get_best()
            
            if current_best.fitness > 0 and (self.best_solution is None or current_best.fitness > self.best_fitness):
                self.best_solution = current_best.copy()
                self.best_fitness = current_best.fitness
            
            if verbose and gen % 10 == 0:
                print(f"Generation {stats['generation']:3d}: best={stats['best']:8.2f}, avg={stats['avg']:8.2f}, worst={stats['worst']:8.2f}")
            
            self.population.normalize_fitness()
            self.population.reproduce()
            
            if target_fitness and stats['best'] >= target_fitness:
                if verbose:
                    print(f"\nTarget fitness {target_fitness} reached at generation {gen}")
                break
        # Apply local search if specified
        if use_local_search and self.best_solution:
            if verbose:
                print(f"\nApplying local search ({local_search_method})...")
        
            from algorithms import hill_climbing, simulated_annealing
        
            if local_search_method == 'hill_climbing':
                self.best_solution = hill_climbing(
                    self.best_solution, 
                    self.cylinders, 
                    self.container, 
                    self.placer, 
                    verbose=verbose
                )
            elif local_search_method == 'simulated_annealing':
                self.best_solution = simulated_annealing(
                    self.best_solution,
                    self.cylinders,
                    self.container,
                    self.placer,
                    verbose=verbose
                )
            self.best_fitness = self.best_solution.fitness
        return self.best_solution
    
    def get_solution_details(self, dna):
        # Get detailed info about a solution DNA 
        cylinder_copies = [copy.deepcopy(c) for c in self.cylinders]
        
        success = self.placer.place_cylinders(cylinder_copies, dna.genes, self.container)
        
        if not success:
            return None
        
        is_valid, error_msg = check_all_constraints(cylinder_copies, self.container)
        center_x, center_y = calculate_center_of_mass(cylinder_copies)
        density = calculate_packing_density(cylinder_copies, self.container)
        
        return {
            'genes': dna.genes,
            'fitness': dna.fitness,
            'valid': is_valid,
            'error': error_msg if not is_valid else None,
            'cylinders': cylinder_copies,
            'center_of_mass': (center_x, center_y),
            'packing_density': density
        }
    
    def print_solution(self, dna):
        if dna is None:
            print("\n" + "-" * 60)
            print("NO VALID SOLUTION FOUND")
            return
        
        details = self.get_solution_details(dna)
        
        if details is None:
            print("\n" + "-" * 60)
            print("ERROR: Could not place cylinders")
            print("-" * 60)
            return
        
        print("\n" + "-" * 60)
        print("SOLUTION DETAILS")
        print("-" * 60)
        print(f"Placement order: {details['genes']}")
        print(f"Fitness: {details['fitness']:.2f}")
        print(f"Valid: {details['valid']}")
        if not details['valid']:
            print(f"Error: {details['error']}")
        print(f"Center of mass: ({details['center_of_mass'][0]:.2f}, {details['center_of_mass'][1]:.2f})")
        print(f"Packing density: {details['packing_density']:.2%}")
        print("\nCylinder positions:")
        for cyl in details['cylinders']:
            print(f"  {cyl}")
        print("=" * 60)