# study group matching service
Group matching service using cosine similarity, agglomerative clustering, Multi Dimensional Scaling(MDS).

# Used library

- numpy 
- sklearn (cosine_similarity, AgglomerativeClustering, MDS)
- json
- matplotlib

# Code

[algorithm.py](https://github.com/941-life/study-group/blob/main/algorithm.py) : Main code, here we calculate the cosine similarity, agglomerative clustering, Multi Dimensional Scaling(MDS).

[show_clustering.py](https://github.com/941-life/study-group/blob/main/show_clustering.py) : Visualize clustered data with matplotlib using Algorithm.py's function

[show_matrix.py](https://github.com/941-life/study-group/blob/main/show_matrix.py) : Visualize matrix that transforms a cosine similarity based matrix into a distance matrix

[students_data.json](https://github.com/941-life/study-group/blob/main/students_data.json) : Json file of student’s information including vectorized data

[vector.py](https://github.com/941-life/study-group/blob/main/vector.py) : Preprocessing and vectorize the data from user. Values can be directly entered at the main function and save the data as a json file.

