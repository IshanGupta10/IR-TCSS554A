# imports for the given class
import numpy as np
import pandas as pd
import copy
import argparse


class PageRank:
    '''
    PageRank class to calculate Page Rank for
    given graph of connected web pages.
    '''
    def __init__(self):
        self.power = 0
        self.original_vector = None
        self.converged_vector = None
        self.graph = dict()
        self.m_matrix = list()

    def generate_graph(self, file_path):
        '''
        Creates adjacency list from the connected
        compunents given in the file.
        :param file_path: path of the txt file.
        :return: None
        '''
        with open(file_path, 'r') as _file:
            for line in _file:
                connection = line.strip().split()
                if connection[0] not in self.graph:
                    self.graph[connection[0]] = []
                    if connection[2] == "1":
                        self.graph[connection[0]].append(connection[1])
                else:
                    if connection[2] == "1":
                        self.graph[connection[0]].append(connection[1])

    def generate_m_matrix(self):
        '''
        Creates M matrix from the adjacency list of the graph.
        :return: None
        '''
        df = pd.DataFrame(columns=self.graph.keys(), index=self.graph.keys())
        df = df.fillna(0.0)

        for key, val in self.graph.items():
            for i in range(0, len(val)):
                df.loc[val[i], key] = 1 / len(val)

        self.m_matrix = df.values

    def generate_a_matrix(self, beta):
        '''
        Generates A Matrix from the help of beta
        and equation A_Matrix =  beta * M_Matrix + (1 - beta)/total_nodes
        :param beta: beta value
        :return: A_Matrix
        '''
        teleport_factor = (1.0 - beta) / len(self.graph)
        return beta * self.m_matrix + teleport_factor

    def generate_rank_vectors(self):
        '''
        Generates rank vectors for calculations of Page Ranks.
        :return: None.
        '''
        self.original_vector = list()
        self.converged_vector = list()

        for i in range(0, len(self.graph.keys())):
            self.original_vector.append(1 / len(self.graph.keys()))

        self.original_vector = np.matrix(self.original_vector).T

        self.converged_vector = copy.deepcopy(self.original_vector)
        self.converged_vector.fill(0)

    def power_converge(self, beta):
        '''
        Calculates power iterations and converged page ranks
        for given matrices.
        :param beta: beta value.
        :return: converged pang rank vectors.
        '''
        self.power = 0
        rank_vector_t = copy.deepcopy(self.original_vector)
        teleport_factor = (1.0 - beta) / len(self.graph.keys())

        while not np.allclose(rank_vector_t, self.converged_vector, rtol=1e-06, atol=1e-06):
            rank_vector_t = self.original_vector
            self.converged_vector = beta * self.m_matrix * rank_vector_t + teleport_factor
            self.original_vector = self.converged_vector
            self.power += 1

        return self.power, self.converged_vector


def get_arguments():
    '''
    processes arguments from command line.
    :return: processed command line arguments.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", help="path to the graph file")
    parser.add_argument("--beta", help="value for the beta")
    return parser.parse_args()


if __name__ == '__main__':

    args = get_arguments()

    pageRankObject = PageRank()
    pageRankObject.generate_graph(args.file_path)

    pageRankObject.generate_m_matrix()
    print ("M Matrix :")
    print (pageRankObject.m_matrix)

    a_matrix = pageRankObject.generate_a_matrix(float(args.beta))
    print ("A Matrix : ")
    print (a_matrix)

    pageRankObject.generate_rank_vectors()
    print ("Original Rank Vector : ")
    print (pageRankObject.original_vector)

    iterations_a, converged_vector_a = pageRankObject.power_converge(float(args.beta))
    print ("Power Iterations A : ", iterations_a)
    print ("Converged Vector for A : ")
    print (converged_vector_a)

    # For M matrix the value of beta = 1.0
    args.beta = 1.0
    pageRankObject.generate_rank_vectors()
    iterations_m, converged_vector_m = pageRankObject.power_converge(args.beta)
    print ("Power Iterations for M : ", iterations_m)
    print ("Converged Vector for M : ")
    print (converged_vector_m)