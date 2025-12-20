from models import DNA
import copy

class GreedyAlgorithm:
    def __init__(self, cylinders, container, placer):
        self.cylinders = cylinders
        self.container = container
        self.placer = placer
        self.best_solution = None
        self.best_fitness = 0
    
    def solve(self, strategy='largest_first', verbose=True):
        """
        Solve using greedy strategy
        
        Args:
            strategy: 'largest_first', 'heaviest_first', or 'smallest_first'
            verbose: Print progress
        """
        if verbose:
            print(f"Running Greedy Algorithm ({strategy})...")
        
        if strategy == 'largest_first':
            sorted_indices = self._sort_by_size(descending=True)
        elif strategy == 'heaviest_first':
            sorted_indices = self._sort_by_weight(descending=True)
        elif strategy == 'smallest_first':
            sorted_indices = self._sort_by_size(descending=False)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")
        
        dna = DNA(len(self.cylinders))
        dna.genes = sorted_indices
        dna.calculate_fitness(self.cylinders, self.container, self.placer)
        
        self.best_solution = dna
        self.best_fitness = dna.fitness
        
        if verbose:
            valid = "Valid" if dna.fitness > 0 else "Invalid"
            print(f"  Strategy: {strategy}")
            print(f"  Placement order: {dna.genes}")
            print(f"  Fitness: {dna.fitness:.2f} ({valid})")
        
        return dna
    
    def solve_all_strategies(self, verbose=True):
        """
        Try all greedy strategies and return best
        """
        if verbose:
            print("Testing all greedy strategies...")
        
        strategies = ['largest_first', 'heaviest_first', 'smallest_first']
        results = {}
        
        for strategy in strategies:
            solution = self.solve(strategy=strategy, verbose=verbose)
            results[strategy] = {
                'solution': solution,
                'fitness': solution.fitness
            }
            if verbose:
                print()
        
        best_strategy = max(results.items(), key=lambda x: x[1]['fitness'])
        
        if verbose:
            print("=" * 60)
            print("Best greedy strategy:", best_strategy[0])
            print(f"Best fitness: {best_strategy[1]['fitness']:.2f}")
            print("=" * 60)
        
        self.best_solution = best_strategy[1]['solution']
        self.best_fitness = best_strategy[1]['fitness']
        
        return results
    
    def _sort_by_size(self, descending=True):
        """Sort cylinder indices by diameter"""
        indexed_cylinders = [(i, cyl.diameter) for i, cyl in enumerate(self.cylinders)]
        sorted_cylinders = sorted(indexed_cylinders, key=lambda x: x[1], reverse=descending)
        return [i for i, _ in sorted_cylinders]
    
    def _sort_by_weight(self, descending=True):
        """Sort cylinder indices by weight"""
        indexed_cylinders = [(i, cyl.weight) for i, cyl in enumerate(self.cylinders)]
        sorted_cylinders = sorted(indexed_cylinders, key=lambda x: x[1], reverse=descending)
        return [i for i, _ in sorted_cylinders]