import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from visualization import visualize_all_solutions, visualize_solution_from_files

def main():
    print("GENERATING SOLUTION VISUALIZATIONS")
    print("-" * 60)
    
    # Generate all visualizations
    visualize_all_solutions(
        solutions_dir="data/solutions",
        output_dir="visualization/results",
        show=False  # Set to True to display each one
    )
    
    print("\n" + "-" * 60)
    print("VISUALIZATION COMPLETE")

def visualize_specific_instance():
    """Example: Visualize a specific instance"""
    print("\nVisualizing specific instance...")
    
    visualize_solution_from_files(
        instance_file="data/challenging/instance_04.txt",
        solution_file="data/solutions/challenging/instance_04_solution.txt",
        save_path="visualizations/challenging_04_detailed.png",
        show=True  # Display this one
    )


if __name__ == "__main__":
    main()
