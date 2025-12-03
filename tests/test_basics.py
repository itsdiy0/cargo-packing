import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models import Container, Cylinder
from utils import calculate_center_of_mass, check_all_constraints

def test_container():
    print("Testing Container class...")
    
    container = Container(20, 15, 1000)
    print(f"  Created: {container}")
    print(f"  Safe X zone: {container.safe_x_min} to {container.safe_x_max}")
    print(f"  Safe Y zone: {container.safe_y_min} to {container.safe_y_max}")
    
    assert container.is_position_inside(10, 7.5, 2) == True
    assert container.is_position_inside(1, 7.5, 2) == False
    assert container.is_position_inside(19, 7.5, 2) == False
    
    print("  Container tests passed")


def test_cylinder():
    print("\nTesting Cylinder class...")
    
    cyl1 = Cylinder(0, 2.0, 100)
    cyl2 = Cylinder(1, 3.0, 150)
    
    print(f"  Created: {cyl1}")
    print(f"  Created: {cyl2}")
    
    cyl1.set_position(5, 5)
    cyl2.set_position(10, 5)
    
    print(f"  After placement: {cyl1}")
    print(f"  After placement: {cyl2}")
    
    distance = cyl1.distance_to(cyl2)
    print(f"  Distance between cylinders: {distance:.2f}m")
    
    assert cyl1.overlaps_with(cyl2) == False
    
    cyl2.set_position(6, 5)
    assert cyl1.overlaps_with(cyl2) == True
    
    print("  Cylinder tests passed")


def test_center_of_mass():
    print("\nTesting center of mass calculation...")
    
    cyl1 = Cylinder(0, 2.0, 100)
    cyl2 = Cylinder(1, 2.0, 200)
    cyl3 = Cylinder(2, 2.0, 150)
    
    cyl1.set_position(5, 5)
    cyl2.set_position(10, 8)
    cyl3.set_position(12, 10)
    
    cylinders = [cyl1, cyl2, cyl3]
    
    center_x, center_y = calculate_center_of_mass(cylinders)
    print(f"  Center of mass: ({center_x:.2f}, {center_y:.2f})")
    
    expected_x = (100*5 + 200*10 + 150*12) / 450
    expected_y = (100*5 + 200*8 + 150*10) / 450
    
    assert abs(center_x - expected_x) < 0.01
    assert abs(center_y - expected_y) < 0.01
    
    print("  Center of mass tests passed")


def test_constraints():
    print("\nTesting constraint checking...")
    
    container = Container(20, 15, 1000)
    
    cyl1 = Cylinder(0, 2.0, 100)
    cyl2 = Cylinder(1, 2.0, 200)
    cyl1.set_position(10, 7)
    cyl2.set_position(12, 8)
    
    cylinders = [cyl1, cyl2]
    
    is_valid, message = check_all_constraints(cylinders, container)
    print(f"  Valid config: {is_valid} - {message}")
    assert is_valid
    
    cyl2.set_position(10.5, 7)
    is_valid, message = check_all_constraints(cylinders, container)
    print(f"  Overlap config: {is_valid} - {message}")
    assert not is_valid
    
    print("  Constraint tests passed")


if __name__ == "__main__":
    print("=" * 50)
    print("RUNNING BASIC TESTS")
    print("=" * 50)
    test_container()
    test_cylinder()
    test_center_of_mass()
    test_constraints()
    
    print("\n" + "=" * 50)
    print("ALL TESTS PASSED")
    print("=" * 50)