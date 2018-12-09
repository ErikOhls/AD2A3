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

    for vert in F:
        for inner_vert in F[vert]:
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

    def est_insanity(self):
        if (list(map(lambda x: int(x), nx.__version__.split("."))) < [1, 9]):
            max_flow = nx.ford_fulkerson
        else:
            max_flow = nx.maximum_flow
            G = nx.complete_graph(10, create_using=nx.DiGraph());

            G.remove_edge(0,1);
            G.remove_edge(0,2);
            G.remove_edge(0,4);
            G.remove_edge(0,6);
            G.remove_edge(0,7);
            G.remove_edge(0,9);
            G.remove_edge(1,4);
            G.remove_edge(1,7);
            G.remove_edge(2,1);
            G.remove_edge(2,4);
            G.remove_edge(2,5);
            G.remove_edge(2,6);
            G.remove_edge(2,7);
            G.remove_edge(2,8);
            G.remove_edge(3,0);
            G.remove_edge(3,1);
            G.remove_edge(3,2);
            G.remove_edge(3,7);
            G.remove_edge(3,8);
            G.remove_edge(3,9);
            G.remove_edge(4,3);
            G.remove_edge(4,7);
            G.remove_edge(4,8);
            G.remove_edge(5,0);
            G.remove_edge(5,1);
            G.remove_edge(5,3);
            G.remove_edge(5,4);
            G.remove_edge(5,8);
            G.remove_edge(6,1);
            G.remove_edge(6,3);
            G.remove_edge(6,4);
            G.remove_edge(6,5);
            G.remove_edge(6,7);
            G.remove_edge(6,9);
            G.remove_edge(7,5);
            G.remove_edge(8,0);
            G.remove_edge(8,1);
            G.remove_edge(8,6);
            G.remove_edge(8,7);
            G.remove_edge(9,1);
            G.remove_edge(9,2);
            G.remove_edge(9,4);
            G.remove_edge(9,5);
            G.remove_edge(9,7);
            G.remove_edge(9,8);
            G.remove_edge(0,8);
            G.remove_edge(1,8);
            G.remove_edge(6,8);
            G.remove_edge(7,8);
            G.remove_edge(2,0);
            G.remove_edge(2,3);
            G.remove_edge(2,9);

            G[0][3]['capacity'] = 42;
            G[0][5]['capacity'] = 241;
            G[1][0]['capacity'] = 85;
            G[1][2]['capacity'] = 122;
            G[1][3]['capacity'] = 231;
            G[1][5]['capacity'] = 116;
            G[1][6]['capacity'] = 114;
            G[1][9]['capacity'] = 273;
            G[3][4]['capacity'] = 223;
            G[3][5]['capacity'] = 140;
            G[3][6]['capacity'] = 134;
            G[4][0]['capacity'] = 57;
            G[4][1]['capacity'] = 30;
            G[4][2]['capacity'] = 223;
            G[4][5]['capacity'] = 62;
            G[4][6]['capacity'] = 108;
            G[4][9]['capacity'] = 90;
            G[5][2]['capacity'] = 49;
            G[5][6]['capacity'] = 70;
            G[5][7]['capacity'] = 95;
            G[5][9]['capacity'] = 390;
            G[6][0]['capacity'] = 59;
            G[6][2]['capacity'] = 208;
            G[7][0]['capacity'] = 62;
            G[7][1]['capacity'] = 247;
            G[7][2]['capacity'] = 44;
            G[7][3]['capacity'] = 17;
            G[7][4]['capacity'] = 74;
            G[7][6]['capacity'] = 81;
            G[7][9]['capacity'] = 32;
            G[8][2]['capacity'] = 200;
            G[8][3]['capacity'] = 362;
            G[8][4]['capacity'] = 364;
            G[8][5]['capacity'] = 299;
            G[8][9]['capacity'] = 25;
            G[9][0]['capacity'] = 58;
            G[9][3]['capacity'] = 134;
            G[9][6]['capacity'] = 394;

            s = 8;
            t = 2;
            self.run_test(s,t,draw=True)
            #flow_g, F_g = max_flow(G, s, t);
            #u,v = sensitive(G.copy(), s, t, F_g);
            #G[u][v]["capacity"] = G[u][v]["capacity"] - 1;
            #new_flow_g, new_F_g = max_flow(G, s, t);

    def est_shit_test(self):
        if (list(map(lambda x: int(x), nx.__version__.split("."))) < [1, 9]):
            max_flow = nx.ford_fulkerson
        else:
            max_flow = nx.maximum_flow
            G = nx.complete_graph(8, create_using=nx.DiGraph());

            G.remove_edge(0,1);
            G.remove_edge(1,2);
            G.remove_edge(1,4);
            G.remove_edge(1,5);
            G.remove_edge(1,6);
            G.remove_edge(2,0);
            G.remove_edge(2,3);
            G.remove_edge(2,4);
            G.remove_edge(3,0);
            G.remove_edge(3,1);
            G.remove_edge(3,4);
            G.remove_edge(3,5);
            G.remove_edge(3,7);
            G.remove_edge(4,0);
            G.remove_edge(4,5);
            G.remove_edge(4,7);
            G.remove_edge(5,0);
            G.remove_edge(5,2);
            G.remove_edge(6,0);
            G.remove_edge(6,2);
            G.remove_edge(6,3);
            G.remove_edge(6,4);
            G.remove_edge(6,5);
            G.remove_edge(6,7);
            G.remove_edge(7,0);
            G.remove_edge(7,1);
            G.remove_edge(7,2);
            G.remove_edge(7,5);
            G.remove_edge(0,5);
            G.remove_edge(2,5);
            G.remove_edge(2,1);
            G.remove_edge(2,6);
            G.remove_edge(2,7);

            G[0][2]['capacity'] = 164;
            G[0][3]['capacity'] = 209;
            G[0][4]['capacity'] = 111;
            G[0][6]['capacity'] = 55;
            G[0][7]['capacity'] = 116;
            G[1][0]['capacity'] = 124;
            G[1][3]['capacity'] = 51;
            G[1][7]['capacity'] = 144;
            G[3][2]['capacity'] = 54;
            G[3][6]['capacity'] = 77;
            G[4][1]['capacity'] = 145;
            G[4][2]['capacity'] = 165;
            G[4][3]['capacity'] = 16;
            G[4][6]['capacity'] = 131;
            G[5][1]['capacity'] = 55;
            G[5][3]['capacity'] = 95;
            G[5][4]['capacity'] = 2;
            G[5][6]['capacity'] = 108;
            G[5][7]['capacity'] = 133;
            G[6][1]['capacity'] = 135;
            G[7][3]['capacity'] = 2;
            G[7][4]['capacity'] = 165;
            G[7][6]['capacity'] = 4;

            print "test", list(G)

            s = 5;
            t = 2;

            self.run_test(s,t,draw=True)

    @classmethod
    def tearDownClass(cls):
        if HAVE_PLT:
            plt.show()

if __name__ == "__main__":
    unittest.main()
