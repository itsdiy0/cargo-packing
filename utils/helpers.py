import math

def calculate_center_of_mass(cylinders):
    placed_cylinders = [c for c in cylinders if c.placed]
    
    if not placed_cylinders:
        return None, None
    
    total_weight = sum(c.weight for c in placed_cylinders)
    
    if total_weight == 0:
        return None, None
    
    center_x = sum(c.weight * c.x for c in placed_cylinders) / total_weight
    center_y = sum(c.weight * c.y for c in placed_cylinders) / total_weight
    
    return center_x, center_y


def calculate_total_weight(cylinders):
    return sum(c.weight for c in cylinders if c.placed)


def calculate_packing_density(cylinders, container):
    placed_cylinders = [c for c in cylinders if c.placed]
    
    if not placed_cylinders:
        return 0.0
    
    cylinder_area = sum(c.get_area() for c in placed_cylinders)
    container_area = container.width * container.depth
    
    return cylinder_area / container_area


def check_all_constraints(cylinders, container):
    placed_cylinders = [c for c in cylinders if c.placed]
    
    if len(placed_cylinders) != len(cylinders):
        return False, f"Only {len(placed_cylinders)}/{len(cylinders)} cylinders placed"
    
    for cylinder in placed_cylinders:
        if not container.is_position_inside(cylinder.x, cylinder.y, cylinder.radius):
            return False, f"Cylinder {cylinder.id} is out of bounds"
    
    for i, cyl1 in enumerate(placed_cylinders):
        for cyl2 in placed_cylinders[i+1:]:
            if cyl1.overlaps_with(cyl2):
                return False, f"Cylinders {cyl1.id} and {cyl2.id} overlap"
    
    total_weight = calculate_total_weight(cylinders)
    if total_weight > container.max_weight:
        return False, f"Total weight {total_weight}kg exceeds limit {container.max_weight}kg"
    
    center_x, center_y = calculate_center_of_mass(cylinders)
    if not container.is_center_of_mass_valid(center_x, center_y):
        return False, f"Center of mass ({center_x:.2f}, {center_y:.2f}) outside safe zone"
    
    return True, "All constraints satisfied"