import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import Container, Cylinder, DNA, Population
from algorithms import GreedyPlacer

def test_population_creation():
    print("Testing population creation...")
    
    container = Container(20, 15, 1000)
    cylinders = [
        Cylinder(0, 2.0, 100),
        Cylinder(1, 2.0, 100),
        Cylinder(2, 2.0, 100)
    ]
    placer = GreedyPlacer(step_size=0.5)
    
    population = Population(
        size=10,
        num_cylinders=3,
        mutation_rate=0.01,
        cylinders=cylinders,
        container=container,
        placer=placer
    )
    
    print(f"  Population size: {len(population.population)}")
    print(f"  Generation: {population.generation}")
    
    assert len(population.population) == 10
    assert population.generation == 0
    
    print("  Population creation test passed")


def test_fitness_calculation():
    print("\nTesting fitness calculation...")
    
    container = Container(20, 15, 1000)
    cylinders = [
        Cylinder(0, 2.0, 100),
        Cylinder(1, 2.0, 100)
    ]
    placer = GreedyPlacer(step_size=0.5)
    
    population = Population(
        size=5,
        num_cylinders=2,
        mutation_rate=0.01,
        cylinders=cylinders,
        container=container,
        placer=placer
    )
    
    population.calculate_fitness()
    
    print("  Individual fitnesses:")
    for i, ind in enumerate(population.population):
        print(f"    Individual {i}: {ind.fitness:.2f}")
    
    assert all(ind.fitness >= 0 for ind in population.population)
    
    print("  Fitness calculation test passed")


def test_evolution():
    print("\nTesting evolution...")
    
    container = Container(20, 15, 1000)
    cylinders = [
        Cylinder(0, 2.0, 100),
        Cylinder(1, 2.0, 100),
        Cylinder(2, 2.0, 100)
    ]
    placer = GreedyPlacer(step_size=0.5)
    
    population = Population(
        size=20,
        num_cylinders=3,
        mutation_rate=0.05,
        cylinders=cylinders,
        container=container,
        placer=placer
    )
    
    print("  Initial generation:", population.generation)
    initial_best = population.get_best()
    print(f"  Initial best fitness: {initial_best.fitness:.2f}")
    
    for i in range(5):
        population.evolve()
        stats = population.get_stats()
        print(f"  Gen {stats['generation']}: best={stats['best']:.2f}, avg={stats['avg']:.2f}")
    
    final_best = population.get_best()
    print(f"  Final best fitness: {final_best.fitness:.2f}")
    print(f"  Final best genes: {final_best.genes}")
    
    assert population.generation == 5
    
    print("  Evolution test passed")


def test_best_individual():
    print("\nTesting best individual retrieval...")
    
    container = Container(20, 15, 1000)
    cylinders = [
        Cylinder(0, 2.0, 100),
        Cylinder(1, 2.0, 100)
    ]
    placer = GreedyPlacer(step_size=0.5)
    
    population = Population(
        size=10,
        num_cylinders=2,
        mutation_rate=0.01,
        cylinders=cylinders,
        container=container,
        placer=placer
    )
    
    best = population.get_best()
    print(f"  Best individual: {best}")
    
    population.calculate_fitness()
    all_fitnesses = [ind.fitness for ind in population.population]
    max_fitness = max(all_fitnesses)
    
    assert best.fitness == max_fitness
    
    print("  Best individual test passed")


if __name__ == "__main__":
    print("=" * 50)
    print("RUNNING POPULATION TESTS")
    print("=" * 50)
    
    test_population_creation()
    test_fitness_calculation()
    test_evolution()
    test_best_individual()
    
    print("\n" + "=" * 50)
    print("ALL POPULATION TESTS PASSED")
    print("=" * 50)