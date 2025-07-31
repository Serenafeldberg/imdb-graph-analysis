import csv
import heapq
from heapdict import heapdict
from collections import deque

MOVIE_TITLE_TYPE = "movie"
MOVIE_COLUMNS = ["tconst", "titleType", "primaryTitle"]
PRINCIPALS_COLUMNS = ["nconst", "category"]
MOVIES_DATA_PATH = "./datasets/title-basics-f.tsv"
ACTORS_DATA_PATH = "./datasets/title-principals-f.tsv"
ACTORS_NAMES_PATH = "./datasets/name-basics-f.tsv"


def read_data(movies_file, actors_file, actors_name_file):
    print("Reading data")
    movies_by_id = {}
    with open(movies_file, "r", newline="", encoding="utf-8") as file1:
        reader = csv.DictReader(file1, delimiter="\t")
        for row in reader:
            if row["titleType"] == MOVIE_TITLE_TYPE:
                movies_by_id[row['tconst']] = row

    actors_ids = set()
    actors_by_movie = {m: set() for m in movies_by_id.keys()}
    with open(actors_file, "r", newline="", encoding="utf-8") as file2:
        reader = csv.DictReader(file2, delimiter="\t")
        for row in reader:
            if row["tconst"] in actors_by_movie:
                actors_by_movie[row["tconst"]].update([row["nconst"]])
                actors_ids.update([row["nconst"]])

    actor_names_by_id = {}
    with open(actors_name_file, "r", newline="", encoding="utf-8") as file2:
        reader = csv.DictReader(file2, delimiter="\t")
        for row in reader:
            if row["nconst"] in actors_ids:
                actor_names_by_id[row["nconst"]] = row["primaryName"]

    return movies_by_id, actors_by_movie, actor_names_by_id

def dfs (graph, start_vertx, end_vertx = None):
    """
    Depth First Search
    :param graph: the graph
    :param start_vertx: the starting vertex
    :return: the visited vertices
    """
    visited = set()
    stack = [start_vertx]
    while stack:
        v = stack.pop()
        if v == end_vertx:
            return visited
        for w in graph.get_neighbors(v):
            if w not in visited:
                visited.add(w)
                stack.append(w)

    return visited



def bfs (graph, start_vertex, end_vertex = None):
    """
    Breadth First Search
    :param graph: the graph
    :param start_vertex: the starting vertex
    :return: the distance from the starting vertex to the others
    """
    dist = {}
    visited = set()
    dist [start_vertex] = 0
    queue = deque([start_vertex])
    visited.add(start_vertex)
    while queue:
        v = queue.popleft()
        if v == end_vertex:
            return dist
        for w in graph.get_neighbors(v):
            if w not in visited:
                visited.add(w)
                dist[w] = dist[v] + 1
                queue.append(w)

    return dist

def connected (vertices, graph):
    """
    Finds the connected components
    :param vertices: the vertices
    :param graph: the graph
    :return: the connected components (dictionary) and the connected components list
    """
    visited = set()
    connected_comp = {}
    connected_comp_list = []
    cont = 1
    for vertex in vertices:
        if vertex not in visited:
            vis = dfs(graph, vertex)
            connected_comp_list.append(vis)
            for v in vis:
                connected_comp[v] = cont
            visited.update(vis)
            cont += 1
    return connected_comp, connected_comp_list

def weight (v, w, graph):
    """
    Calculates the weight of an edge
    :param v: the first vertex
    :param w: the second vertex
    :param graph: the graph
    :return: the weight of the edge
    """
    return len(graph.get_edge_data(v, w))

def find_component (graph, vertex):
    """
    Finds the connected component of a vertex
    :param graph: the graph
    :param vertex: the vertex
    :return: the component list
    """
    if not graph.vertex_exists(vertex):
        return None
    component = dfs(graph, vertex)
    return component

def dijkstra_heapdict(graph, start):
    component = find_component(graph, start)
    distances = {vertex: float('inf') for vertex in component}
    previous_vertices = {vertex: None for vertex in component}
    distances[start] = 0
    queue = heapdict({start: 0})

    while queue:
        current_vertex, current_distance = queue.popitem()

        if current_distance > distances[current_vertex]:
            continue

        neighbors = graph.get_neighbors(current_vertex)
        for neighbor in neighbors:
            weight = len(graph.get_edge_data(current_vertex, neighbor))
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_vertices[neighbor] = current_vertex
                queue[neighbor] = distance

    return distances, previous_vertices

def dijkstra (graph, vertex):
    """
    Dijkstra algorithm
    :param graph: the graph
    :param vertex: the starting vertex
    :return: the distance from the starting vertex to the others and the previous vertex
    """
    visited = set()
    dist = {}
    prev = {}
    dist[vertex] = 0
    prev[vertex] = None
    for v in find_component(graph, vertex):
        if (v == vertex):
            continue
        dist[v] = float('inf')
        prev[v] = None

    q = []
    heapq.heapify(q)
    heapq.heappush(q, [dist[vertex], vertex])
    while q:
        v = heapq.heappop(q)[1]
        if v in visited:
            continue
        for neigh in graph.get_neighbors(v):
            newdist = dist[v] + weight(v, neigh, graph)
            if newdist < dist[neigh]:
                dist[neigh] = newdist
                prev[neigh] = v
                heapq.heappush(q, [dist[neigh], neigh])
        visited.add(v)

    return dist, prev

def put_names (a_set, graph):
    """
    Puts the names of the actors in a list
    :param a_set: the set of actors by id
    :param graph: the graph
    :return: the list of actors
    """
    new_list = []
    a_set = list(a_set)
    for id in a_set:
        new_list.append(graph.get_vertex_data(id))
    return new_list

def put_names_dict (dict, graph):
    """
    Puts the names of the actors in a dictionary
    :param dict: the dictionary of actors by id
    :param graph: the graph
    :return: the list of actors
    """
    new_dict = {}
    for id, value in dict.items():
        new_dict[graph.get_vertex_data(id)] = value
    return new_dict

def put_names_prev (dict, graph):
    """
    Puts the names of the actors in a dictionary
    :param dict: the dictionary of actors by id
    :param graph: the graph
    :return: the dictionary of actors"""
    new_dict = {}
    for id, value in dict.items():
        new_dict[graph.get_vertex_data(id)] = graph.get_vertex_data(value)
    return new_dict