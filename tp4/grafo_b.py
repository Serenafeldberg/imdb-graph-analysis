from graph import Graph
from functions import *
import random

def load_graph_b(movies_by_id, actors_by_movie, actor_names_by_id) -> Graph:
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
        for actor in actors_by_movie[movie_id]:
            if not graph.vertex_exists(actor):
                graph.add_vertex(actor, actor_names_by_id.get(actor, "ERROR"))
            if not graph.vertex_exists(movie_id):
                graph.add_vertex(movie_id, movie_title)
            if not graph.edge_exists(actor, movie_id):
                graph.add_edge(actor, movie_id, {" "})

    return graph

def sep_rate (vertex2, min_paths):
    """
    Calculates the separation rate between two vertices
    :param vertex2: the second vertex
    :param min_paths: the minimum paths dictionary 
    :return: the separation rate
    """
    if vertex2 not in min_paths:
        return -1
    return int(min_paths[vertex2]/2)

def separation_rate (vertex1, vertex2, graph):
    """
    Calculates the separation rate between two vertices
    :param vertex1: the first vertex
    :param vertex2: the second vertex
    :param graph: the graph
    :return: the separation rate
    """
    if not graph.vertex_exists(vertex1) or not graph.vertex_exists(vertex2):
        return -1
    min_paths = bfs(graph, vertex1, vertex2)
    return sep_rate(vertex2, min_paths)

def choose_actor (actors_id, graph):
    """
    Chooses two actors from the graph, both in the same connected component
    :param actors_id: the actors ids
    :param graph: the graph
    :return: the two actors ids
    """
    actor = random.choice(actors_id)
    while not graph.vertex_exists(actor):
        actor = random.choice(actors_id)
    component = find_component(graph, actor)
    actor2 = random.choice(actors_id)
    while actor2 not in component:
        actor2 = random.choice(actors_id)
    return actor, actor2

def find_vertex (graph, vertex_name):
    """
    Finds a vertex by its id
    :param graph: the graph
    :param vertex_name: the vertex name
    :return: the vertex
    """
    for vertex in graph.get_vertices():
        if vertex_name == graph.get_vertex_data(vertex):
            return vertex
        
    return None

def sep_rate_kevin_bacon (graph):
    """
    Calculates the separation rate between Kevin Bacon and the actor with the highest separation rate
    :param graph: the graph
    :return: the actor name and the separation rate
    """
    kevin_bacon = find_vertex(graph, "Kevin Bacon")
    maximums = []
    if kevin_bacon is None:
        return -1, None
    connected_comp = find_component(graph, kevin_bacon)
    if connected_comp is None:
        return -1, None

    min_paths = bfs(graph, kevin_bacon)
    max_rate = -1
    max_name = None
    for vertex in connected_comp:
        if vertex != kevin_bacon and vertex[0] == 'n':
            rate = sep_rate(vertex, min_paths)
            if rate >= max_rate:
                if rate > max_rate:
                    maximums.clear()
                max_rate = rate
                max_name = graph.get_vertex_data(vertex)
                maximums.append(max_name)

    return max_rate, maximums

def update (visited, vertex):
    """
    Updates the visited dictionary
    :param visited: the visited dictionary
    :param vertex: the vertex
    """
    if vertex not in visited:
        visited[vertex] = 0
    visited[vertex] += 1

def random_walks (graph, walks, num_steps):
    """
    Does random walks in the graph
    :param graph: the graph
    :param walks: the number of walks
    :param num_steps: the number of steps of each walk
    :return: the visited actors and movies
    """
    visited_a = {}
    visited_m = {}
    for _ in range (walks):
        vertex = random.choice(list(graph.get_vertices()))

        for _ in range (num_steps):
            neighbors = graph.get_neighbors(vertex)
            if len(neighbors) == 0:
                break
            vertex = random.choice(list(neighbors))
            if vertex[0] == 'n':
                update(visited_a, vertex)
            else:
                update(visited_m, vertex)

    return visited_a, visited_m

def centrality (graph, walks, num_steps):
    """
    Calculates the centrality of the graph
    :param graph: the graph
    :param walks: the number of walks
    :param num_steps: the number of steps of each walk
    :return: the top 10 actors and movies
    """
    actors, movies = random_walks(graph, walks, num_steps)
    actors = put_names_dict(actors, graph)
    movies = put_names_dict(movies, graph)
    top10_a = sorted(actors.items(), key=lambda x: x[1], reverse=True)[:10]
    top10_m = sorted(movies.items(), key=lambda x: x[1], reverse=True)[:10]

    return top10_a, top10_m

  

if __name__ == '__main__':
    movies_by_id, actors_by_movie, actor_names_by_id = read_data(MOVIES_DATA_PATH, ACTORS_DATA_PATH, ACTORS_NAMES_PATH)
    graph = load_graph_b(movies_by_id, actors_by_movie, actor_names_by_id)

    """EJERCICIO 2"""
    actors_id = list(actor_names_by_id.keys())
    ac1, ac2 = choose_actor(actors_id, graph)
    sepa_rate = separation_rate(ac1, ac2, graph)

    if (sepa_rate == -1):
        print(f"There is no path between {actor_names_by_id[ac1]} and {actor_names_by_id[ac2]}")
    else:
        print(f"Separation rate between {actor_names_by_id[ac1]} and {actor_names_by_id[ac2]} is {sepa_rate}")


    """EJERCICIO 3"""
    max_rate, actors = sep_rate_kevin_bacon(graph)
    if max_rate == -1:
        print(f"There is no path between Kevin Bacon and other actors")
    else:
        print(f"Actor(s) with the highest separation rate ({max_rate}) from Kevin Bacon is {actors}")

    
    """EJERCICIO 8"""
    centrality_a, centrality_m = centrality(graph, 500, 50)
    print(f"Top 10 actors with the highest centrality:", centrality_a)
    print(f"Top 10 movies with the highest centrality:", centrality_m)


