import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import AgglomerativeClustering
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


# 그룹화 결과 출력 함수
def print_clusters(students, labels):
    print("\nCluster Results:")
    clusters = {}
    for i, label in enumerate(labels):
        clusters.setdefault(label, []).append(students[i]["name"])  # 같은 그룹의 학생들을 묶음
    for cluster_id, names in clusters.items():
        print(f"Group {cluster_id}: {', '.join(names)}")


if __name__ == "__main__":
    students = load_from_json("students_data.json")

    # 학생 벡터 추출/ 유사도 행렬 계산
    student_vectors = [student["vector"] for student in students]
    similarity_matrix = calculate_similarity_matrix(student_vectors)

    # 유사도 행렬 출력
    print_similarity_matrix(students, similarity_matrix)

    # 클러스터링 수행 (Agglomerative Clustering 사용)
    clustering = AgglomerativeClustering(
        n_clusters=None,  # 자동으로 클러스터 수 결정
        distance_threshold=0.7,  # 유사도 임계값 설정 (1 - threshold = 거리)
        metric="precomputed",  # 사전 계산된 유사도 행렬 사용
        linkage="complete"  # 가장 멀리 떨어진 두 점 사이의 거리 기준
    )
    labels = clustering.fit_predict(1 - similarity_matrix)  # 거리 행렬로 변환 후 클러스터링

    # 그룹화 결과 출력
    print_clusters(students, labels)