from models import DNA
import random
import copy

class RandomSearch:
    def __init__(self, cylinders, container, placer):
        self.cylinders = cylinders
        self.container = container
        self.placer = placer
        self.best_solution = None
        self.best_fitness = 0
        self.history = []
    
    def solve(self, num_trials=1000, verbose=True):
        """
        Try random orderings and keep the best
        
        Args:
            num_trials: Number of random orderings to try
            verbose: Print progress
        """
        if verbose:
            print(f"Running Random Search ({num_trials} trials)...")
        
        valid_count = 0
        
        for trial in range(num_trials):
            dna = DNA(len(self.cylinders))
            dna.calculate_fitness(self.cylinders, self.container, self.placer)
            
            if dna.fitness > 0:
                valid_count += 1
            
            if dna.fitness > self.best_fitness:
                self.best_solution = dna.copy()
                self.best_fitness = dna.fitness
                
                if verbose and trial % 100 == 0:
                    print(f"  Trial {trial}: New best fitness: {self.best_fitness:.2f}")
            
            self.history.append({
                'trial': trial,
                'fitness': dna.fitness
            })
        
        if verbose:
            print(f"\n  Completed {num_trials} trials")
            print(f"  Valid solutions found: {valid_count}/{num_trials} ({valid_count/num_trials*100:.1f}%)")
            print(f"  Best fitness: {self.best_fitness:.2f}")
            print(f"  Best order: {self.best_solution.genes if self.best_solution else 'None'}")
        
        return self.best_solution
    
    def get_statistics(self):
        """Get statistics about the search"""
        if not self.history:
            return None
        
        fitnesses = [h['fitness'] for h in self.history]
        valid_fitnesses = [f for f in fitnesses if f > 0]
        
        return {
            'total_trials': len(self.history),
            'valid_solutions': len(valid_fitnesses),
            'success_rate': len(valid_fitnesses) / len(self.history),
            'best_fitness': max(fitnesses),
            'avg_fitness': sum(fitnesses) / len(fitnesses),
            'avg_valid_fitness': sum(valid_fitnesses) / len(valid_fitnesses) if valid_fitnesses else 0
        }