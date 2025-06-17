from vector import load_from_json
from show_matrix import show_distance_matrix
from show_clustering import show_clustering
from algorithm import calculate_similarity_matrix, mds_scaling, agglomerative_clustering


def generate_visualizations():
    # Load student data
    students = load_from_json()
    if not students:
        print("No student data found. Please add some students first.")
        return

    # Extract names and vectors
    names = [student["name"] for student in students]
    vectors = [student["vector"] for student in students]

    # Calculate similarity matrix
    similarity_matrix = calculate_similarity_matrix(vectors)
    # Convert to distance matrix
    distance_matrix = 1 - similarity_matrix
    # MDS for 2D coordinates
    coordinates = mds_scaling(distance_matrix)
    # Clustering
    clustering = agglomerative_clustering()
    labels = clustering.fit_predict(distance_matrix)

    # Visualize similarity matrix
    show_distance_matrix(names, coordinates, save_plot=True)
    # Visualize clustering
    show_clustering(names, labels, coordinates, save_plot=True)

if __name__ == "__main__":
    generate_visualizations() 