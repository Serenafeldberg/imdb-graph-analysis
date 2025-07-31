from graph import Graph
import csv
from itertools import combinations
from functions import *
import random
import time
from tqdm import tqdm


def load_graph(movies_by_id, actors_by_movie, actor_names_by_id) -> Graph:
    """
    Loads the graph
    :param movies_by_id: the movies data by id as dict
    :param actors_by_movie: the actors data by movie
    :param actor_names_by_id: the actors names by their ids
    :return: a Graph
    """
    graph = Graph()
    print("Loading graph")

    for movie_id in movies_by_id.keys():
        movie_title = movies_by_id[movie_id]['primaryTitle']
        for actor1, actor2 in combinations(actors_by_movie[movie_id], 2):
            if not graph.vertex_exists(actor1):
                graph.add_vertex(actor1, actor_names_by_id.get(actor1, "ERROR"))
            if not graph.vertex_exists(actor2):
                graph.add_vertex(actor2, actor_names_by_id.get(actor2, "ERROR"))
            existing_data = set()
            if graph.edge_exists(actor1, actor2):
                existing_data = graph.get_edge_data(actor1, actor2)
            graph.add_edge(vertex1=actor1, vertex2=actor2,
                           data={movie_title} | existing_data)
    return graph

def order_list (a_list):
    """
    Orders a list by length of its elements
    :param a_list: the list
    :return: the ordered list"""
    a_list.sort(key=lambda x: len(x), reverse=True)
    return a_list


def all_min_paths (graph):
    """
    Calculates the minimum paths from each vertex to each other vertex
    :param graph: the graph
    :return: the minimum paths
    """
    min_paths = {}
    for v in graph.get_vertices():
        min_path, prev = dijkstra(graph, v)
        min_paths[v] = (min_path, prev)

    return min_paths

def convert_seconds(seconds):
    """
    Converts seconds to days, hours, minutes and seconds
    :param seconds: the seconds
    :return: the converted seconds
    """
    days = int(seconds // 86400)
    remaining_seconds = seconds % 86400

    hours = int(remaining_seconds // 3600)

    remaining_seconds %= 3600

    minutes = int(remaining_seconds // 60)

    remaining_seconds %= 60

    result = "{:02d}:{:02d}:{:02d}:{:02d}".format(days, hours, minutes, int(remaining_seconds))
    return result

def all_min_paths_time (graph):
    """
    Calculates the time it takes to calculate the minimum paths from each vertex to each other vertex
    :param graph: the graph
    :return: the time it takes to calculate the minimum paths
    """
    times = []
    for i in range (5):
        sum_time = 0
        for i in tqdm(range (10)):
            vertex = random.choice(list(graph.get_vertices()))
            start = time.time()
            dijkstra(graph, vertex)
            end = time.time()
            sum_time += (end-start)

        sum_time /= 10
        sum_time *= len(graph.get_vertices())
        times.append(sum_time)
        break

    median_time = sorted(times)[len(times)//2]

    return convert_seconds(median_time)

def max_min_paths (biggest_component, graph):
    """
    Calculates the maximum minimum path by taking 11 random vertices
    :param min_paths: the minimum paths
    :return: the maximum minimum path (estimated)
    """
    values= []
    sum_time = 0
    max_key = random.choice(list(biggest_component))
    visited = set()
    for i in tqdm(range (11)):
        if max_key in visited:
            actor = random.choice(list(biggest_component))
        else:
            actor = max_key
        start_time = time.time()
        min_paths = bfs(graph, actor)
        end_time = time.time()
        max_value = 0
        max_key = 0
        for key, value in min_paths.items():
            if value > max_value:
                max_value = value
                max_key = key
        visited.add(actor)
        sum_time += (end_time - start_time)

        values.append(max_value)
    sum_time /= 11
    sum_time *= len(biggest_component)
    print("Tiempo promedio de ejecución para calcular el diametro: ", convert_seconds(sum_time))

    max_value = max(values)
    return max_value

def avg_separations (biggest_component, graph):
    """
    Calculates the average separations in the principal component by taking 10 random vertices
    :param biggest_component: the biggest component
    :param graph: the graph
    :return: the median average separations
    """
    separations = []
    sum_time = 0
    for i in tqdm(range (11)):
        vertex = random.choice (list(biggest_component))
        start_time = time.time()
        sep = bfs(graph, vertex)
        end_time = time.time()
        avg = 0
        for value in sep.values():
            avg += value
        avg /= len(sep)
        separations.append(avg)
        sum_time += (end_time - start_time)

    sum_time /= 11
    sum_time *= len(biggest_component)
    print("Tiempo promedio de ejecución para las distancias promedio: ", convert_seconds(sum_time))
    avg = sorted(separations)[len(separations)//2]

    return avg

def betweenness_centrality (graph, top=10, iter = 20):
    """
    Calculates the betweenness centrality of each vertex
    :param graph: the graph
    :return: the betweenness centrality of each vertex
    """
    betweenness = {}
    visited = set()
    
    for _ in range (iter):
        vertex = random.choice(list(graph.get_vertices()))
        while vertex in visited:
            vertex = random.choice(list(graph.get_vertices()))
        visited.add(vertex)
        min_paths = bfs(graph, vertex)
        for key in min_paths.keys():
            if key != vertex:
                if key not in betweenness.keys():
                    betweenness[key] = 0
                betweenness[key] += 1

    betweenness = {key: value/iter for key, value in betweenness.items()}
    betweenness = put_names_dict(betweenness, graph)
    betweenness = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:top]
    return betweenness

if __name__ == "__main__":
    # Define the paths to the datasets

    movies_by_id, actors_by_movie, actor_names_by_id = read_data(MOVIES_DATA_PATH, ACTORS_DATA_PATH, ACTORS_NAMES_PATH)
    graph = load_graph(movies_by_id, actors_by_movie, actor_names_by_id)
    #graph.print_graph()

    """EJERCICIO 1"""
    connected_components, connected_components_list = connected (graph.get_vertices(), graph)
    cant = max(connected_components.values())
    print("Cantidad de componentes conexas: ", cant)

    connected_components_list = order_list(connected_components_list)
    second_biggest = put_names(connected_components_list[1], graph)
    print(f"Segunda componente conexa mas grande ({len(connected_components_list[1])} componentes): ", second_biggest)

    smallest = put_names(connected_components_list[-1], graph)
    print(f"Componente conexa mas chica ({len(connected_components_list[-1])} componentes): ", smallest)

    """EJERCICIO 4"""
    actor = random.choice(list(graph.get_vertices()))
    min_paths , prev = dijkstra(graph, actor)
    print(f"Caminos minimos desde {graph.get_vertex_data(actor)}", put_names_dict (min_paths, graph))
    print("Actores previos", put_names_prev(prev, graph))
    
    """EJERCICIO 5"""
    # Si se quisiera calcular se debe llamar a la funcion all_min_paths(graph)
    time_dijkstra = all_min_paths_time(graph)
    print("Tiempo de ejecucion de Dijkstra para todos los vertices: ", time_dijkstra)

    """EJERCICIO 6"""
    max_min_path = max_min_paths(connected_components_list[0], graph)
    print("Camino minimo mas largo de la componente conexa principal: ", max_min_path)

    """EJERCICIO 7"""
    separations = avg_separations(connected_components_list[0], graph)
    print("Separacion promedio de la componente conexa principal: ", separations)

    """EJERCICIO 9"""
    betweenness = betweenness_centrality(graph)
    print("Betweenness centrality: ", betweenness)
