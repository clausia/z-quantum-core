import os
import unittest
import random

import networkx as nx
from zquantum.core.graph import (
    compare_graphs,
    generate_barbell_graph,
    generate_caveman_graph,
    generate_graph_from_specs,
    generate_graph_node_dict,
    generate_ladder_graph,
    generate_random_graph_erdos_renyi,
    generate_random_regular_graph,
    generate_graph_from_specs,
    _generate_random_value_from_string,
    load_graph,
    save_graph,
)


class TestGraph(unittest.TestCase):
    def test_compare_graphs(self):
        # Given
        G1 = nx.Graph()
        G2 = nx.Graph()
        G3 = nx.Graph()

        G1.add_edges_from([(1, 2), (2, 3), (1, 3)])
        G2.add_edges_from([(1, 2), (2, 3), (1, 3)])
        G3.add_edges_from([(1, 2), (2, 3)])

        # When/Then
        self.assertTrue(compare_graphs(G1, G2))
        self.assertFalse(compare_graphs(G2, G3))

    def test_graph_io(self):
        # Given
        G = nx.Graph()
        G.add_edges_from([(1, 2), (2, 3), (1, 3)])

        # When
        save_graph(G, "Graph.json")
        G2 = load_graph("Graph.json")

        # Then
        self.assertTrue(compare_graphs(G, G2))

        os.remove("Graph.json")

    def test_generate_graph_node_dict(self):
        # Given
        G = nx.Graph()
        G.add_edges_from([(1, 2), (2, 3), (1, 3)])
        target_node_dict = {1: 0, 2: 1, 3: 2}

        # When
        node_dict = generate_graph_node_dict(G)

        # Then
        self.assertDictEqual(node_dict, target_node_dict)

    def test_generate_random_graph_erdos_renyi(self):
        # Given
        num_nodes = 3
        probability = 1
        target_graph = nx.Graph()
        target_graph.add_edges_from([(0, 1), (1, 2), (0, 2)])

        # When
        graph = generate_random_graph_erdos_renyi(num_nodes, probability)

        # Then
        self.assertTrue(compare_graphs(graph, target_graph))

        # Given
        num_nodes = 3
        probability = 0
        target_graph = nx.Graph()

        # When
        graph = generate_random_graph_erdos_renyi(num_nodes, probability)

        # Then
        self.assertTrue(compare_graphs(graph, target_graph))

        # Given
        num_nodes = 20
        probability = 0.8
        weights = "uniform"

        # When
        graph = generate_random_graph_erdos_renyi(num_nodes, probability, weights)

    def test_generate_random_regular_graph(self):
        # Given
        num_nodes = 4
        degree = 2

        # When
        graph = generate_random_regular_graph(num_nodes, degree)

        # Then
        for n in graph.nodes():
            node_in_edge = [n in e for e in graph.edges()]
            self.assertTrue(sum(node_in_edge) == degree)

        # Given
        num_nodes = 20
        degree = 3
        weights = "uniform"

        # When
        graph = generate_random_regular_graph(num_nodes, degree, weights)

        # Then
        for edge in graph.edges:
            self.assertIn("weight", graph.edges[edge].keys())

        self.assertEqual(len(graph.nodes), num_nodes)

    def test_generate_caveman_graph(self):
        # Given
        number_of_cliques = 3
        size_of_cliques = 4
        weights = "uniform"

        # When
        graph = generate_caveman_graph(number_of_cliques, size_of_cliques, weights)

        # Then
        for edge in graph.edges:
            self.assertIn("weight", graph.edges[edge].keys())

        self.assertEqual(len(graph.nodes), number_of_cliques * 4)

    def test_generate_ladder_graph(self):
        # Given
        length_of_ladder = 4
        weights = "uniform"

        # When
        graph = generate_ladder_graph(length_of_ladder, weights)

        # Then
        for edge in graph.edges:
            self.assertIn("weight", graph.edges[edge].keys())

        self.assertEqual(len(graph.nodes), length_of_ladder * 2)

    def test_generate_barbell_graph(self):
        # Given
        number_of_vertices_complete_graph = 4
        weights = "uniform"

        # When
        graph = generate_barbell_graph(number_of_vertices_complete_graph, weights)

        # Then
        for edge in graph.edges:
            self.assertIn("weight", graph.edges[edge].keys())

        self.assertEqual(len(graph.nodes), number_of_vertices_complete_graph * 2)

    def test_seed(self):
        # Given
        num_nodes = 4
        degree = 2
        seed = 123

        target_graph = generate_random_regular_graph(
            num_nodes, degree, weights="uniform", seed=seed
        )

        # When
        graph = generate_random_regular_graph(
            num_nodes, degree, weights="uniform", seed=seed
        )

        # Then
        self.assertTrue(compare_graphs(graph, target_graph))

    def test_generate_graph_from_specs(self):
        # Given
        specs = {"type_graph": "erdos_renyi", "num_nodes": 3, "probability": 1.0}
        target_graph = nx.Graph()
        target_graph.add_edges_from([(0, 1), (1, 2), (0, 2)])

        # When
        graph = generate_graph_from_specs(specs)

        # Then
        self.assertTrue(compare_graphs(graph, target_graph))

        # Given
        specs = {"type_graph": "regular", "num_nodes": 4, "degree": 2}

        # When
        graph = generate_graph_from_specs(specs)

        # Then
        for n in graph.nodes():
            node_in_edge = [n in e for e in graph.edges()]
            self.assertTrue(sum(node_in_edge) == 2)

        # Given
        specs = {"type_graph": "complete", "num_nodes": 4}
        target_graph = nx.Graph()
        target_graph.add_edges_from([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)])

        # When
        graph = generate_graph_from_specs(specs)

        # Then
        self.assertTrue(compare_graphs(graph, target_graph))

        # When
        specs = {"type_graph": "complete", "num_nodes": 10, "weights": "uniform"}

        # When
        graph = generate_graph_from_specs(specs)

        # Then
        for edge in graph.edges:
            self.assertIn("weight", graph.edges[edge].keys())

    def test_generate_random_value_from_string_uniform(self):
        # Given
        specs_float = "uniform_-5._5."

        # When
        value_float = _generate_random_value_from_string(specs_float)

        # Then
        self.assertTrue(type(value_float) is float)
        self.assertTrue((value_float > -5) and (value_float < 5))

    def test_generate_random_value_from_string_uniformrange(self):
        # Given
        specs_int = "uniformrange_5_10"

        # When
        value_int = _generate_random_value_from_string(specs_int)

        # Then
        self.assertTrue(type(value_int) is int)
        self.assertTrue(value_int in range(5, 10))

    def test_generate_random_value_from_string_choice(self):
        # Given
        specs_float = "choice_3._5._14."
        specs_int = "choice_3_5_14"

        # When
        value_float = _generate_random_value_from_string(specs_float)
        value_int = _generate_random_value_from_string(specs_int)

        # Then
        self.assertTrue(type(value_float) is float)
        self.assertTrue(type(value_int) is int)
        self.assertTrue(value_float in [3.0, 5.0, 14.0])
        self.assertTrue(value_int in [3, 5, 14])

    def test_generate_random_value_from_string_normal(self):
        # Given
        specs_float = "normal_-10._0.0001"
        random.seed(123)

        # When
        value_float = _generate_random_value_from_string(specs_float)

        # Then
        self.assertTrue(type(value_float) is float)
        self.assertTrue((value_float > -11.0) and (value_float < -9.0))

    def test_generate_random_value_from_string_constant(self):
        # Given
        specs_float = "constant_5."
        specs_int = "constant_5"

        # When
        value_float = _generate_random_value_from_string(specs_float)
        value_int = _generate_random_value_from_string(specs_int)

        # Then
        self.assertTrue(type(value_float) is float)
        self.assertTrue(type(value_int) is int)
        self.assertEqual(value_float, 5)
        self.assertTrue(value_int, 5)

    def test_generate_graph_from_specs_with_string_random(self):
        # Given
        specs = {"type_graph": "regular", "num_nodes": 8, "degree": "choice_3_4"}

        # When
        graph = generate_graph_from_specs(specs)

        # Then
        degrees = [deg for node, deg in graph.degree]
        degree_ref = degrees[0]
        self.assertTrue(degree_ref in [3, 4])
        for degree in degrees:
            self.assertEqual(degree, degree_ref)

        # Given
        specs = {
            "type_graph": "regular",
            "num_nodes": 8,
            "degree": 3,
            "weights": "uniform_-1_-0.5",
        }

        # When
        graph = generate_graph_from_specs(specs)

        # Then
        for node1, node2, weight in graph.edges(data="weight"):
            self.assertTrue((weight > -1) and (weight < -0.5))
