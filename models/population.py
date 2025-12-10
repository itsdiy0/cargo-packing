import random
from models.dna import DNA

class Population:
    def __init__(self, size, num_cylinders, mutation_rate, cylinders, container, placer):
        self.size = size
        self.mutation_rate = mutation_rate
        self.cylinders = cylinders
        self.container = container
        self.placer = placer
        self.generation = 0
        
        self.population = []
        for i in range(size):
            self.population.append(DNA(num_cylinders))
    
    def calculate_fitness(self):
        for individual in self.population:
            individual.calculate_fitness(self.cylinders, self.container, self.placer)
    
    def normalize_fitness(self):
        # Convert raw fitness scores to percentages
        total_fitness = sum(ind.fitness for ind in self.population)
        
        if total_fitness == 0:
            for ind in self.population:
                ind.fitness = 1.0 / len(self.population)
        else:
            for ind in self.population:
                ind.fitness /= total_fitness
    
    def selection(self):
        # Relay race
        index = 0
        start = random.random()
        
        while start > 0 and index < len(self.population):
            start -= self.population[index].fitness
            index += 1
        
        index -= 1
        index = max(0, min(index, len(self.population) - 1))
        
        return self.population[index]
    
    def reproduce(self):
        new_population = []
        
        for i in range(self.size):
            parent_a = self.selection()
            parent_b = self.selection()
            
            child = parent_a.crossover(parent_b)
            child.mutate(self.mutation_rate)
            
            new_population.append(child)
        
        self.population = new_population
        self.generation += 1
    
    def evolve(self):
        self.calculate_fitness()
        self.normalize_fitness()
        self.reproduce()
    
    def get_best(self):
        self.calculate_fitness()
        return max(self.population, key=lambda ind: ind.fitness)
    
    def get_best_n(self, n):
        self.calculate_fitness()
        sorted_pop = sorted(self.population, key=lambda ind: ind.fitness, reverse=True)
        return sorted_pop[:n]
    
    def get_stats(self):
        fitnesses = [ind.fitness for ind in self.population]
        return {
            'generation': self.generation,
            'best': max(fitnesses),
            'avg': sum(fitnesses) / len(fitnesses),
            'worst': min(fitnesses)
        }