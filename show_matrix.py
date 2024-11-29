import algorithm
import matplotlib.pyplot as plt
from vector import load_from_json

def show_distance_matrix(names, coordinates):

    # graph size
    plt.figure(figsize=(8, 6))

    # Marking dots
    plt.scatter(coordinates[:, 0], coordinates[:, 1], color='blue')

    # Map the student name for each point
    for i, name in enumerate(names):
        plt.text(coordinates[i, 0], coordinates[i, 1], name, fontsize=10, ha='right')

    plt.xlabel("Dimension 1")
    plt.ylabel("Dimension 2")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    students = load_from_json("students_data.json")
    student_names = [student['name'] for student in students] # student name list

    # Student vector extraction / Calculate the Similarity Matrix
    student_vectors = [student["vector"] for student in students]
    similarity_matrix = algorithm.calculate_similarity_matrix(student_vectors)

    # Converting to distance matrix
    distance_matrix = 1 - similarity_matrix

    # Converting multi dimension Distance Matrix to 2d Matrix
    mds_coordinates = algorithm.mds_scaling(distance_matrix)

    show_distance_matrix(student_names, mds_coordinates)



