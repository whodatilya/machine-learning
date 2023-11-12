import networkx as nx
import matplotlib.pyplot as plt
import random


# Создание случайного графа
def create_random_graph(num_nodes, density):
    G = nx.Graph()
    for i in range(num_nodes):
        G.add_node(i)

    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < density:
                weight = random.randint(1, 10)  # Случайные веса рёбер
                G.add_edge(i, j, weight=weight)

    return G


# Визуализация графа
def plot_graph(G, title, pos=None):
    if pos is None:
        pos = nx.spring_layout(G)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos, with_labels=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.title(title)
    plt.show()



# Поиск минимального остовного дерева
def find_minimum_spanning_tree_prim(G):
    # Создаем пустой граф для минимального остовного дерева
    T = nx.Graph()

    # Выбираем начальную вершину (можно выбрать любую)
    start_node = list(G.nodes())[0]

    # Множество вершин, включенных в минимальное остовное дерево
    included_nodes = {start_node}

    # Пока не включены все вершины
    while len(included_nodes) < len(G.nodes()):
        min_weight = float('inf')
        min_edge = None

        # Поиск ребра с наименьшим весом, один конец которого включен в минимальное остовное дерево,
        # а другой - нет
        for node in included_nodes:
            for neighbor in G.neighbors(node):
                if neighbor not in included_nodes:
                    weight = G[node][neighbor]['weight']
                    if weight < min_weight:
                        min_weight = weight
                        min_edge = (node, neighbor)

        # Добавляем найденное ребро в минимальное остовное дерево
        if min_edge is not None:
            u, v = min_edge
            T.add_edge(u, v, weight=min_weight)
            included_nodes.add(v)

    return T


# Разбиение на кластеры
def cluster_graph_single_linkage(G, num_clusters):
    # Создаем список кластеров, каждый из которых начинается с одной вершины
    clusters = [[node] for node in G.nodes()]

    # Создаем список связей (ребер) с их весами
    edge_weights = [(u, v, G[u][v]['weight']) for (u, v) in G.edges()]

    # Сортируем связи по возрастанию весов
    edge_weights.sort(key=lambda x: x[2])

    # Объединяем кластеры до тех пор, пока не получим заданное количество кластеров
    while len(clusters) > num_clusters:
        u, v, weight = edge_weights.pop(0)

        # Находим кластеры, которые содержат вершины u и v
        u_cluster = None
        v_cluster = None
        for cluster in clusters:
            if u in cluster:
                u_cluster = cluster
            if v in cluster:
                v_cluster = cluster

        # Если у и v находятся в разных кластерах, объединяем их
        if u_cluster != v_cluster:
            u_cluster.extend(v_cluster)
            clusters.remove(v_cluster)

    # Преобразуем список кластеров в список списков вершин
    return clusters


if __name__ == "__main__":
    num_nodes = 5
    density = 1

    # Создаем случайный граф
    G = create_random_graph(num_nodes, density)

    # Выводим граф
    plot_graph(G, "Случайный граф")

    # Находим минимальное остовное дерево
    T = find_minimum_spanning_tree_prim(G)
    plot_graph(T, "Минимальное остовное дерево", pos=nx.spring_layout(G))

    # Разбиваем на кластеры
    num_clusters = 3
    clusters = cluster_graph_single_linkage(G, num_clusters)
    print("Кластеры:")
    for i, cluster in enumerate(clusters):
        print(f"Кластер {i + 1}: {cluster}")
