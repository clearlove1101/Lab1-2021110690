import re
from matplotlib import pyplot as plt
import networkx as nx
import random
import numpy as np

wordsRegex = re.compile(r'\w+')
twoWordsRegex = re.compile(r'\w+[ ]\w+')
with open('text.txt', 'r') as f:
    text = f.read()

result = wordsRegex.findall(text.lower())


class Node:
    def __init__(self, value):
        self.id = None
        self.value = value
        self.next = []


class Connection:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2
        self.weight = 0


class DirectedGraph:
    def __init__(self):
        self.nodes = []
        self.valuelist = []
        self.connections = []
        self.num_nodes = 0

    def addNode(self, node):
        if node.value not in self.valuelist:
            node.id = self.num_nodes
            self.nodes.append(node)
            self.valuelist.append(node.value)
            self.num_nodes += 1

    def searchNodeByValue(self, value):
        for node in self.nodes:
            if node.value == value:
                return node

    def searchNodeById(self, id):
        for node in self.nodes:
            if node.id == id:
                return node

    def searchConnection(self, node1, node2):
        for connection in self.connections:
            if connection.node1 == node1 and connection.node2 == node2:
                return connection

    def addConnection(self, node1, node2):
        if DirectedGraph.searchConnection(self, node1, node2) is None:
            connection = Connection(node1, node2)
            node1.next.append(node2)
            connection.weight += 1
            self.connections.append(connection)
        else:
            DirectedGraph.searchConnection(self, node1, node2).weight += 1

    def showNodes(self):
        for node in self.nodes:
            print(f"{node.id}:{node.value}", end=', ')
        print('')

    def showConnections(self):
        # for node in self.nodes:
        #     if node.next:
        #         print(f'{node.value} -> ', end='')
        #         for next_word in node.next:
        #             print(next_word.value, end=', ')
        #     print('')
        for connection in self.connections:
            print(f'{connection.node1.value} -> {connection.node2.value}, weight: {connection.weight}')


# def generateDirectedGraph(textlist):
#     valuelist = []
#     for word in textlist:
#         if word not in valuelist:
#             valuelist.append(word)
#
#     G = DirectedGraph()
#     for value in valuelist:
#         node = Node(value)
#         G.addNode(node)
#
#     for i in range(len(textlist) - 1):
#         G.addConnection(G.searchNodeByValue(textlist[i]), G.searchNodeByValue(textlist[i + 1]))
#
#     # G.showNodes()
#     # G.showConnections()
#     return G


# def showDirectedGraph(G, node_path=None, edge_path=None):
#     if node_path == None or edge_path == None:
#         G2 = nx.DiGraph()
#         for connection in G.connections:
#             G2.add_edge(connection.node1.value, connection.node2.value, weight=connection.weight)
#
#         pos = nx.kamada_kawai_layout(G2)
#         nx.draw_networkx(G2, pos=pos, with_labels=True, alpha=0.5, font_size=8)
#         labels = nx.get_edge_attributes(G2, 'weight')
#         nx.draw_networkx_edge_labels(G2, pos, edge_labels=labels)
#         plt.savefig('graph.png')
#         plt.show()
#     else:
#         G3 = nx.DiGraph()
#
#         red_nodes = []
#         blue_nodes = []
#         for node in G.nodes:
#             if node.value in node_path:
#                 red_nodes.append(node.value)
#             else:
#                 blue_nodes.append(node.value)
#
#         for red_node in red_nodes:
#             G3.add_node(red_node, color='red', label=red_node)
#         for blue_node in blue_nodes:
#             G3.add_node(blue_node, color='blue', label=blue_node)
#
#         red_edges = []
#         blue_edges = []
#         for connection in G.connections:
#             if connection in edge_path:
#                 red_edges.append((connection.node1.value, connection.node2.value, connection.weight))
#             else:
#                 blue_edges.append((connection.node1.value, connection.node2.value, connection.weight))
#
#         G3.add_weighted_edges_from(red_edges, color='red')
#         G3.add_weighted_edges_from(blue_edges, color='blue')
#
#         pos = nx.kamada_kawai_layout(G3)
#
#         nx.draw_networkx_edges(G3, pos, red_edges, width=2.0, edge_color='red', alpha=0.5)
#         nx.draw_networkx_edges(G3, pos, blue_edges, width=1.0, edge_color='blue', alpha=0.5)
#
#         nx.draw_networkx_nodes(G3, pos, red_nodes, node_color='red', alpha=0.5)
#         nx.draw_networkx_nodes(G3, pos, blue_nodes, node_color='blue', alpha=0.5)
#
#         node_labels = nx.get_node_attributes(G3, 'label')
#         edge_labels = nx.get_edge_attributes(G3, 'weight')
#         nx.draw_networkx_labels(G3, pos, node_labels, font_size=8)
#         nx.draw_networkx_edge_labels(G3, pos, edge_labels=edge_labels)
#         plt.savefig('graph_with_shortest_path.png')
#         plt.show()


