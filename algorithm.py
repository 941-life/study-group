import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import AgglomerativeClustering
from vector import load_from_json
from sklearn.manifold import MDS
import logging
from typing import List, Dict, Any, Tuple, Optional
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

class ClusteringError(Exception):
    """Custom exception for clustering-related errors"""
    pass

# Similarity Calculation
def calculate_similarity_matrix(vectors: List[List[int]]) -> np.ndarray:
    """
    Calculate cosine similarity matrix from student vectors.
    
    Args:
        vectors: List of student vectors
    
    Returns:
        Cosine similarity matrix
    
    Raises:
        ClusteringError: If there's an error calculating the similarity matrix
    """
    try:
        vectors_array = np.array(vectors)
        similarity_matrix = cosine_similarity(vectors_array)
        logger.info("Successfully calculated similarity matrix")
        return similarity_matrix
    except Exception as e:
        logger.error(f"Error calculating similarity matrix: {e}")
        raise ClusteringError(f"Failed to calculate similarity matrix: {e}")

# Similarity matrix print
def print_similarity_matrix(students: List[Dict[str, Any]], matrix: np.ndarray) -> None:
    """
    Print the similarity matrix in a formatted manner.
    
    Args:
        students: List of student data dictionaries
        matrix: Similarity matrix
    """
    try:
        print("\nSimilarity Matrix:")
        print("-" * 80)
        print("Student Names:", end="\t")
        for student in students:
            print(f"{student['name']:>10}", end="\t")
        print("\n" + "-" * 80)
        
        for i, student in enumerate(students):
            print(f"{student['name']:<10}", end="\t")
            for j in range(len(students)):
                print(f"{matrix[i][j]:10.3f}", end="\t")
            print()
        print("-" * 80)
    except Exception as e:
        logger.error(f"Error printing similarity matrix: {e}")
def print_similarity_matrix(json, matrix):
    print("\nSimilarity Matrix:")

    # header, print student's name and dividing line
    header = (" " * 10) + " ".join([f"{student['name'][:10]:>10}" for student in json])
    print(header)
    print("-" * (10 + (11 * len(json))))  # add '-' for readability

    # similarity matrix
    for i, student in enumerate(json):
        row = " ".join([f"{matrix[i, j]:>10.2f}" for j in range(len(json))])
        print(f"{student['name'][:10]:<10} {row}")

# Return AgglomerativeClustering with initialize
def agglomerative_clustering():
    agglo_clustering = AgglomerativeClustering(
        n_clusters=None,  # Automatically determine the number of clusters
        distance_threshold=0.7,  # Set similarity threshold (1 - threshold = distance)
        metric="precomputed",  # Using a pre-calculated similarity matrix
        linkage="complete"  # Calculate the distances between clusters: complete Linkage
    )
    return agglo_clustering

# Grouping result print
def print_clusters(students, labels):
    print("\nCluster Results:")
    clusters = {}
    for i, label in enumerate(labels):
        clusters.setdefault(label, []).append(students[i]["name"])  # Bind same group's student
    for cluster_id, names in clusters.items():
        print(f"Group {cluster_id}: {', '.join(names)}")

# Return MDS scaled matrix, default : 2-d
def mds_scaling(matrix):
    """
    :MDS:
    Create an instance of an MDS class
        n_components : number of dimensions; 2-d
        dissimilarity : Indicators indicating distance or similarity between data; use pre-computed matrix
        random_state : Random seed to make the difference between outcomes due to amorphousness constant
    """
    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=42)
    coordinates = mds.fit_transform(matrix)
    return coordinates

if __name__ == "__main__":
    students = load_from_json("students_data.json")

    # Student vector extraction / Calculate the Similarity Matrix
    student_vectors = [student["vector"] for student in students]
    similarity_matrix = calculate_similarity_matrix(student_vectors)

    print_similarity_matrix(students, similarity_matrix)

    # Converting to distance matrix
    distance_matrix = 1 - similarity_matrix

    # Receives Agglomeration clustering with values set / clustering
    clustering = agglomerative_clustering()
    labels = clustering.fit_predict(distance_matrix)

    print_clusters(students, labels)
