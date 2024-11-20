import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from vector import load_from_json


# 유사도 계산 함수
def calculate_similarity_matrix(student_vectors):
    vectors = np.array(student_vectors)  # List를 NumPy 배열로 변환
    similarity_matrix = cosine_similarity(vectors)  # 코사인 유사도 행렬 계산
    return similarity_matrix


# 유사도 행렬 출력 함수
def print_similarity_matrix(students, similarity_matrix):
    print("\nSimilarity Matrix:")
    header = " " * 15 + " ".join([f"{student['name'][:10]:<10}" for student in students])
    print(header)
    for i, student in enumerate(students):
        row = " ".join([f"{similarity_matrix[i, j]:.2f}" for j in range(len(students))])
        print(f"{student['name'][:10]:<10} {row}")


if __name__ == "__main__":
    students = load_from_json("students_data.json")

    # 학생 벡터 추출/ 유사도 행렬 계산
    student_vectors = [student["vector"] for student in students]
    similarity_matrix = calculate_similarity_matrix(student_vectors)

    # 유사도 행렬 출력
    print_similarity_matrix(students, similarity_matrix)
