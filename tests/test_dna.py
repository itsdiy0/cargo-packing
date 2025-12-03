import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import Container, Cylinder, DNA
from algorithms import GreedyPlacer

def test_dna_creation():
    print("Testing DNA creation...")
    
    dna = DNA(5)
    print(f"  Created: {dna}")
    print(f"  Genes: {dna.genes}")
    
    assert len(dna.genes) == 5
    assert len(set(dna.genes)) == 5
    assert all(0 <= g < 5 for g in dna.genes)
    
    print("  DNA creation test passed")


def test_placement():
    print("\nTesting cylinder placement...")
    
    container = Container(20, 15, 1000)
    
    cylinders = [
        Cylinder(0, 2.0, 100),
        Cylinder(1, 2.0, 100),
        Cylinder(2, 2.0, 100)
    ]
    
    dna = DNA(3)
    dna.genes = [0, 1, 2]
    
    placer = GreedyPlacer(step_size=0.5)
    
    success = placer.place_cylinders(cylinders, dna.genes, container)
    
    print(f"  Placement success: {success}")
    
    for cyl in cylinders:
        print(f"  {cyl}")
    
    assert success
    assert all(c.placed for c in cylinders)
    
    print("  Placement test passed")


def test_fitness():
    print("\nTesting fitness calculation...")
    
    container = Container(20, 15, 1000)
    
    cylinders = [
        Cylinder(0, 2.0, 100),
        Cylinder(1, 2.0, 100)
    ]
    
    dna = DNA(2)
    dna.genes = [0, 1]
    
    placer = GreedyPlacer(step_size=0.5)
    
    dna.calculate_fitness(cylinders, container, placer)
    
    print(f"  Fitness: {dna.fitness}")
    
    assert dna.fitness > 0
    
    print("  Fitness test passed")


def test_crossover():
    print("\nTesting crossover...")
    
    parent1 = DNA(6)
    parent1.genes = [0, 1, 2, 3, 4, 5]
    
    parent2 = DNA(6)
    parent2.genes = [5, 4, 3, 2, 1, 0]
    
    child = parent1.crossover(parent2)
    
    print(f"  Parent 1: {parent1.genes}")
    print(f"  Parent 2: {parent2.genes}")
    print(f"  Child:    {child.genes}")
    
    assert len(child.genes) == 6
    assert len(set(child.genes)) == 6
    assert all(0 <= g < 6 for g in child.genes)
    
    print("  Crossover test passed")


def test_mutation():
    print("\nTesting mutation...")
    
    dna = DNA(5)
    original = dna.genes.copy()
    
    print(f"  Before mutation: {dna.genes}")
    
    dna.mutate(1.0)
    
    print(f"  After mutation:  {dna.genes}")
    
    assert len(dna.genes) == 5
    assert len(set(dna.genes)) == 5
    
    print("  Mutation test passed")


if __name__ == "__main__":
    print("=" * 50)
    print("RUNNING DNA AND PLACEMENT TESTS")
    print("=" * 50)
    
    test_dna_creation()
    test_placement()
    test_fitness()
    test_crossover()
    test_mutation()
    
    print("\n" + "=" * 50)
    print("ALL DNA TESTS PASSED")
    print("=" * 50)