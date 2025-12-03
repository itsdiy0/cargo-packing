import copy

class GreedyPlacer:
    def __init__(self, step_size=0.5):
        self.step_size = step_size
    
    def place_cylinders(self, cylinders, order, container):
        for cylinder_id in order:
            cylinder = cylinders[cylinder_id]
            
            position = self.find_valid_position(cylinder, cylinders, container)
            
            if position is None:
                return False
            
            cylinder.set_position(position[0], position[1])
        
        return True
    
    def find_valid_position(self, cylinder, cylinders, container):
        start_y = container.safe_y_min + cylinder.radius
        end_y = container.safe_y_max - cylinder.radius
        
        start_x = container.safe_x_min + cylinder.radius
        end_x = container.safe_x_max - cylinder.radius
        
        for y in self._range(start_y, end_y, self.step_size):
            for x in self._range(start_x, end_x, self.step_size):
                if self.is_valid_position(cylinder, x, y, cylinders, container):
                    return (x, y)
        
        return None
    
    def is_valid_position(self, cylinder, x, y, cylinders, container):
        if not container.is_position_inside(x, y, cylinder.radius):
            return False
        
        for other in cylinders:
            if not other.placed:
                continue
            if other.id == cylinder.id:
                continue
            
            dx = x - other.x
            dy = y - other.y
            distance = (dx * dx + dy * dy) ** 0.5
            min_distance = cylinder.radius + other.radius
            
            if distance < min_distance:
                return False
        
        return True
    
    def _range(self, start, stop, step):
        current = start
        while current <= stop:
            yield current
            current += step