def queryBridgeWords(word1, word2):
    node1 = G.searchNodeByValue(word1)
    node2 = G.searchNodeByValue(word2)

    if node1 == None or node2 == None:
        if node1 == None and node2 == None:
            print(f"No '{word1}' and '{word2}' in the graph!")
        else:
            if node1 == None:
                print(f"No '{word1}' in the graph!")
            if node2 == None:
                print(f"No '{word2}' in the graph!")
        return 0

    bridge_words = []
    for node in G.nodes:
        if node in node1.next and node2 in node.next:
            bridge_words.append(node.value)

    if bridge_words == []:
        print(f"No bridge words from '{word1}' to '{word2}'!")
    else:
        print(f"The bridge words from '{word1}' to '{word2}' is : ", end='')
        for bridge_word in bridge_words:
            print(f"'{bridge_word}'", end='')
        print('')


def searchBridgeWords(word1, word2):
    node1 = G.searchNodeByValue(word1)
    node2 = G.searchNodeByValue(word2)

    bridge_words = []
    if node1 != None and node2 != None:
        for node in G.nodes:
            if node in node1.next and node2 in node.next:
                bridge_words.append(node.value)

    return bridge_words


# def generateNewText(inputText):
#     word_list = inputText.split(' ')
#
#     i = len(word_list) - 2
#     while i >= 0:
#         word1 = word_list[i]
#         word2 = word_list[i + 1]
#         if searchBridgeWords(word1, word2):
#             word_list.insert(i + 1, random.choice(searchBridgeWords(word1, word2)))
#         i -= 1
#
#     return word_list


def calcShortestPath(word1, word2):
    a = float('inf')
    num_nodes = G.num_nodes
    node1 = G.searchNodeByValue(word1)
    node2 = G.searchNodeByValue(word2)

    if node1 == None or node2 == None:
        if node1 == None and node2 == None:
            print(f"No '{word1}' and '{word2}' in the graph!")
        else:
            if node1 == None:
                print(f"No '{word1}' in the graph!")
            if node2 == None:
                print(f"No '{word2}' in the graph!")
        return 0

    if not node1.next:
        print(f"No path from '{word1}' to '{word2}'!")
        return 0

    # 初始化邻接矩阵、距离数组、前驱数组
    map = np.full((num_nodes, num_nodes), a)
    dist = np.full(num_nodes, a)
    dist[node1.id] = 0
    p = np.full(num_nodes, -1)

    # 向邻接矩阵、距离数组和前驱数组中输入有向图参数
    for connection in G.connections:
        map[connection.node1.id, connection.node2.id] = connection.weight
        if connection.node1.id == node1.id:
            dist[connection.node2.id] = connection.weight
            p[connection.node2.id] = connection.node1.id

    # 初始化集合
    S = {node1.id}
    V = {None}
    for node in G.nodes:
        V.add(node.id)
    V.remove(None)
    V_sub_S = V - S

    # 循环直到所有节点加入S集合
    while V_sub_S != set():
        min_index = 0
        min_edge = a
        V_sub_S_list = list(V_sub_S)
        for i in range(len(V_sub_S)):
            index = V_sub_S_list[i]
            if dist[index] < min_edge and dist[index] > 0:
                min_index = index
                min_edge = dist[index]

        # 更新S和V_sub_S集合
        S.add(min_index)
        V_sub_S = V - S

        # Dijkstra核心，判断新节点加入是否产生捷径
        for j in range(map.shape[1]):
            if map[min_index][j] < a:
                if dist[min_index] + map[min_index][j] <= dist[j]:
                    dist[j] = dist[min_index] + map[min_index][j]
                    p[j] = min_index

    path = [node2.id]
    path_index = node2.id
    while p[path_index] != -1:
        path.append(p[path_index])
        path_index = p[path_index]
    # path.append(node1.id)
    path.reverse()
    node_path = []
    for num in path:
        node_path.append(G.searchNodeById(num).value)

    edge_path = []
    for i in range(len(node_path) - 1):
        edge_path.append(G.searchConnection(G.searchNodeByValue(node_path[i]), G.searchNodeByValue(node_path[i + 1])))

    return node_path, edge_path


