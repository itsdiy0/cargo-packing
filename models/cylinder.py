import math
"""
Cylinder class - represents a cylindrical container (barrel/drum) - object on the cargo
"""
class Cylinder:
    def __init__(self, cylinder_id, diameter, weight):
        # Initialize cylinder properties
        self.id = cylinder_id
        self.diameter = diameter
        self.radius = diameter / 2.0
        self.weight = weight
        # Position attributes
        self.x = None
        self.y = None
        self.placed = False
    
    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.placed = True
    
    def distance_to(self, other_cylinder):
        # Calculate Euclidean distance to another cylinder
        if not self.placed or not other_cylinder.placed:
            return float('inf')
        
        dx = self.x - other_cylinder.x
        dy = self.y - other_cylinder.y
        return math.sqrt(dx * dx + dy * dy)
    
    def overlaps_with(self, other_cylinder):
        # Check if this cylinder overlaps with another cylinder
        if not self.placed or not other_cylinder.placed:
            return False
        
        distance = self.distance_to(other_cylinder)
        min_distance = self.radius + other_cylinder.radius
        
        return distance < min_distance
    
    def get_area(self):
        return math.pi * self.radius * self.radius
    
    def __str__(self):
        if self.placed:
            return f"Cylinder{self.id}(d={self.diameter}m, w={self.weight}kg, pos=({self.x:.2f}, {self.y:.2f}))"
        else:
            return f"Cylinder{self.id}(d={self.diameter}m, w={self.weight}kg, not placed)"