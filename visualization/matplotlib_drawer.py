import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.collections import PatchCollection
import os

class MatplotlibDrawer:
    def __init__(self, container, cylinders, title="Container Packing Solution"):
        self.container = container
        self.cylinders = cylinders
        self.title = title
    
    def draw(self, save_path=None, show=True, dpi=150):
        # Draw the solution using matplotlib
        
        fig, ax = plt.subplots(figsize=(12, 10))
        
        self._draw_container(ax)
        self._draw_safe_zone(ax)
        self._draw_cylinders(ax)
        self._draw_center_of_mass(ax)
        self._add_labels(ax)
        
        ax.set_xlim(-0.5, self.container.width + 0.5)
        ax.set_ylim(-0.5, self.container.depth + 0.5)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_xlabel('Width (m)', fontsize=12)
        ax.set_ylabel('Depth (m)', fontsize=12)
        ax.set_title(self.title, fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
            print(f"Saved visualization to {save_path}")
        
        if show:
            plt.show()
        else:
            plt.close(fig)
        
        return fig, ax
    
    def _draw_container(self, ax):
        """Draw container boundary"""
        rect = patches.Rectangle(
            (0, 0), 
            self.container.width, 
            self.container.depth,
            fill=False, 
            edgecolor='black', 
            linewidth=2.5,
            label='Container boundary'
        )
        ax.add_patch(rect)
    
    def _draw_safe_zone(self, ax):
        """Draw the 60% safe zone"""
        safe_width = self.container.safe_x_max - self.container.safe_x_min
        safe_depth = self.container.safe_y_max - self.container.safe_y_min
        
        rect = patches.Rectangle(
            (self.container.safe_x_min, self.container.safe_y_min),
            safe_width,
            safe_depth,
            fill=True,
            facecolor='lightgreen',
            edgecolor='green',
            linewidth=1.5,
            linestyle='--',
            alpha=0.2,
            label='Safe zone (60%)'
        )
        ax.add_patch(rect)
    
    def _draw_cylinders(self, ax):
        """Draw all placed cylinders"""
        colors = plt.cm.Set3.colors
        
        for cyl in self.cylinders:
            if not cyl.placed:
                continue
            
            color = colors[cyl.id % len(colors)]
            
            circle = patches.Circle(
                (cyl.x, cyl.y),
                cyl.radius,
                fill=True,
                facecolor=color,
                edgecolor='darkblue',
                linewidth=2,
                alpha=0.7
            )
            ax.add_patch(circle)
            
            ax.text(
                cyl.x, cyl.y,
                f"{cyl.id}",
                ha='center', va='center',
                fontsize=12, fontweight='bold',
                color='black'
            )
            
            ax.text(
                cyl.x, cyl.y - cyl.radius * 0.4,
                f"ø{cyl.diameter}m",
                ha='center', va='center',
                fontsize=8,
                color='black'
            )
            
            ax.text(
                cyl.x, cyl.y + cyl.radius * 0.4,
                f"{cyl.weight}kg",
                ha='center', va='center',
                fontsize=8,
                color='black'
            )
    
    def _draw_center_of_mass(self, ax):
        """Draw center of mass marker"""
        from utils import calculate_center_of_mass
        
        center_x, center_y = calculate_center_of_mass(self.cylinders)
        
        if center_x is None:
            return
        
        ax.plot(
            center_x, center_y,
            marker='+',
            markersize=20,
            markeredgewidth=3,
            color='red',
            label=f'Center of Mass ({center_x:.2f}, {center_y:.2f})'
        )
        
        ax.plot(
            center_x, center_y,
            marker='o',
            markersize=15,
            markerfacecolor='none',
            markeredgecolor='red',
            markeredgewidth=2
        )
    
    def _add_labels(self, ax):
        """Add info box with statistics"""
        from utils import calculate_packing_density, calculate_total_weight
        
        density = calculate_packing_density(self.cylinders, self.container)
        total_weight = calculate_total_weight(self.cylinders)
        
        info_text = (
            f"Container: {self.container.width}m × {self.container.depth}m\n"
            f"Cylinders: {len([c for c in self.cylinders if c.placed])}/{len(self.cylinders)}\n"
            f"Total weight: {total_weight:.1f}/{self.container.max_weight}kg\n"
            f"Packing density: {density*100:.2f}%"
        )
        
        ax.text(
            0.02, 0.98,
            info_text,
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        )
        
        ax.legend(loc='upper right', fontsize=9)


def visualize_solution_from_files(instance_file, solution_file, save_path=None, show=True):
    # Load and visualize a solution from files

    from utils import load_instance_from_file, load_solution_from_file
    
    container, cylinders = load_instance_from_file(instance_file)
    solution = load_solution_from_file(solution_file)
    
    for cyl_data in solution['cylinders']:
        cyl_id = cyl_data['id']
        cylinders[cyl_id].set_position(cyl_data['x'], cyl_data['y'])
    
    instance_name = os.path.basename(instance_file).replace('.txt', '')
    title = f"Solution: {instance_name} (Fitness: {solution['fitness']:.2f})"
    
    drawer = MatplotlibDrawer(container, cylinders, title=title)
    return drawer.draw(save_path=save_path, show=show)


def visualize_all_solutions(solutions_dir="data/solutions", output_dir="visualizations", show=False):
    # Generate visualizations for all saved solutions
    import glob
    
    os.makedirs(output_dir, exist_ok=True)
    
    for category in ['reference', 'challenging']:
        solution_path = os.path.join(solutions_dir, category)
        
        if not os.path.exists(solution_path):
            continue
        
        solution_files = glob.glob(os.path.join(solution_path, "*_solution.txt"))
        
        print(f"\nGenerating visualizations for {category} instances...")
        
        for solution_file in sorted(solution_files):
            instance_name = os.path.basename(solution_file).replace('_solution.txt', '')
            instance_file = os.path.join('data', category, f'{instance_name}.txt')
            
            if not os.path.exists(instance_file):
                print(f"  Warning: Instance file not found: {instance_file}")
                continue
            
            output_path = os.path.join(output_dir, category, f'{instance_name}.png')
            
            print(f"  Generating: {instance_name}.png")
            
            try:
                visualize_solution_from_files(
                    instance_file,
                    solution_file,
                    save_path=output_path,
                    show=show
                )
            except Exception as e:
                print(f"  Error generating {instance_name}: {e}")
        
        print(f"  Completed {category} instances")
    
    print(f"\nAll visualizations saved to {output_dir}/")