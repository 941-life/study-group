import algorithm
import matplotlib.pyplot as plt
from vector import load_from_json
#from scipy.cluster.hierarchy import dendrogram, linkage

def show_clustering(names, labels, coordinates):

    # Plotting the clustering result in 2D space
    plt.figure(figsize=(8, 6))
    colors = ['red', 'green', 'blue', 'yellow', 'black']

    # Scatter plot with cluster labels
    for i in range(max(labels) + 1):
        cluster_points = coordinates[labels == i]
        plt.scatter(cluster_points[:, 0], cluster_points[:, 1], color=colors[i], label=f"Cluster {i + 1}")

    # Adding labels to the points
    for i, name in enumerate(names):
        plt.text(coordinates[i, 0], coordinates[i, 1], name, fontsize=10, ha='right')

    plt.xlabel("Dimension 1")
    plt.ylabel("Dimension 2")
    plt.legend()
    plt.grid(True)
    plt.show()

    """
    # dendrogram
    linkage_matrix = linkage(distance_matrix, method='average')
    plt.figure(figsize=(10, 6))
    dendrogram(linkage_matrix, labels=names, leaf_rotation=90, leaf_font_size=10)
    plt.title("Dendrogram of Agglomerative Clustering")
    plt.xlabel("Students")
    plt.ylabel("Distance")
    plt.show()
    """


if __name__ == "__main__":
    students = load_from_json("students_data.json")
    student_names = [student['name'] for student in students] # student name list

    # Student vector extraction / Calculate the Similarity Matrix
    student_vectors = [student["vector"] for student in students]
    similarity_matrix = algorithm.calculate_similarity_matrix(student_vectors)

    # Converting to distance matrix
    distance_matrix = 1 - similarity_matrix

    # Receives Agglomeration clustering with values set / clustering
    clustering = algorithm.agglomerative_clustering()
    agglo_clustering_labels = clustering.fit_predict(distance_matrix)

    # Converting multi dimension Distance Matrix to 2d Matrix
    mds_coordinates = algorithm.mds_scaling(distance_matrix)

    # show clustered result
    show_clustering(student_names, agglo_clustering_labels, mds_coordinates)
