from models import Container, Cylinder
from solvers import CargoPackingSolver
from tests.test_instances import get_all_test_instances

def load_instance_from_dict(data):
    container = Container(
        width=data['container']['width'],
        depth=data['container']['depth'],
        max_weight=data['container']['max_weight']
    )
    
    cylinders = []
    for i, cyl_data in enumerate(data['cylinders']):
        cylinders.append(Cylinder(
            cylinder_id=i,
            diameter=cyl_data['diameter'],
            weight=cyl_data['weight']
        ))
    
    return container, cylinders


def run_instance(instance_data):
    print(f"\nTesting {instance_data['name']}...")
    
    container, cylinders = load_instance_from_dict(instance_data)
    
    print(f"Container: {container}")
    print(f"Number of cylinders: {len(cylinders)}")
    
    params = instance_data['ga_params']
    solver = CargoPackingSolver(
        container=container,
        cylinders=cylinders,
        population_size=params['population_size'],
        mutation_rate=params['mutation_rate'],
        step_size=params['step_size']
    )
    
    best_solution = solver.solve(
        max_generations=params['max_generations'],
        verbose=True
    )
    
    solver.print_solution(best_solution)
    
    return solver


def run_all_examples():
    print("=" * 60)
    print("CARGO PACKING GENETIC ALGORITHM - TEST INSTANCES")
    print("=" * 60)
    
    instances = get_all_test_instances()
    solvers = []
    
    for instance in instances:
        solver = run_instance(instance)
        solvers.append(solver)
    
    print("\nAll tests completed!")
    return solvers


if __name__ == "__main__":
    run_all_examples()