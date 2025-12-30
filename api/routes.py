from flask import Blueprint, request, jsonify, Response
from models import Container, Cylinder, DNA
from solvers import CargoPackingSolver
from algorithms import GreedyAlgorithm, RandomSearch, GreedyPlacer, hill_climbing
from utils import calculate_center_of_mass, calculate_packing_density, check_all_constraints
import json
import time
import copy

api_bp = Blueprint('api', __name__)

@api_bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})


@api_bp.route('/solve', methods=['POST'])
def solve():
    """
    Solve a custom problem instance
    """
    data = request.json
    
    container_data = data.get('container')
    cylinders_data = data.get('cylinders')
    algorithm = data.get('algorithm', 'genetic')
    params = data.get('params', {})
    
    container = Container(
        width=float(container_data['width']),
        depth=float(container_data['depth']),
        max_weight=float(container_data['max_weight'])
    )
    
    cylinders = []
    for i, cyl in enumerate(cylinders_data):
        cylinders.append(Cylinder(
            cylinder_id=i,
            diameter=float(cyl['diameter']),
            weight=float(cyl['weight'])
        ))
    
    placer = GreedyPlacer(step_size=params.get('step_size', 0.3))
    
    result = None
    
    if algorithm == 'genetic':
        solver = CargoPackingSolver(
            container=container,
            cylinders=cylinders,
            population_size=params.get('population_size', 100),
            mutation_rate=params.get('mutation_rate', 0.05),
            step_size=params.get('step_size', 0.3)
        )
        
        solution = solver.solve(
            max_generations=params.get('max_generations', 200),
            verbose=False,
            use_local_search=params.get('use_local_search', True)
        )
        
        if solution:
            details = solver.get_solution_details(solution)
            result = {
                'algorithm': 'Genetic Algorithm',
                'solution': solution.genes,
                'fitness': solution.fitness,
                'details': {
                    'valid': details['valid'],
                    'center_of_mass': details['center_of_mass'],
                    'packing_density': details['packing_density'],
                    'cylinders': [
                        {
                            'id': cyl.id,
                            'x': cyl.x,
                            'y': cyl.y,
                            'diameter': cyl.diameter,
                            'radius': cyl.radius,
                            'weight': cyl.weight
                        }
                        for cyl in details['cylinders']
                    ]
                },
                'generation_history': [
                    {'generation': h['generation'], 'best': h['best'], 'avg': h['avg']}
                    for h in solver.generation_history
                ]
            }
    
    elif algorithm == 'greedy':
        solver = GreedyAlgorithm(cylinders, container, placer)
        solution = solver.solve(strategy=params.get('strategy', 'largest_first'), verbose=False)
        
        if solution:
            cylinder_copies = [copy.deepcopy(c) for c in cylinders]
            placer.place_cylinders(cylinder_copies, solution.genes, container)
            center_x, center_y = calculate_center_of_mass(cylinder_copies)
            density = calculate_packing_density(cylinder_copies, container)
            is_valid, _ = check_all_constraints(cylinder_copies, container)
            
            result = {
                'algorithm': 'Greedy Algorithm',
                'solution': solution.genes,
                'fitness': solution.fitness,
                'details': {
                    'valid': is_valid,
                    'center_of_mass': (center_x, center_y),
                    'packing_density': density,
                    'cylinders': [
                        {
                            'id': cyl.id,
                            'x': cyl.x,
                            'y': cyl.y,
                            'diameter': cyl.diameter,
                            'radius': cyl.radius,
                            'weight': cyl.weight
                        }
                        for cyl in cylinder_copies
                    ]
                }
            }
    
    elif algorithm == 'random':
        solver = RandomSearch(cylinders, container, placer)
        solution = solver.solve(num_trials=params.get('num_trials', 1000), verbose=False)
        
        if solution:
            cylinder_copies = [copy.deepcopy(c) for c in cylinders]
            placer.place_cylinders(cylinder_copies, solution.genes, container)
            center_x, center_y = calculate_center_of_mass(cylinder_copies)
            density = calculate_packing_density(cylinder_copies, container)
            is_valid, _ = check_all_constraints(cylinder_copies, container)
            
            stats = solver.get_statistics()
            
            result = {
                'algorithm': 'Random Search',
                'solution': solution.genes,
                'fitness': solution.fitness,
                'details': {
                    'valid': is_valid,
                    'center_of_mass': (center_x, center_y),
                    'packing_density': density,
                    'cylinders': [
                        {
                            'id': cyl.id,
                            'x': cyl.x,
                            'y': cyl.y,
                            'diameter': cyl.diameter,
                            'radius': cyl.radius,
                            'weight': cyl.weight
                        }
                        for cyl in cylinder_copies
                    ]
                },
                'statistics': stats
            }
    
    if result:
        return jsonify({'success': True, 'result': result})
    else:
        return jsonify({'success': False, 'error': 'No solution found'}), 400


@api_bp.route('/solve-stream', methods=['POST', 'OPTIONS'])
def solve_stream():
    if request.method == 'OPTIONS':
        response = Response()
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
    
    data = request.json
    
    container_data = data.get('container')
    cylinders_data = data.get('cylinders')
    params = data.get('params', {})
    
    container = Container(
        width=float(container_data['width']),
        depth=float(container_data['depth']),
        max_weight=float(container_data['max_weight'])
    )
    
    cylinders = []
    for i, cyl in enumerate(cylinders_data):
        cylinders.append(Cylinder(
            cylinder_id=i,
            diameter=float(cyl['diameter']),
            weight=float(cyl['weight'])
        ))
    
    def generate():
        solver = CargoPackingSolver(
            container=container,
            cylinders=cylinders,
            population_size=params.get('population_size', 100),
            mutation_rate=params.get('mutation_rate', 0.05),
            step_size=params.get('step_size', 0.3)
        )
        
        yield f"data: {json.dumps({'type': 'start', 'total_generations': params.get('max_generations', 200)})}\n\n"
        
        max_gens = params.get('max_generations', 200)
        update_interval = max(1, max_gens // 20)
        
        for gen in range(max_gens):
            solver.population.calculate_fitness()
            stats = solver.population.get_stats()
    
            current_best = solver.population.get_best()
            if current_best.fitness > 0 and (solver.best_solution is None or current_best.fitness > solver.best_fitness):
                solver.best_solution = current_best.copy()
                solver.best_fitness = current_best.fitness
    
            # Send update EVERY generation (not just every 10)
            progress_data = {
                'type': 'progress',
                'generation': gen,
                'best_fitness': stats['best'],
                'avg_fitness': stats['avg'],
                'worst_fitness': stats['worst']
            }
    
            if solver.best_solution:
                details = solver.get_solution_details(solver.best_solution)
                if details and details['cylinders']:
                    print(f"Gen {gen}: Sending solution with order {solver.best_solution.genes}, fitness {solver.best_solution.fitness}")
                    progress_data['solution'] = {
                        'placement_order': solver.best_solution.genes,
                        'cylinders': [
                            {
                                'id': cyl.id,
                                'x': cyl.x,
                                'y': cyl.y,
                                'diameter': cyl.diameter,
                                'radius': cyl.radius,
                                'weight': cyl.weight
                            }
                            for cyl in details['cylinders'] if cyl.placed
                        ],
                        'center_of_mass': details['center_of_mass'] if details['center_of_mass'][0] else [0, 0],
                        'packing_density': details['packing_density']
                    }
    
            yield f"data: {json.dumps(progress_data)}\n\n"
            time.sleep(0.05)
    
    response = Response(generate(), mimetype='text/event-stream')
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['X-Accel-Buffering'] = 'no'
    
    return response