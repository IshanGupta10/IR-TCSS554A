# imports
import numpy as np
import pandas as pd

##################################
# function to create adjacency list
# from graph of the webpages.
##################################
def generate_adjacency_list():
    adjacency_list = dict()

    with open('./graph.txt', 'r') as _file:
        for line in _file:
            connection = line.strip().split()
            if connection[0] not in adjacency_list:
                adjacency_list[connection[0]] = []
                if connection[2] == "1":
                    adjacency_list[connection[0]].append(connection[1])
            else:
                if connection[2] == "1":
                    adjacency_list[connection[0]].append(connection[1])

    return adjacency_list


##################################
# generates M Matrix from the adjacency
# list
##################################
def generate_m_matrix(graph):
    df = pd.DataFrame(columns=graph.keys(), index=graph.keys(), dtype="double")
    df = df.fillna(0.0)

    for key, val in graph.items():
        for i in range(0, len(val)):
            df.loc[val[i], key] = 1 / len(val)

    m_matrix = df.values

    return m_matrix


##################################
# generates original rank vector from
# the adjancecy list
##################################
def generate_original_rank_vector(graph):
    original_rank_vector = []

    for i in range(0, len(graph.keys())):
        original_rank_vector.append(1 / len(graph.keys()))

    original_rank_vector = np.matrix(original_rank_vector).T

    return original_rank_vector


##################################
# generates A matrix using M matrix
# follows the equation given in the
# PageRank presentation.
##################################
def generate_A_matrix(graph, m_matrix, beta):

    teleport_factor = (1 - beta) / len(graph) # this is teleport propbability
    a_matrix = beta * m_matrix + teleport_factor

    return a_matrix


##################################
# power iteration method for M
# matrix using equation r(t+1) = M * r(t)
##################################
def power_converge_m_matrix(rank_vector, m_matrix):
    power = 0
    rank_vector_t = rank_vector
    rank_vector_t_plus_1 = np.empty(shape=(len(rank_vector), 1))
    rank_vector_t_plus_1.fill(0)

    while not np.allclose(rank_vector_t, rank_vector_t_plus_1, rtol=1e-06, atol=1e-06):
        rank_vector_t = rank_vector
        rank_vector_t_plus_1 = m_matrix * rank_vector_t
        rank_vector = rank_vector_t_plus_1
        power += 1

    return power, rank_vector_t_plus_1


##################################
# power iteration method for A
# matrix using equation -
# r(t+1) = Sigma(beta * M Matrix * r(t) + ((1-beta)/(total_nodes)))
##################################
def power_converge_a_matrix(graph, rank_vector, m_matrix, beta):
    power = 0
    rank_vector_t = rank_vector
    rank_vector_t_plus_1 = np.empty(shape=(len(rank_vector), 1))
    rank_vector_t_plus_1.fill(0)
    teleport_factor = (1 - beta) / len(graph) # this is teleport propbability

    while not np.allclose(rank_vector_t, rank_vector_t_plus_1, rtol=1e-06, atol=1e-06):
        rank_vector_t = rank_vector
        rank_vector_t_plus_1 = beta * m_matrix * rank_vector_t + teleport_factor
        rank_vector = rank_vector_t_plus_1
        power += 1

    return power, rank_vector_t_plus_1


if __name__ == '__main__':
    graph = generate_adjacency_list()
    m_matrix = generate_m_matrix(graph)
    rank_vector = generate_original_rank_vector(graph)
    beta = 0.85
    a_matrix = generate_A_matrix(graph, m_matrix, beta)
    m_iterations, final_rank_vector_m = power_converge_m_matrix(rank_vector, m_matrix)
    a_iterations, final_rank_vector_a = power_converge_a_matrix(graph, rank_vector, m_matrix, beta)
    print ('Iterations M : ', m_iterations)
    print ('Iterations A : ', a_iterations)
    print ('Original Rank Vector : ')
    print (rank_vector)
    print ('Matrix M : ')
    print (m_matrix)
    print ('Matrix A : ')
    print (a_matrix)
    print ('Final Rank Vector M : ')
    print (final_rank_vector_m)
    print ('Final Rank Vector A : ')
    print (final_rank_vector_a)
