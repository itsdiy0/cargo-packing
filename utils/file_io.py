from models import Container, Cylinder

def load_instance_from_file(filepath):
    """
    Load a problem instance from a text file
    
    Expected format:
    container <width> <depth> <max_weight>
    cylinder <diameter> <weight>
    cylinder <diameter> <weight>
    
    """
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    container = None
    cylinders = []
    
    for line in lines:
        line = line.strip()
        
        if not line or line.startswith('#'):
            continue
        
        parts = line.split()
        
        if parts[0] == 'container':
            width = float(parts[1])
            depth = float(parts[2])
            max_weight = float(parts[3])
            container = Container(width, depth, max_weight)
        
        elif parts[0] == 'cylinder':
            diameter = float(parts[1])
            weight = float(parts[2])
            cylinder_id = len(cylinders)
            cylinders.append(Cylinder(cylinder_id, diameter, weight))
    
    if container is None:
        raise ValueError(f"No container definition found in {filepath}")
    
    if len(cylinders) == 0:
        raise ValueError(f"No cylinders found in {filepath}")
    
    return container, cylinders


def save_solution_to_file(filepath, dna, container, cylinders, fitness, details=None):
    """
    Save a solution to a text file
    
    Format:
    placement_order <id1> <id2> <id3> ...
    fitness <value>
    cylinder <id> <x> <y> <diameter> <weight>
    ...
    """
    with open(filepath, 'w') as f:
        f.write(f"placement_order {' '.join(map(str, dna.genes))}\n")
        f.write(f"fitness {fitness:.2f}\n")
        
        if details:
            f.write(f"valid {details['valid']}\n")
            f.write(f"center_of_mass {details['center_of_mass'][0]:.2f} {details['center_of_mass'][1]:.2f}\n")
            f.write(f"packing_density {details['packing_density']:.4f}\n")
            f.write("\n")
            
            for cyl in details['cylinders']:
                if cyl.placed:
                    f.write(f"cylinder {cyl.id} {cyl.x:.2f} {cyl.y:.2f} {cyl.diameter:.2f} {cyl.weight:.2f}\n")


def load_solution_from_file(filepath):
    """
    Load a solution from a text file
    
    Returns:
        dict with keys: placement_order, fitness, cylinders
    """
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    solution = {
        'placement_order': None,
        'fitness': None,
        'valid': None,
        'center_of_mass': None,
        'packing_density': None,
        'cylinders': []
    }
    
    for line in lines:
        line = line.strip()
        
        if not line or line.startswith('#'):
            continue
        
        parts = line.split()
        
        if parts[0] == 'placement_order':
            solution['placement_order'] = list(map(int, parts[1:]))
        
        elif parts[0] == 'fitness':
            solution['fitness'] = float(parts[1])
        
        elif parts[0] == 'valid':
            solution['valid'] = parts[1] == 'True'
        
        elif parts[0] == 'center_of_mass':
            solution['center_of_mass'] = (float(parts[1]), float(parts[2]))
        
        elif parts[0] == 'packing_density':
            solution['packing_density'] = float(parts[1])
        
        elif parts[0] == 'cylinder':
            cyl_data = {
                'id': int(parts[1]),
                'x': float(parts[2]),
                'y': float(parts[3]),
                'diameter': float(parts[4]),
                'weight': float(parts[5])
            }
            solution['cylinders'].append(cyl_data)
    
    return solution