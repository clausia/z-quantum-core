import networkx as nx
import json
from itertools import combinations
import random
from random import uniform, normalvariate, choice
from .utils import SCHEMA_VERSION
from typing import TextIO, Optional, Union
import ast
from zquantum.core.typing import LoadSource, AnyPath


def save_graph(graph: nx.Graph, filename: AnyPath):
    """Saves a NetworkX graph object to JSON file.

    Args:
        graph (networks.Graph): the input graph object
        filename (string): name of the output file
    """
    f = open(filename, "w")
    graph_dict = nx.readwrite.json_graph.node_link_data(graph)
    graph_dict["schema"] = SCHEMA_VERSION + "-graph"
    json.dump(graph_dict, f, indent=2)
    f.close()


def load_graph(file: LoadSource) -> nx.Graph:
    """Reads a JSON file for extracting the NetworkX graph object.

    Args:
        file (str or file-like object): the file to load

    Returns:
        networkx.Graph: the graph
    """

    if isinstance(file, str):
        with open(file, "r") as f:
            data = json.load(f)
    else:
        data = json.load(file)

    return nx.readwrite.json_graph.node_link_graph(data)


def compare_graphs(graph1: nx.Graph, graph2: nx.Graph) -> bool:
    """Compares two NetworkX graph objects to see if they are identical.
    NOTE: this is *not* solving isomorphism problem.
    """

    for n1, n2 in zip(graph1.nodes, graph2.nodes):
        if n1 != n2:
            return False
    for e1, e2 in zip(graph1.edges, graph2.edges):
        if e1 != e2:
            return False
    return True


def generate_graph_node_dict(graph: nx.Graph) -> dict:
    """Generates a dictionary containing key:value pairs in the form of
                    nx.Graph node : integer index of the node

    Args:
        graph: nx.Graph object

    Returns:
        A dictionary as described
    """
    nodes_int_map = []
    for node_index, node in enumerate(graph.nodes):
        nodes_int_map.append((node, node_index))
    nodes_dict = dict(nodes_int_map)
    return nodes_dict


def generate_random_graph_erdos_renyi(
    num_nodes: int,
    probability: float,
    random_weights: Union[bool, str] = False,
    seed: Optional[int] = None,
) -> nx.Graph:
    """Randomly generate a graph from Erdos-Renyi ensemble.
    A graph is constructed by connecting nodes randomly.
    Each edge is included in the graph with probability p independent from
    every other edge. Equivalently, all graphs with n nodes and M edges have
    equal probability.

    Args:
        num_nodes: integer
            Number of nodes.
        probability: float
            Probability of two nodes connecting.
        random_weights: bool or str
            Flag indicating whether the weights should be random or constant.
            By default False, i.e. all the edge weights are set to 1.
            More details on how to specify random distributions in weight_graph_edges()

    
    Returns:
        A networkx.Graph object
    """
    output_graph = nx.erdos_renyi_graph(n=num_nodes, p=probability, seed=seed)
    output_graph = weight_graph_edges(output_graph, random_weights, seed)

    return output_graph


def generate_random_regular_graph(
    num_nodes: int,
    degree: int,
    random_weights: Union[bool, str] = False,
    seed: Optional[int] = None,
) -> nx.Graph:
    """Randomly generate a d-regular graph.
    A graph is generated by picking uniformly a graph among the set of graphs
    with the desired number of nodes and degre.
    Args:
        num_nodes: integer
            Number of nodes.
        degre: int
            Degre of each edge.
        random_weights: bool or str
            Flag indicating whether the weights should be random or constant.
            By default False, i.e. all the edge weights are set to 1.
            More details on how to specify random distributions in weight_graph_edges()
    
    Returns:
        A networkx.Graph object
    """
    output_graph = nx.random_regular_graph(d=degree, n=num_nodes, seed=seed)
    output_graph = weight_graph_edges(output_graph, random_weights, seed)

    return output_graph


def generate_caveman_graph(
    number_of_cliques: int,
    size_of_cliques: int,
    random_weights: bool = False,
    seed: Optional[int] = None,
) -> nx.Graph:
    output_graph = nx.caveman_graph(number_of_cliques, size_of_cliques)
    output_graph = weight_graph_edges(output_graph, random_weights, seed)
    return output_graph


def generate_ladder_graph(
    length_of_ladder: int, random_weights: bool = False, seed: Optional[int] = None
) -> nx.Graph:
    output_graph = nx.ladder_graph(length_of_ladder)
    output_graph = weight_graph_edges(output_graph, random_weights, seed)
    return output_graph


def generate_barbell_graph(
    number_of_vertices_complete_graph: int,
    random_weights: bool = False,
    seed: Optional[int] = None,
) -> nx.Graph:
    output_graph = nx.barbell_graph(number_of_vertices_complete_graph, 0)
    output_graph = weight_graph_edges(output_graph, random_weights, seed)
    return output_graph


