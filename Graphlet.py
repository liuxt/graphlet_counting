import networkx as nx
import matplotlib.pyplot as plt
import time
import numpy as np
import pdb


class Graphlet:
    # class variables
    # 3-nodes triangles
    open_triangle_dict = {}
    close_triangle_dict = {}

    total_close_triangle = []
    total_open_triangle = []
    # 4-nodes
    four_path_dict = {}
    four_chordal_cycle_dict = {}
    four_tailed_triangle_dict = {}
    four_clique_dict = {}
    four_cycle_dict = {}
    three_star_dict = {}

    total_four_path = []
    total_three_star = []
    total_four_cycle = []
    total_four_tailed_triangle = []
    total_four_chordal_cycle = []
    total_four_clique = []

    # 5-nodes, totally 21 of them
    total_five_graphlet = []
    for _ in  range(21):
        total_five_graphlet.append({})

    # 6-nodes, totally 112 of them
    total_six_graphlet = []
    for _ in range(112):
        total_six_graphlet.append({})

    # 7-nodes, totally 853 of them
    total_seven_graphlet = []
    for _ in range(853):
        total_seven_graphlet.append({})

    # initializer
    def __init__(self, init_graph):
        self.G = init_graph
        self._init_all_data()
        self._count_triangles()
        self._count_4_nodes_global()
        self._count_total_5_nodes()

    def show_graph(self):
        nx.draw(self.G, with_labels=True)
        plt.show()

    # print triangles
    def print_triangles(self):
        print("close triangle dict:")
        print(self.close_triangle_dict)
        print("open triangle dict:")
        print(self.open_triangle_dict)

        print("total close triangles:")
        print(self.total_close_triangle)
        print("total open triangles:")
        print(self.total_open_triangle)
        print("number of total close triangle: %d" % len(self.total_close_triangle))
        print("number of totla open triangle: %d" % len(self.total_open_triangle))

    def print_4_nodes(self):
        '''
        print("4 path dict:")
        print(self.four_path_dict)
        print("3 star dict:")
        print(self.three_star_dict)
        print("four cycle dict")
        print(self.four_cycle_dict)
        print("4 tailed triangle:")
        print(self.four_tailed_triangle_dict)
        print("4 chordal cycle:")
        print(self.four_chordal_cycle_dict)
        print("4 clique:")
        print(self.four_clique_dict)
        '''

        print("total four path:")
        print(len(self.total_four_path))
        print("total three star: ")
        print(len(self.total_three_star))
        print("total four cycle: ")
        print(len(self.total_four_cycle))
        print("total four tailed triangle:")
        print(len(self.total_four_tailed_triangle))
        print("total four chordal cycle:")
        print(len(self.total_four_chordal_cycle))
        print("total four clique:")
        print(len(self.total_four_clique))

    def print_5_nodes(self):
        print("total five node graphlets")
        print(self.total_five_graphlet)

    def print_6_nodes(self):
        print("total six node graphlets")
        print(self.total_six_graphlet)


    # add one node and count 3-node graphlets
    def add_one_node(self, added_node, connected_nodes):
        # add_node
        self.G.add_node(added_node)

        # add_edge
        for i in connected_nodes:
            self.G.add_edge(added_node, i)

        k = added_node

        for i in self.G.neighbors(k):
            for j in self.G.neighbors(i):
                if self.G.has_edge(j, k):
                    if i in self.close_triangle_dict:
                        self.close_triangle_dict[i].append((j, k))
                    else:
                        self.close_triangle_dict[i] = []
                        self.close_triangle_dict[i].append((j, k))
                    if i < j:
                        self.total_close_triangle.append((i, j, k))

                else:
                    if i in self.open_triangle_dict:
                        self.open_triangle_dict[i].append((j, k))
                    else:
                        self.open_triangle_dict[i] = []
                        self.open_triangle_dict[i].append((j, k))

                    self.total_open_triangle.append((i, j, k))

        for i in self.G.neighbors(k):
            for j in self.G.neighbors(k):
                if i < j and not self.G.has_edge(i, j):
                    if k in self.open_triangle_dict:
                        self.open_triangle_dict[k].append((i, j))
                    else:
                        self.open_triangle_dict[k] = []
                        self.open_triangle_dict[k].append((i, j))

                    self.total_open_triangle.append((k, i, j))
                if i < j and self.G.has_edge(i, j):
                    if k in self.close_triangle_dict:
                        self.close_triangle_dict[k].append((i, j))
                    else:
                        self.close_triangle_dict[k] = []
                        self.close_triangle_dict[k].append((i, j))


    # helper methods

    def _init_all_data(self):
        # class variables
        # 3-nodes triangles
        self.open_triangle_dict = {}
        self.close_triangle_dict = {}

        self.total_close_triangle = []
        self.total_open_triangle = []
        # 4-nodes
        self.four_path_dict = {}
        self.four_chordal_cycle_dict = {}
        self.four_tailed_triangle_dict = {}
        self.four_clique_dict = {}
        self.four_cycle_dict = {}
        self.three_star_dict = {}

        self.total_four_path = []
        self.total_three_star = []
        self.total_four_cycle = []
        self.total_four_tailed_triangle = []
        self.total_four_chordal_cycle = []
        self.total_four_clique = []

        # 5-nodes, totally 21 of them
        self.total_five_graphlet = []
        for _ in range(21):
            self.total_five_graphlet.append({})

        # 6-nodes, totally 112 of them
        total_six_graphlet = []
        for _ in range(112):
            total_six_graphlet.append({})

        # 7-nodes, totally 853 of them
        total_seven_graphlet = []
        for _ in range(853):
            total_seven_graphlet.append({})

    def _add_2_dict(self, dictionary, index, content):
        if index not in dictionary:
            dictionary[index] = [content]
        else:
            dictionary[index].append(content)

    # count five total nodes from four total node
    def _count_total_5_nodes(self):
        '''
        # derive from 3-star
        for node_pair in self.total_three_star:
            node, node1, node2, node3 = node_pair
            for i in self.G.neighbors(node):
                # No.1 5 node graphlet
                if (i != node1 and i != node2 and i != node3 and i > node3 and not self.G.has_edge(i, node1)
                   and not self.G.has_edge(i, node2)
                   and not self.G.has_edge(i, node3)):
                    # outside nodes from small to large
                    sorted_list = sorted((node1, node2, node3, i))
                    index = (node, sorted_list[0], sorted_list[1], sorted_list[2], sorted_list[3])
                    self.total_five_graphlet[0][index] = None
            for i in self.G.neighbors(node1):
                # No.2
                if (i != node and not self.G.has_edge(i, node) and not self.G.has_edge(i, node2)
                    and not self.G.has_edge(i, node3)):
                    index = (node, node2, node3, node1, i)
                    self.total_five_graphlet[1][index] = None
                    
            for i in self.G.neighbors(node2):
                # No.2
                if (i != node and not self.G.has_edge(i, node) and not self.G.has_edge(i, node1)
                    and not self.G.has_edge(i, node3)):
                    index = (node, node1, node3, node2, i)
                    self.total_five_graphlet[1][index] = None
                    
            for i in self.G.neighbors(node3):
                # No.2
                if (i != node and not self.G.has_edge(i, node) and not self.G.has_edge(i, node1)
                    and not self.G.has_edge(i, node2)):
                    index = (node, node1, node2, node3, i)
                    self.total_five_graphlet[1][index] = None

        # derive from 3 path
        for node_pair in self.total_four_path:
            node, node1, node2, node3 = node_pair
            for i in self.G.neighbors(node):
                pass
            for i in self.G.neighbors(node1):
                # No.3
                if (i != node and node1 < node2 and not self.G.has_edge(node, i) and not self.G.has_edge(i, node2)
                    and not self.G.has_edge(i, node3)):
                    self.total_five_graphlet[2][(node, node1, i, node2, node3)] = None
                # No.8
                if (i != node and self.G.has_edge(i, node1) and self.G.has_edge(i, node3)
                    and not self.G.has_edge(i, node) and not self.G.has_edge(i, node2)):
                    if i == sorted((i, node1, node, node3, node2))[0]:
                        self.total_five_graphlet[7][(i, node1, node, node3, node2)] = None

            for i in self.G.neighbors(node2):
                pass
            for i in self.G.neighbors(node3):
                # No.3
                if (i != node2 and node < node3 and not self.G.has_edge(node, i) and not self.G.has_edge(i, node2)
                    and not self.G.has_edge(i, node1)):
                    self.total_five_graphlet[2][(node2, node, node1, node3, i)] = None
                # No.8
                if (i != node2 and self.G.has_edge(i, node1) and self.G.has_edge(i, node3)
                    and not self.G.has_edge(i, node) and not self.G.has_edge(i, node2)):
                    if i == sorted((i, node1, node, node3, node2)):
                        self.total_five_graphlet[7][(i, node1, node, node3, node2)] = None

        # derive from 4-cycle
        for node_pair in self.total_four_cycle:
            node, node1, node2, node3 = node_pair
            for i in self.G.neighbors(node):
                # No.7
                if (i != node1 and i != node2 and not self.G.has_edge(i, node1) and not self.G.has_edge(i, node2) and
                    not self.G.has_edge(i, node3)):
                    self.total_five_graphlet[6][(i, node, node1, node2, node3)] = None
                # No.12
                if (i != node1 and i != node2 and self.G.has_edge(i, node1) and not self.G.has_edge(i, node2) and
                    not self.G.has_edge(i, node3)):
                    self.total_five_graphlet[11][(i, node, node1, node2, node3)] = None
                if (i != node1 and i != node2 and not self.G.has_edge(i, node1) and self.G.has_edge(i, node2) and
                    not self.G.has_edge(i, node3)):
                    self.total_five_graphlet[11][(i, node, node1, node2, node3)] = None
                # No.13
                if (i != node1 and i != node2 and not self.G.has_edge(i, node1) and not self.G.has_edge(i, node2) and
                    self.G.has_edge(node3, i)):
                    if i == sorted((node1, node2, i))[0]:
                        self.total_five_graphlet[12][(i, node, node1, node2, node3)] = None
                # No.18
                if (i != node1 and i != node2 and self.G.has_edge(i, node1) and self.G.has_edge(i, node2) and
                    G.has_edge(i, node3)):
                    self.total_five_graphlet[17][(i, node, node1, node2, node3)] = None

            for i in self.G.neighbors(node1):
                # No.7
                if (i != node and i != node3 and not self.G.has_edge(i, node) and not self.G.has_edge(i, node2) and
                        not self.G.has_edge(i, node3)):
                    self.total_five_graphlet[6][(i, node1, node, node3, node2)] = None
                # No.13
                if (i != node and i != node3 and not self.G.has_edge(i, node) and self.G.has_edge(i, node2)
                    and not self.G.has_edge(i, node3)):
                    if i == sorted((i, node, node3))[0]:
                        self.total_five_graphlet[12][(i, node1, node, node3, node2)] = None

            for i in  self.G.neighbors(node2):
                # No.7
                if (i != node and i != node3 and not self.G.has_edge(i, node) and not self.G.has_edge(i, node1) and
                        not self.G.has_edge(i, node3)):
                    self.total_five_graphlet[6][(i, node2, node, node3, node1)] = None

            for i in self.G.neighbors(node3):
                # No.7
                if (i != node1 and i != node2 and not self.G.has_edge(i, node1) and not self.G.has_edge(i, node2) and
                        not self.G.has_edge(i, node)):
                    self.total_five_graphlet[6][(i, node3, node1, node2, node)] = None
                # No.12
                if (i != node1 and i != node2 and self.G.has_edge(i, node1) and not self.G.has_edge(i, node2) and
                        not self.G.has_edge(i, node)):
                    self.total_five_graphlet[11][(i, node3, node1, node2, node)] = None
                if (i != node1 and i != node2 and not self.G.has_edge(i, node1) and self.G.has_edge(i, node2) and
                        not self.G.has_edge(i, node)):
                    self.total_five_graphlet[11][(i, node3, node1, node2, node)] = None

        # derive from chord triangle
        for node_pair in self.total_four_chordal_cycle:
            node, node1, node2, node3 = node_pair
            for i in self.G.neighbors(node):
                # No.10
                if (i != node1 and i != node2 and not self.G.has_edge(i, node1) and not self.G.has_edge(i, node2)
                    and not self.G.has_edge(node3, i)):
                    self.total_five_graphlet[9][(i, node, node1, node2, node3)] = None
                # No.16
                if (i != node1 and i != node2 and i < node3 and self.G.has_edge(i, node1) and not self.G.has_edge(i, node2) and
                    not self.G.has_edge(i, node3)):
                    self.total_five_graphlet[15][(i, node, node1, node2, node3)] = None
                if (i != node1 and i != node2 and i < node3 and  not self.G.has_edge(i, node1) and self.G.has_edge(i, node2) and
                    not self.G.has_edge(i, node3)):
                    self.total_five_graphlet[15][(i, node, node1, node2, node3)] = None
                # No.17
                if (i != node1 and i != node2 and not self.G.has_edge(i, node1) and not self.G.has_edge(i, node2) and
                    self.G.has_edge(node3, i)):
                    self.total_five_graphlet[16][(i, node, node1, node2, node3)] = None
                # No.20
                if (i != node1 and i != node2  and self.G.has_edge(i, node1) and self.G.has_edge(i, node2) and
                    G.has_edge(i, node3)):
                    if i == sorted((i, node1, node2))[0]:
                        self.total_five_graphlet[19][(i, node, node1, node2, node3)] = None
            for i in self.G.neighbors(node1):
                # No.11
                if (i != node and i != node3 and i != node2 and not self.G.has_edge(i, node) and not self.G.has_edge(i, node2) and
                        not self.G.has_edge(i, node3)):
                    self.total_five_graphlet[10][(i, node1, node, node3, node2)] = None
                # No.14
                if (i != node and i != node3 and i != node2 and not self.G.has_edge(i, node) and self.G.has_edge(i, node2)
                    and not self.G.has_edge(i, node3)):
                    if i == sorted((node, node3, i))[0]:
                        self.total_five_graphlet[13][(i, node, node1, node2, node3)] = None
            for i in self.G.neighbors(node2):
                # No.11
                if (i != node and i != node3 and i != node1 and not self.G.has_edge(i, node) and not self.G.has_edge(i, node1) and
                        not self.G.has_edge(i, node3)):
                    self.total_five_graphlet[10][(i, node2, node, node3, node1)] = None
            for i in self.G.neighbors(node3):
                # No.10
                if (i != node1 and i != node2 and not self.G.has_edge(i, node1) and not self.G.has_edge(i, node2) and
                        not self.G.has_edge(i, node)):
                    self.total_five_graphlet[9][(i, node3, node1, node2, node)] = None
                # No.16
                if (i != node1 and i != node2 and i < node and self.G.has_edge(i, node1) and not self.G.has_edge(i, node2) and
                        not self.G.has_edge(i, node)):
                    self.total_five_graphlet[15][(i, node3, node1, node2, node)] = None
                if (i != node1 and i != node2 and i < node and not self.G.has_edge(i, node1) and self.G.has_edge(i, node2) and
                        not self.G.has_edge(i, node)):
                    self.total_five_graphlet[15][(i, node3, node1, node2, node)] = None
                '''
        # derive from 4 clique:
        for node_pair in self.total_four_clique:
            node, node1, node2, node3 = node_pair
            for i in self.G.neighbors(node):
                '''
                # No.15, almost same as No.7
                if (i != node1 and i != node2 and i != node3 and not self.G.has_edge(i, node1) and not self.G.has_edge(i, node2) and
                        not self.G.has_edge(i, node3)):
                    self.total_five_graphlet[14][(i, node, node1, node2, node3)] = None
                # No.19, almost same as No.12
                if (i != node1 and i != node2 and i != node3 and self.G.has_edge(i, node1) and not self.G.has_edge(i, node2) and
                        not self.G.has_edge(i, node3)):
                    self.total_five_graphlet[18][(i, node, node1, node2, node3)] = None
                if (i != node1 and i != node2 and i != node3 and not self.G.has_edge(i, node1) and self.G.has_edge(i, node2) and
                        not self.G.has_edge(i, node3)):
                    self.total_five_graphlet[18][(i, node, node1, node2, node3)] = None
                    '''
                # No.21
                if (i != node1 and i != node2 and i != node3 and self.G.has_edge(i, node1) and self.G.has_edge(i, node2)
                    and self.G.has_edge(i, node3)):
                    if i == sorted((i, node, node1, node2, node3))[0]:
                        self.total_five_graphlet[20][(i, node, node1, node2, node3)] = None

            '''
            for i in self.G.neighbors(node1):
                # No.15, almost same as No.7
                if (i != node and i != node3 and i != node2 and not self.G.has_edge(i, node) and not self.G.has_edge(i, node2) and
                        not self.G.has_edge(i, node3)):
                    self.total_five_graphlet[14][(i, node1, node, node3, node2)] = None


            for i in self.G.neighbors(node2):
                # No.15, almost same as No.7
                if (i != node and i != node3 and i != node2 and not self.G.has_edge(i, node) and not self.G.has_edge(i, node1) and
                        not self.G.has_edge(i, node3)):
                    self.total_five_graphlet[14][(i, node2, node, node3, node1)] = None

            for i in self.G.neighbors(node3):
                # No.15, almost same as No.7
                if (i != node1 and i != node2 and i != node and not self.G.has_edge(i, node1) and not self.G.has_edge(i, node2) and
                        not self.G.has_edge(i, node)):
                    self.total_five_graphlet[14][(i, node3, node1, node2, node)] = None
                # No.19 almost same as No.12
                if (i != node1 and i != node2 and i != node and self.G.has_edge(i, node1) and not self.G.has_edge(i, node2) and
                        not self.G.has_edge(i, node)):
                    self.total_five_graphlet[18][(i, node3, node1, node2, node)] = None
                if (i != node1 and i != node2 and i != node and not self.G.has_edge(i, node1) and self.G.has_edge(i, node2) and
                        not self.G.has_edge(i, node)):
                    self.total_five_graphlet[18][(i, node3, node1, node2, node)] = None
                '''






        # derive from tailed triangle
        for node_pair in self.total_four_tailed_triangle:
            node, node1, node2, node3 = node_pair
            # No.4
            for i in self.G.neighbors(node):
                # No.6
                if (i != node1 and i != node2 and i < node3 and not self.G.has_edge(i, node1) and not self.G.has_edge(i, node2)
                    and not self.G.has_edge(i, node3)):
                    self.total_five_graphlet[5][(node1, node, i, node2, node3)] = None
            for i in self.G.neighbors(node1):
                # No.6
                if (i != node and i != node2 and i < node3 and not self.G.has_edge(i, node) and not self.G.has_edge(i, node2)
                    and not self.G.has_edge(i, node3)):
                    self.total_five_graphlet[5][(node, node1, i, node2, node3)] = None
            for i in self.G.neighbors(node2):
                # No.6
                if (i != node and i != node1 and i > node3 and not self.G.has_edge(i, node)
                    and not self.G.has_edge(i, node1) and not self.G.has_edge(i, node3)):
                    self.total_five_graphlet[3][(node, node1, node2, node3, i)] = None
                # No.9
                if (i != node and i != node1 and i > node3 and node3 > node and not self.G.has_edge(i, node)
                    and not self.G.has_edge(i, node1) and self.G.has_edge(i, node3)):
                    self.total_five_graphlet[8][(node, node1, node2, node3, i)] = None
            for i in self.G.neighbors(node3):
                # No.5
                if (i != node2 and not self.G.has_edge(node, i) and not self.G.has_edge(node1, i)
                    and not self.G.has_edge(node2, i)):
                    self.total_five_graphlet[4][(node, node1, node2, node3, i)] = None

    # this function only generate global counting
    def _count_4_nodes_global(self):
        # derive  from close triangles dict
        for node_pairs in self.total_close_triangle:
            (node, node1, node2) = node_pairs
            '''
            for i in self.G.neighbors(node1):
                # 4 tailed triangle
                if i != node2 and i != node and not self.G.has_edge(i, node2) and not self.G.has_edge(i, node):
                    self.total_four_tailed_triangle.append((node, node2, node1, i))
                # 4-chordal cycle
                if i != node and self.G.has_edge(i, node2) and not self.G.has_edge(i, node):
                    if node < i:
                        self.total_four_chordal_cycle.append((node, node1, node2, i))
            for i in self.G.neighbors(node2):
                # 4 tailed triangle
                if i != node1 and i != node and  not self.G.has_edge(i, node1) and not self.G.has_edge(i, node):
                    self.total_four_tailed_triangle.append((node, node1, node2, i))
                # 4 chordal cycle
                if i != node and i != node1 and self.G.has_edge(i, node) and not self.G.has_edge(i, node1):
                    if node1 < i:
                        self.total_four_chordal_cycle.append((node1, node, node2, i))
                        '''
            for i in self.G.neighbors(node):
                '''
                # 4 tailed triangle
                if i != node1 and i != node2 and not self.G.has_edge(i, node1) and not self.G.has_edge(i, node2):
                    self.total_four_tailed_triangle.append((node1, node2, node, i))
                    '''
                # 4 clique
                if self.G.has_edge(i, node1) and self.G.has_edge(i, node2):
                    if node < node1 < node2 < i:
                        self.total_four_clique.append((node, node1, node2, i))
                        '''
                # 4 chordal cycle
                if i != node1 and i != node2 and self.G.has_edge(i, node1) and not self.G.has_edge(i, node2):
                    if node2 < i:
                        self.total_four_chordal_cycle.append((node2, node, node1, i))
                        '''

        ''' 
        # derive from open triangles
        for node_pairs in self.total_open_triangle:
            (node, node1, node2) = node_pairs
            for i in self.G.neighbors(node1):
                # 4-path, small node first
                if not self.G.has_edge(node2, i) and not self.G.has_edge(node, i):
                    # eliminate duplication
                    if node < node1:
                        self.total_four_path.append((node, node2, node1, i))
                # 4-cycle, small node first
                if i != node and self.G.has_edge(node2, i) and not self.G.has_edge(node, i):
                    if node < i and node < node1 and node < node2:
                        self.total_four_cycle.append((node, node1, node2, i))

            for i in self.G.neighbors(node2):
                # 4-path, small node first
                if not self.G.has_edge(node1, i) and not self.G.has_edge(node, i):
                    # eliminate duplication
                    if node < node2:
                        self.total_four_path.append((node, node1, node2, i))
            for i in self.G.neighbors(node):
                # 3-star
                if node1 < node2 < i and not self.G.has_edge(node1, i) and not self.G.has_edge(node2, i):
                    # eliminate duplication: from small to big index
                    self.total_three_star.append((node, node1, node2, i))
        '''
    # this function must be after _count_trianlges function
    def _count_4_nodes(self):
        # derive  from close triangles dict
        for node in self.close_triangle_dict:
            for node_pairs in self.close_triangle_dict[node]:
                (node1, node2) = node_pairs
                for i in self.G.neighbors(node1):
                    # 4 tailed triangle
                    if i != node2 and not self.G.has_edge(i, node2) and not self.G.has_edge(i, node):
                        self._add_2_dict(self.four_tailed_triangle_dict, node, (node2, node1, i))
                        if node < node2:
                            self.total_four_tailed_triangle.append((node, node2, node1, i))
                    # 4-chordal cycle
                    if i != node and self.G.has_edge(i, node2) and not self.G.has_edge(i, node):
                        self._add_2_dict(self.four_chordal_cycle_dict, node, (node1, node2, i))
                        if node < i:
                            self.total_four_chordal_cycle.append((node, node1, node2, i))
                for i in self.G.neighbors(node2):
                    # 4 tailed triangle
                    if i != node1 and not self.G.has_edge(i, node1) and not self.G.has_edge(i, node):
                        self._add_2_dict(self.four_tailed_triangle_dict, node, (node1, node2, i))
                        if node < node1:
                            self.total_four_tailed_triangle.append((node, node1, node2, i))
                for i in self.G.neighbors(node):
                    # 4-clique
                    if self.G.has_edge(i, node1) and self.G.has_edge(i, node2):
                        if node1 < node2 < i:
                            self._add_2_dict(self.four_clique_dict, node, (node1, node2, i))
                        if node < node1 < node2 < i:
                            self.total_four_clique.append((node, node1, node2, i))

        # derive from open triangles
        for node in self.open_triangle_dict:
            for node_pairs in self.open_triangle_dict[node]:
                (node1, node2) = node_pairs
                for i in self.G.neighbors(node1):
                    # 4-path, small node first
                    if not self.G.has_edge(node2, i) and not self.G.has_edge(node, i):
                        self._add_2_dict(self.four_path_dict, node, (node2, node1, i))
                        # eliminate duplication
                        if node < node1:
                            self.total_four_path.append((node, node2, node1, i))
                    # 4-cycle, small node first
                    if i != node and self.G.has_edge(node2, i) and not self.G.has_edge(node, i):
                        self._add_2_dict(self.four_cycle_dict, node, (node1, node2, i))
                        if node < i and node < node1 and node < node2:
                            self.total_four_cycle.append((node, node1, node2, i))

                for i in self.G.neighbors(node2):
                    # 4-path, small node first
                    if not self.G.has_edge(node1, i) and not self.G.has_edge(node, i):
                        self._add_2_dict(self.four_path_dict, node, (node1, node2, i))
                        # eliminate duplication
                        if node < node2:
                            self.total_four_path.append((node, node1, node2, i))
                for i in self.G.neighbors(node):
                    # 3-star
                    if node1 < node2 < i and not self.G.has_edge(node1, i) and not self.G.has_edge(node2, i):
                        # eliminate duplication: from small to big index
                        self._add_2_dict(self.three_star_dict, node, (node1, node2, i))
                        self.total_three_star.append((node, node1, node2, i))

    def _count_triangles(self):
        num_node = nx.number_of_nodes(self.G)
        for k in range(num_node):
            for i in self.G.neighbors(k):
                for j in self.G.neighbors(k):
                    if i < j:
                        # There is a close triangle
                        if self.G.has_edge(i, j):
                            if k in self.close_triangle_dict:
                                self.close_triangle_dict[k].append((i, j))
                            else:
                                self.close_triangle_dict[k] = []
                                self.close_triangle_dict[k].append((i, j))

                            if k < i:
                                self.total_close_triangle.append((k, i, j))

                        # There is an open triangle
                        else:
                            if k in self.open_triangle_dict:
                                self.open_triangle_dict[k].append((i, j))
                            else:
                                self.open_triangle_dict[k] = []
                                self.open_triangle_dict[k].append((i, j))

                            self.total_open_triangle.append((k, i, j))

 # main function
