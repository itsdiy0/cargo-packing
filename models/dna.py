import random
import copy

class DNA:
    def __init__(self, num_cylinders):
        # Initialize DNA with a random permutation of cylinder indices
        self.num_cylinders = num_cylinders
        self.genes = list(range(num_cylinders))
        random.shuffle(self.genes)
        self.fitness = 0
    
    def calculate_fitness(self, cylinders, container, placer):
        # Calculate fitness based on placement success and quality
        from utils.helpers import (
            check_all_constraints,
            calculate_packing_density,
            calculate_center_of_mass
        )
        
        cylinder_copies = [copy.deepcopy(c) for c in cylinders]
        
        success = placer.place_cylinders(cylinder_copies, self.genes, container)
        
        if not success:
            self.fitness = 0
            return
        
        is_valid, error_msg = check_all_constraints(cylinder_copies, container)
        
        if not is_valid:
            self.fitness = 0
            return
        
        self.fitness = 10000
        
        density = calculate_packing_density(cylinder_copies, container)
        self.fitness += density * 1000
        
        center_x, center_y = calculate_center_of_mass(cylinder_copies)
        container_center_x = container.width / 2
        container_center_y = container.depth / 2
        
        dx = abs(center_x - container_center_x) / container.width
        dy = abs(center_y - container_center_y) / container.depth
        centeredness = 1 - (dx + dy) / 2
        self.fitness += centeredness * 500
    
    def crossover(self, partner):
        # Create a child DNA by combining genes from self and partner
        child = DNA(self.num_cylinders)
        
        start = random.randint(0, self.num_cylinders - 1)
        end = random.randint(start + 1, self.num_cylinders)
        
        child.genes = [-1] * self.num_cylinders
        child.genes[start:end] = self.genes[start:end]
        
        child_pos = end % self.num_cylinders
        for gene in partner.genes:
            if gene not in child.genes:
                child.genes[child_pos] = gene
                child_pos = (child_pos + 1) % self.num_cylinders
        
        return child
    
    def mutate(self, mutation_rate):
        for i in range(len(self.genes)):
            if random.random() < mutation_rate:
                j = random.randint(0, len(self.genes) - 1)
                self.genes[i], self.genes[j] = self.genes[j], self.genes[i]
    
    def copy(self):
        new_dna = DNA(self.num_cylinders)
        new_dna.genes = self.genes.copy()
        new_dna.fitness = self.fitness
        return new_dna
    
    def __str__(self):
        return f"DNA(genes={self.genes}, fitness={self.fitness:.2f})"