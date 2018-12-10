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

    vertices = list(G)
    g_util = {}

    for i in range(len(vertices)):
        tmp = list(G.edges(vertices[i]))
        neighbours = []
        for k in range(len(tmp)):
            (node, neighbour) = tmp[k]
            neighbours.append(neighbour)
        edges = dict.fromkeys(neighbours)
        for j in range(len(tmp)):
            edges[neighbours[j]] = G[vertices[i]][neighbours[j]]["capacity"]
        g_util[vertices[i]] = edges

    print F
    print g_util

    for vert in F:
        print "looking at vert:", vert
        for inner_vert in F[vert]:
            print "looking at edge:", inner_vert
            print F[vert][inner_vert], g_util[vert][inner_vert]
            if F[vert][inner_vert] == g_util[vert][inner_vert]:
                return vert, inner_vert

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
        print "list:", list(self.G)
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

    def est_sanity(self):
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


    def est_shit_test(self): # Works when refactored
        self.G.add_edge(0, 2, capacity = 164)
        self.G.add_edge(0, 3, capacity = 209)
        self.G.add_edge(0, 4, capacity = 111)
        self.G.add_edge(0, 6, capacity = 55)
        self.G.add_edge(0, 7, capacity = 116)
        self.G.add_edge(1, 0, capacity = 124)
        self.G.add_edge(1, 3, capacity = 51)
        self.G.add_edge(1, 7, capacity = 144)
        self.G.add_edge(3, 2, capacity = 54)
        self.G.add_edge(3, 6, capacity = 77)
        self.G.add_edge(4, 1, capacity = 145)
        self.G.add_edge(4, 2, capacity = 165)
        self.G.add_edge(4, 3, capacity = 16)
        self.G.add_edge(4, 6, capacity = 131)
        self.G.add_edge(5, 1, capacity = 55)
        self.G.add_edge(5, 3, capacity = 95)
        self.G.add_edge(5, 4, capacity = 2)
        self.G.add_edge(5, 6, capacity = 108)
        self.G.add_edge(5, 7, capacity = 133)
        self.G.add_edge(6, 1, capacity = 135)
        self.G.add_edge(7, 3, capacity = 2)
        self.G.add_edge(7, 4, capacity = 165)
        self.G.add_edge(7, 6, capacity = 4)

        s = 5;
        t = 2;

        self.run_test(s,t,draw=True)

    def est_new_test(self): # Returns non sensitive edge
        self.G.add_edge(0, 1, capacity = 17)
        self.G.add_edge(0, 2, capacity = 111)
        self.G.add_edge(0, 4, capacity = 67)
        self.G.add_edge(0, 6, capacity = 224)
        self.G.add_edge(0, 7, capacity = 154)
        self.G.add_edge(1, 2, capacity = 320)
        self.G.add_edge(1, 3, capacity = 35)
        self.G.add_edge(1, 7, capacity = 223)
        self.G.add_edge(1, 8, capacity = 139)
        self.G.add_edge(2, 4, capacity = 18)
        self.G.add_edge(2, 6, capacity = 136)
        self.G.add_edge(2, 8, capacity = 237)
        self.G.add_edge(3, 0, capacity = 55)
        self.G.add_edge(3, 2, capacity = 87)
        self.G.add_edge(3, 7, capacity = 170)
        self.G.add_edge(4, 1, capacity = 132)
        self.G.add_edge(4, 3, capacity = 6)
        self.G.add_edge(5, 2, capacity = 117)
        self.G.add_edge(5, 3, capacity = 110)
        self.G.add_edge(5, 4, capacity = 289)
        self.G.add_edge(5, 6, capacity = 160)
        self.G.add_edge(5, 8, capacity = 250)
        self.G.add_edge(6, 1, capacity = 136)
        self.G.add_edge(6, 3, capacity = 3)
        self.G.add_edge(6, 4, capacity = 75)
        self.G.add_edge(6, 7, capacity = 303)
        self.G.add_edge(8, 0, capacity = 11)
        self.G.add_edge(8, 3, capacity = 134)
        self.G.add_edge(8, 4, capacity = 102)
        self.G.add_edge(8, 6, capacity = 112)
        self.G.add_edge(8, 7, capacity = 33)

        s = 5;
        t = 7;

        self.run_test(s,t,draw=True)

    def test_small(self): # Nedritad, returns non sensitive edge
        max_flow = nx.maximum_flow
        G = nx.complete_graph(7, create_using=nx.DiGraph());

        G.remove_edge(0,3);
        G.remove_edge(0,4);
        G.remove_edge(1,0);
        G.remove_edge(1,2);
        G.remove_edge(1,4);
        G.remove_edge(1,5);
        G.remove_edge(1,6);
        G.remove_edge(2,0);
        G.remove_edge(2,3);
        G.remove_edge(3,1);
        G.remove_edge(3,4);
        G.remove_edge(3,5);
        G.remove_edge(4,2);
        G.remove_edge(4,5);
        G.remove_edge(4,6);
        G.remove_edge(5,0);
        G.remove_edge(5,2);
        G.remove_edge(6,0);
        G.remove_edge(6,2);
        G.remove_edge(6,3);
        G.remove_edge(6,5);
        G.remove_edge(1,3);
        G.remove_edge(4,3);
        G.remove_edge(5,3);
        G.remove_edge(4,0);
        G.remove_edge(4,1);

        G[0][1]['capacity'] = 63;
        G[0][2]['capacity'] = 97;
        G[0][5]['capacity'] = 40;
        G[0][6]['capacity'] = 164;
        G[2][1]['capacity'] = 59;
        G[2][4]['capacity'] = 75;
        G[2][5]['capacity'] = 167;
        G[2][6]['capacity'] = 169;
        G[3][0]['capacity'] = 173;
        G[3][2]['capacity'] = 27;
        G[3][6]['capacity'] = 31;
        G[5][1]['capacity'] = 49;
        G[5][4]['capacity'] = 24;
        G[5][6]['capacity'] = 21;
        G[6][1]['capacity'] = 15;
        G[6][4]['capacity'] = 95;

        s = 3;
        t = 4;
        flow_g, F_g = max_flow(G, s, t);
        u,v = sensitive(G.copy(), s, t, F_g);
        G[u][v]["capacity"] = G[u][v]["capacity"] - 1;
        new_flow_g, new_F_g = max_flow(G, s, t);
        print new_flow_g, "<", flow_g, "?"
        # Expected output: new_flow_g < flow_g

    def test_small2(self):
        max_flow = nx.maximum_flow
        G = nx.complete_graph(7, create_using=nx.DiGraph());

        G.remove_edge(0,5);
        G.remove_edge(0,6);
        G.remove_edge(1,0);
        G.remove_edge(1,2);
        G.remove_edge(1,4);
        G.remove_edge(2,0);
        G.remove_edge(2,4);
        G.remove_edge(2,6);
        G.remove_edge(3,0);
        G.remove_edge(3,1);
        G.remove_edge(3,2);
        G.remove_edge(4,0);
        G.remove_edge(4,3);
        G.remove_edge(4,6);
        G.remove_edge(5,1);
        G.remove_edge(5,2);
        G.remove_edge(5,3);
        G.remove_edge(5,4);
        G.remove_edge(5,6);
        G.remove_edge(6,1);
        G.remove_edge(6,3);
        G.remove_edge(1,5);
        G.remove_edge(2,5);
        G.remove_edge(3,5);
        G.remove_edge(4,5);
        G.remove_edge(6,5);
        G.remove_edge(3,4);
        G.remove_edge(3,6);

        G[0][1]['capacity'] = 69;
        G[0][2]['capacity'] = 62;
        G[0][3]['capacity'] = 36;
        G[0][4]['capacity'] = 96;
        G[1][3]['capacity'] = 183;
        G[1][6]['capacity'] = 137;
        G[2][1]['capacity'] = 43;
        G[2][3]['capacity'] = 77;
        G[4][1]['capacity'] = 65;
        G[4][2]['capacity'] = 33;
        G[5][0]['capacity'] = 39;
        G[6][0]['capacity'] = 103;
        G[6][2]['capacity'] = 52;
        G[6][4]['capacity'] = 106;

        s = 5;
        t = 3;
        flow_g, F_g = max_flow(G, s, t);
        u,v = sensitive(G.copy(), s, t, F_g);
        G[u][v]["capacity"] = G[u][v]["capacity"] - 1;
        new_flow_g, new_F_g = max_flow(G, s, t);
        print new_flow_g, "<", flow_g, "?"
        # Expected output: new_flow_g < flow_g

    @classmethod
    def tearDownClass(cls):
        if HAVE_PLT:
            plt.show()

if __name__ == "__main__":
    unittest.main()
