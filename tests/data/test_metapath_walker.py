# -*- coding: utf-8 -*-
#
# Copyright 2017-2018 Data61, CSIRO
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
import networkx as nx
from stellar.data.explorer import MetaPathWalk


def create_test_graph():
    """
    Creates a simple graph for testing the BreadthFirstWalk class. The node ids are string or integers. Each node
    also has a label based on the type of its id such that nodes with string ids and those with integer ids have
    labels 's' and 'n' resepctively.

    Returns:
        A simple graph with 13 nodes and 24 edges (including self loops for all but two of the nodes) in
        networkx format.

    """
    g = nx.Graph()
    edges = [
        ("0", 1),
        ("0", 2),
        (1, 3),
        (1, 4),
        (3, 6),
        (4, 7),
        (4, 8),
        (2, 5),
        (5, 9),
        (5, 10),
        ("0", "0"),
        (1, 1),
        (3, 3),
        (6, 6),
        (4, 4),
        (7, 7),
        (8, 8),
        (2, 2),
        (5, 5),
        (9, 9),
        (
            "self loner",
            "self loner",
        ),  # node that is not connected with any other nodes but has self loop
    ]

    g.add_edges_from(edges)
    g.add_node(
        "loner"
    )  # node that is not connected to any other nodes and not having a self loop

    for node in g.nodes():
        if type(node) == str:  # make these type s for string
            g.node[node]['label'] = 's'
        else:  # make these type n for number
            g.node[node]['label'] = 'n'

    return g


class TestMetaPathWalk(object):

    def test_parameter_checking(self):
        g = create_test_graph()
        mrw = MetaPathWalk(g)

        nodes = [1]
        n = 1
        length = 2
        seed = None
        metapaths = [['n', 's', 'n']]

        with pytest.raises(ValueError):
            # nodes should be a list of node ids even for a single node
            mrw.run(nodes=None, n=n, length=length, metapaths=metapaths, seed=seed)
            mrw.run(nodes=0, n=n, length=length, metapaths=metapaths, seed=seed)
            # only list is acceptable type for nodes
            mrw.run(nodes=(1,2,), n=n, length=length, metapaths=metapaths, seed=seed)
            # n has to be positive integer
            mrw.run(nodes=nodes, n=-1, length=length, metapaths=metapaths, seed=seed)
            mrw.run(nodes=nodes, n=11.4, length=length, metapaths=metapaths, seed=seed)
            mrw.run(nodes=nodes, n=0, length=length, metapaths=metapaths, seed=seed)
            # length has to be positive integer
            mrw.run(nodes=nodes, n=n, length=-3, metapaths=metapaths, seed=seed)
            mrw.run(nodes=nodes, n=n, length=0, metapaths=metapaths, seed=seed)
            mrw.run(nodes=nodes, n=n, length=4.6, metapaths=metapaths, seed=seed)
            mrw.run(nodes=nodes, n=n, length=1.0000001, metapaths=metapaths, seed=seed)
            # metapaths has to be a list of lists of strings denoting the node labels
            mrw.run(nodes=nodes, n=n, length=length, metapaths=['n', 's'], seed=seed)
            mrw.run(nodes=nodes, n=n, length=length, metapaths=[[1, 2]], seed=seed)
            mrw.run(nodes=nodes, n=n, length=length, metapaths=[['n', 's'], []], seed=seed)
            mrw.run(nodes=nodes, n=n, length=length, metapaths=[['n', 's'], ['s', 1]], seed=seed)
            mrw.run(nodes=nodes, n=n, length=length, metapaths=[('n', 's',)], seed=seed)
            mrw.run(nodes=nodes, n=n, length=length, metapaths=(['n', 's'], ['s', 'n', 's'],), seed=seed)
            # seed has to be integer or None
            mrw.run(nodes=nodes, n=n, length=length, metapaths=metapaths, seed=-1)
            mrw.run(nodes=nodes, n=n, length=length, metapaths=metapaths, seed=1000.345)

        # If no root nodes are given, an empty list is returned which is not an error but I thought this method
        # is the best for checking this behaviour.
        walks = mrw.run(nodes=[], n=n, length=length, metapaths=metapaths, seed=seed)
        assert len(walks) == 0

    def test_walk_generation_single_root_node_loner(self):
        g = create_test_graph()
        mrw = MetaPathWalk(g)

        seed = None
        nodes = ["loner"]  # has no edges, not even to itself
        n = 1
        length = 5
        metapaths = [['s', 'n', 's',]]

        walks = mrw.run(nodes=nodes, n=n, length=length, metapaths=metapaths, seed=seed)
        assert len(walks) == n
        assert len(walks[0]) == 1

        n = 5
        walks = mrw.run(nodes=nodes, n=n, length=length, metapaths=metapaths, seed=seed)
        assert len(walks) == n
        for walk in walks:
            assert len(walk) == 1

    def test_walk_generation_single_root_node_self_loner(self):
        g = create_test_graph()
        mrw = MetaPathWalk(g)

        seed = None
        nodes = ["self loner"]  # this node has self edges but not other edges
        n = 1
        length = 10
        metapaths = [['s', 'n', 'n', 's', ]]

        walks = mrw.run(nodes=nodes, n=n, length=length, metapaths=metapaths, seed=seed)
        assert len(walks) == n
        assert len(walks[0]) == 1  # for the ['s', 'n', 'n', 's'] metapath only the starting node is returned

        metapaths = [['s', 's', ]]
        walks = mrw.run(nodes=nodes, n=n, length=length, metapaths=metapaths, seed=seed)
        assert len(walks) == n
        assert len(walks[0]) == length  # the node is repeated length times
        for node in walks[0]:
            assert node == 'self loner'

    def test_walk_generation_single_root_node(self):

        g = create_test_graph()
        mrw = MetaPathWalk(g)

        nodes = ["0"]
        n = 1
        n_size = [0]


    def test_walk_generation_many_root_nodes(self):

        g = create_test_graph()
        mrw = MetaPathWalk(g)

        nodes = ["0", 2]
        n = 1
        n_size = [0]


    def test_walk_generation_number_of_walks_per_root_nodes(self):

        g = create_test_graph()
        mrw = MetaPathWalk(g)

        nodes = [1]
        n = 2
        n_size = [0]
