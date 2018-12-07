#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
'''
Assignment 3: Controlling Maximum Flow

Team Number: 
Student Names: 
'''

import unittest
import networkx as nx
# API for networkx flow algorithms changed in v1.9:
if (list(map(lambda x: int(x), nx.__version__.split("."))) < [1, 9]):
    max_flow = nx.ford_fulkerson
else:
    max_flow = nx.maximum_flow
"""
We use max_flow() to generate flows for the included tests,
and you may of course use it as well in any tests you generate.
As always, your implementation of the senstive() function may NOT make use
of max_flow(), or any of the other graph algorithm implementations
provided by networkx.
"""

# If your solution needs a queue (like the BFS algorithm), you can use this one:
from collections import deque

try:
    import matplotlib.pyplot as plt
    HAVE_PLT = True
except ImportError:
    HAVE_PLT = False

"""
F is represented in python as a dictionary of dictionaries;
i.e., given two nodes u and v,
the computed flow from u to v is given by F[u][v].
"""
def sensitive(G, s, t, F):
    """
    Sig:   graph G(V,E), int, int, int[0..|V|-1, 0..|V|-1] ==> int, int
    Pre:    
    Post:   
    Ex:    sensitive(G,0,5,F) ==> (1, 3)
    """
    return None, None


class SensitiveSanityCheck(unittest.TestCase):
    """
    Test suite for the sensitive edge problem
    """
    def draw_graph(self, H, u, v, flow1, F1, flow2, F2):
        if not HAVE_PLT:
            return
        pos = nx.spring_layout(self.G)
        plt.subplot(1,2,1)
        plt.axis('off')
        nx.draw_networkx_nodes(self.G,pos)
        nx.draw_networkx_edges(self.G,pos)
        nx.draw_networkx_labels(self.G,pos)
        nx.draw_networkx_edge_labels(
            self.G, pos,
            edge_labels={(u,v):'{}/{}'.format(
                  F1[u][v],
                  self.G[u][v]['capacity']
                ) for (u,v,data) in nx.to_edgelist(self.G)})
        plt.title('before: flow={}'.format(flow1))
        plt.subplot(1,2,2)
        plt.axis('off')
        nx.draw_networkx_nodes(self.G,pos)
        nx.draw_networkx_edges(self.G,pos)
        nx.draw_networkx_edges(
            self.G, pos,
            edgelist=[(u,v)],
            width=3.0,
            edge_color='b')
        nx.draw_networkx_labels(self.G,pos)
        nx.draw_networkx_edge_labels(
            self.G, pos,
            edge_labels={(u,v):'{}/{}'.format(
                  F2[u][v],H[u][v]['capacity']
                ) for (u,v,data) in nx.to_edgelist(self.G)})
        plt.title('after: flow={}'.format(flow2))

    def setUp(self):
        """start every test with an empty directed graph"""
        self.G = nx.DiGraph()

    def run_test(self, s, t, draw=False):
        """standard tests to run for all cases

        Uses networkx to generate a maximal flow
        """
        H = self.G.copy()
        # compute max flow
        flow_g, F_g = max_flow(self.G, s, t)
        # find a sensitive edge
        u,v = sensitive(self.G, s, t, F_g)
        # is u a node in G?
        self.assertIn(u, self.G, "Invalid edge ({}, {})".format(u ,v))
        # is (u,v) an edge in G?
        self.assertIn(v, self.G[u], "Invalid edge ({}, {})".format(u ,v))
        # decrease capacity of (u,v) by 1
        H[u][v]["capacity"] = H[u][v]["capacity"] - 1
        # recompute max flow
        flow_h, F_h = max_flow(H, s, t)
        if draw:
            self.draw_graph(H, u, v, flow_g, F_g, flow_h, F_h)
        # is the new max flow lower than the old max flow?
        self.assertLess(
            flow_h,
            flow_g,
            "Returned non-sensitive edge ({},{})".format(u,v))

    def test_sanity(self):
        """Sanity check"""
        # The attribute on each edge MUST be called "capacity"
        # (otherwise the max flow algorithm in run_test will fail).
        self.G.add_edge(0, 1, capacity = 16)
        self.G.add_edge(0, 2, capacity = 13)
        self.G.add_edge(2, 1, capacity = 4)
        self.G.add_edge(1, 3, capacity = 12)
        self.G.add_edge(3, 2, capacity = 9)
        self.G.add_edge(2, 4, capacity = 14)
        self.G.add_edge(4, 3, capacity = 7)
        self.G.add_edge(3, 5, capacity = 20)
        self.G.add_edge(4, 5, capacity = 4)
        self.run_test(0,5,draw=True)

    @classmethod
    def tearDownClass(cls):
        if HAVE_PLT:
            plt.show()

if __name__ == "__main__":
    unittest.main()