if __name__ == "__main__":
    G = nx.Graph()
    '''
    G.add_edges_from(
        [(0, 3), (1, 3), (1, 4), (1, 7), (2, 3), (2, 4), (2, 5), (2, 7), (3, 4), (3, 5), (3, 6), (4, 5), (4, 6),
        (4, 7),(5, 6)])
    '''
    # G.add_edges_from([(0, 1), (0, 2), (0,3), (0,4), (3, 5), (5, 9), (5, 8), (5, 7), (5, 6)])
    '''
    size = 10
    for i in range(7):
        start = time.time()
        G = nx.fast_gnp_random_graph(size, 0.5, seed=0)
        graphlet = Graphlet(G)
        end = time.time()
        print("%d sized graph: %f" % (size, end - start))
        size = size * 2
    '''
    G = nx.fast_gnp_random_graph(100, 0.4, seed=0)
    #G = nx.barabasi_albert_graph(100,  3, seed=0)
    graphlet = Graphlet(G)
    graphlet.print_triangles()
    print("\n")
    graphlet.print_4_nodes()
    print("\n")
    print(len(graphlet.total_five_graphlet[20]))
    ''' 
    count = 1
    for d in graphlet.total_five_graphlet:
        print("%dth graphlet: %d" % (count, len(d)))
        print(d)
        count = count + 1
    graphlet.show_graph()
    '''


