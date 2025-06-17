import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Any
import logging
import os
from config import *

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, LOG_LEVEL))

# Create console handler if no handlers exist
if not logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, LOG_LEVEL))
    formatter = logging.Formatter(LOG_FORMAT)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

def show_clustering(names: List[str], labels: np.ndarray, coordinates: np.ndarray, save_plot: bool = False) -> None:
    """
    Visualize clustering results in 2D space.
    
    Args:
        names: List of student names
        labels: Cluster labels for each student
        coordinates: MDS coordinates for visualization
        save_plot: Whether to save the plot as an image
    
    Raises:
        Exception: If there's an error during visualization
    """
    try:
        plt.figure(figsize=PLOT_FIGURE_SIZE)
        
        # Get unique cluster labels and generate colors
        unique_labels = np.unique(labels)
        colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_labels)))
        
        # Create scatter plot for each cluster
        for label, color in zip(unique_labels, colors):
            mask = labels == label
            plt.scatter(
                coordinates[mask, 0],
                coordinates[mask, 1],
                c=[color],
                label=f'Cluster {label + 1}',
                alpha=0.6
            )
            
            # Add student names as labels
            for i, name in enumerate(names):
                if mask[i]:
                    plt.annotate(
                        name,
                        (coordinates[i, 0], coordinates[i, 1]),
                        xytext=(5, 5),
                        textcoords='offset points',
                        fontsize=PLOT_FONT_SIZE
                    )
        
        # Customize plot
        plt.title("Student Clustering Results", fontsize=PLOT_FONT_SIZE + 2)
        plt.xlabel("Dimension 1", fontsize=PLOT_FONT_SIZE)
        plt.ylabel("Dimension 2", fontsize=PLOT_FONT_SIZE)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(fontsize=PLOT_FONT_SIZE)
        
        # Set background color
        plt.gca().set_facecolor('#f8f9fa')
        plt.gcf().set_facecolor('white')
        
        # Adjust layout
        plt.tight_layout()
        
        # Save plot if requested
        if save_plot:
            os.makedirs('docs/images', exist_ok=True)
            plt.savefig('docs/images/clustering_results.png', dpi=300, bbox_inches='tight')
            logger.info("Saved clustering results plot to docs/images/clustering_results.png")
        
        plt.show()
        
        logger.info("Successfully displayed clustering visualization")
    except Exception as e:
        logger.error(f"Error displaying clustering: {e}")
        raise

if __name__ == "__main__":
    try:
        # Load and process student data
        from vector import load_from_json
        from algorithm import process_student_data
        
        students = load_from_json()
        if not students:
            print("No student data found. Please add some students first.")
            exit(1)
        
        # Process data
        _, _, labels, coordinates = process_student_data(students)
        
        # Extract student names
        names = [student["name"] for student in students]
        
        # Show visualization and save plot
        show_clustering(names, labels, coordinates, save_plot=True)
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"\nAn unexpected error occurred: {e}")