def weight_graph_edges(
    graph: nx.Graph,
    random_weights: Union[bool, str] = False,
    seed: Optional[int] = None,
) -> nx.Graph:
    """Update the weights of all the edges of a graph.

    Args:
        graph: nx.Graph
            The input graph.
        random_weights: bool or str
            Flag indicating whether the weights should be random or constant.
            if False (default) static weights, i.e. equal to 1.0
            if True weights are drawn from uniform(0,1)
            if a string it will be used when generating random values for the weights
    
    Returns:
        A networkx.Graph object
    """
    assert not (graph.is_multigraph()), "Cannot deal with multigraphs"
    if seed is not None:
        random.seed(seed)
    if random_weights == True:
        weighted_edges = [(e[0], e[1], uniform(0, 1)) for e in graph.edges]
    elif random_weights == False:
        weighted_edges = [(e[0], e[1], 1.0) for e in graph.edges]
    else:
        weighted_edges = [
            (e[0], e[1], generate_random_value_from_string(random_weights))
            for e in graph.edges
        ]

    # If edges already present, it will effectively update them (except for multigraph)
    graph.add_weighted_edges_from(weighted_edges)
    return graph


def generate_graph_from_specs(graph_specs: dict) -> nx.Graph:
    """Generate a graph from a specs dictionary

    Args:
        graph_specs: dictionnary
            Specifications of the graph to generate. It should contain at 
            least an entry with key 'type' and one with num_nodes.
            Note that some of the entries are processed using generate_random_value_from_string()
            i.e. they could contain a value (int or float) which will be untouched
            or a string specifying how the value should be randomly generated
    
    Returns:
        A networkx.Graph object
    """
    type_graph = graph_specs["type_graph"]
    num_nodes = graph_specs["num_nodes"]
    random_weights = graph_specs.get("random_weights", False)
    seed = graph_specs.get("seed", None)
    number_of_cliques = graph_specs.get("number_of_cliques", None)
    size_of_cliques = graph_specs.get("size_of_cliques", None)
    length_of_ladder = graph_specs.get("length_of_ladder", None)
    number_of_vertices_complete_graph = graph_specs.get(
        "number_of_vertices_complete_graph", None
    )

    if type_graph == "erdos_renyi":
        probability = generate_random_value_from_string(graph_specs["probability"])
        graph = generate_random_graph_erdos_renyi(
            num_nodes, probability, random_weights, seed
        )

    elif type_graph == "regular":
        degree = generate_random_value_from_string(graph_specs["degree"])
        graph = generate_random_regular_graph(num_nodes, degree, random_weights, seed)

    elif type_graph == "complete":
        graph = generate_random_graph_erdos_renyi(num_nodes, 1.0, random_weights, seed)

    elif type_graph == "caveman":
        graph = generate_caveman_graph(
            number_of_cliques, size_of_cliques, random_weights, seed
        )

    elif type_graph == "ladder":
        graph = generate_ladder_graph(length_of_ladder, random_weights, seed)

    elif type_graph == "barbell":
        graph = generate_barbell_graph(
            number_of_vertices_complete_graph, random_weights, seed
        )
    else:
        raise (NotImplementedError("This type of graph is not supported: ", type_graph))

    return graph


def generate_random_value_from_string(
    specs: Union[str, int, float]
) -> Union[int, float]:
    """ Generate values (int or float) from a string specifying how the value
    should be generated. If an int or float is passed as an input they will be 
    returned as an output.

    Args:
        random_string: string
            Specifications of the random value to generate. 
            of the form: type-randomness_arg0_arg1_.._argN                
            
    Returns:
        A int or float value (the type will depend on the specs, 
        E.g. generate_random_value_from_string('choice_5_6_7') will return an int 
        while generate_random_value_from_string('choice_5._6._7.')  will return
        a float)
    """
    if type(specs) in [int, float]:
        return specs
    else:
        assert type(specs) is str
        specs_split = specs.split("_")
        type_random = specs_split[0]

        if type_random == "uniform":
            min_val = ast.literal_eval(specs_split[1])
            max_val = ast.literal_eval(specs_split[2])
            value = uniform(min_val, max_val)

        elif type_random == "uniformrange":
            range_choice = range(
                *[ast.literal_eval(split) for split in specs_split[1:]]
            )
            value = choice(range_choice)

        elif type_random == "choice":
            choices = [ast.literal_eval(split) for split in specs_split[1:]]
            value = choice(choices)

        elif type_random == "normal":
            mu = ast.literal_eval(specs_split[1])
            sigma = ast.literal_eval(specs_split[2])
            value = normalvariate(mu, sigma)

        elif type_random == "constant":
            value = ast.literal_eval(specs_split[1])

        return value