# def randomWalk():
#     G = generateDirectedGraph(result)
#     nodes = G.nodes
#     start_node = random.choice(nodes)
#     nodes_passed = [start_node]
#     edges_passed = []
#     values_list = [start_node.value]
#     if not start_node.next:
#         print(start_node.value)
#         return 0
#     next_node = random.choice(start_node.next)
#     i = 0
#
#     while True:
#         nodes_passed.append(next_node)
#         next_node_value = next_node.value
#         values_list.append(next_node_value)
#         if G.searchConnection(nodes_passed[i], nodes_passed[i + 1]) in edges_passed:
#             del (nodes_passed[i + 1])
#             break
#         else:
#             edges_passed.append(G.searchConnection(nodes_passed[i], nodes_passed[i + 1]))
#             if not next_node.next:
#                 break
#             else:
#                 next_node = random.choice(next_node.next)
#             i += 1
#
#     return nodes_passed


while 1:
    print('-' * 30 + '软件工程实验一结对编程部分' + '-' * 30)
    print('*' + ' ' * 20 + '1.生成有向图' + ' ' * 15 + '2.展示有向图' + ' ' * 20 + '*')
    print('*' + ' ' * 20 + '3.查询桥接词' + ' ' * 15 + '4.生成新文本' + ' ' * 20 + '*')
    print('*' + ' ' * 21 + '5.最短路径' + ' ' * 16 + '6.随机游走' + ' ' * 22 + '*')
    print('-' * 81)
    action = input('请输入您需使用的功能(输入q退出)：')
    G = generateDirectedGraph(result)
    if action == '1':
        print('DirectedGraph generated!')
    elif action == '2':
        showDirectedGraph(G)
    elif action == '3':
        content = twoWordsRegex.match(input("Please enter two words separated by space :"))
        while content == None:
            content = twoWordsRegex.match(input("Please enter two words separated by space :"))
        word1, word2 = content.group().split(' ')
        word1 = word1.strip()
        word2 = word2.strip()

        queryBridgeWords(word1, word2)
    elif action == '4':
        inputText = input("Please enter a few words :")
        for word in generateNewText(inputText):
            print(word, end=' ')
        print('')
    elif action == '5':
        content = twoWordsRegex.match(input("Please enter two words separated by space :"))
        while content == None:
            content = twoWordsRegex.match(input("Please enter two words separated by space :"))
        word1, word2 = content.group().split(' ')
        word1 = word1.strip()
        word2 = word2.strip()

        if calcShortestPath(word1, word2) != 0:
            node_path, edge_path = calcShortestPath(word1, word2)
            for node in node_path:
                print(node, end=' ')
            print('')

            showDirectedGraph(G, node_path, edge_path)

    elif action == '6':
        string = ''
        node_passed_list = randomWalk()
        if node_passed_list != 0:
            for node in node_passed_list:
                string += str(node.value + ' ')
                print(node.value, end=' ')
            print('')
        string.strip()

        with open('randomWalk.txt', 'w') as f:
            f.write(string)
        f.close()
    elif action == 'q':
        break
    else:
        print('请输入1-8使用该系统或输入q退出')
        continue
