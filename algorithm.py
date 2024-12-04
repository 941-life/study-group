import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import AgglomerativeClustering
from vector import load_from_json
from sklearn.manifold import MDS

# Similarity Calculation
def calculate_similarity_matrix(vectors):
    array_vectors = np.array(vectors)  # convert list into numpy array
    matrix = cosine_similarity(array_vectors)  # calculate cosine similarity matrix
    return matrix

# Similarity matrix print
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
    students = load_from_json("students_data.json") # load json

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
