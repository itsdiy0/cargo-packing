"""
Container class - represents the rectangular cargo container
"""
class Container:
    def __init__(self, width, depth, max_weight):
        # Initialize container dimensions and weight limit
        self.width = width
        self.depth = depth
        self.max_weight = max_weight
        # Define safe zone boundaries (20% to 80% of width and depth)
        self.safe_x_min = width * 0.2
        self.safe_x_max = width * 0.8
        self.safe_y_min = depth * 0.2
        self.safe_y_max = depth * 0.8
    
    def is_position_inside(self, x, y, radius):
        # Check if a circle with given radius at (x, y) fits inside the container
        left_ok = (x - radius) >= 0
        right_ok = (x + radius) <= self.width
        rear_ok = (y - radius) >= 0
        front_ok = (y + radius) <= self.depth
        
        return left_ok and right_ok and rear_ok and front_ok
    
    def is_center_of_mass_valid(self, center_x, center_y):
        # Check if the center of mass is within the safe zone
        x_valid = self.safe_x_min <= center_x <= self.safe_x_max
        y_valid = self.safe_y_min <= center_y <= self.safe_y_max
        
        return x_valid and y_valid
    
    def __str__(self):
        return f"Container({self.width}m x {self.depth}m, max_weight={self.max_weight}kg)"