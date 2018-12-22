#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
'''
Assignment 3: Party seating problem

Team Number:
Student Names:
'''
import unittest
import networkx as nx
import random as rand

# If your solution needs a queue, you can use this one:
from collections import deque

def generate_list():
    # Max guests
    tak = rand.randint(16, 100)

    known = [None]*tak
    range_max = tak - 1
    for guest in range(0, range_max):

        # Max friends
        nr_of_relationships = rand.randint(0, rand.randint(0, 5))
        cur = []
        if known[guest] != None:
            cur = known[guest]
        else:
            known[guest] = cur
        for rel in range(0, nr_of_relationships):
            friend = rand.randint(0, range_max)

            fri = []
            if known[friend] != None:
                fri = known[friend]

            if friend != guest:

                cur.append(friend)
                known[guest] = cur

                fri.append(guest)
                known[friend] = fri

    for guest in range(0, len(known)):
        if known[guest] == None:
                       known[guest] = []

    return known

def party(known):
    """
    Sig:    int[1..m, 1..n] ==> boolean, int[1..j], int[1..k]
    Pre:
    Post:
    Ex:     [[1,2],[0],[0]] ==> True, [0], [1,2]
    """
    A = []
    # List containing all guests seated at table A
    # Type: int[]
    B = []
    # List containing all guests seated at table B
    # Type: int[]
    guest_ID = 0

    for guest in known:
    # Invariant: len(known)
    #   Variant: len(known)-1

        if len(guest) == 0: # If length of guest is 0, then they know no one.
            A.append(guest_ID)

        else:
            friend_in_A = False
            friend_in_B = False

            friend_in_A, friend_in_B = deep_search(known, A, B, guest, [], friend_in_A, friend_in_B)

            if friend_in_A and friend_in_B:
                return False, [], []

            if friend_in_A:
                B.append(guest_ID)
            else:
                A.append(guest_ID)

        guest_ID += 1

    return True, A, B

def deep_search(known, A, B, guest, visited, friend_in_A, friend_in_B):
    # Invariant: len(guest)
    #   Variant: len(guest)-1
    """
    Sig:    int[1..m, 1..n], int[0..x], int[0..y], int[], boolean, boolean \
            ==> boolean, boolean
    Pre:
    Post:
    Ex:     [[1,2],[0],[0]], [],  [], 0, [], False, False ==> False, False
            [[1,2],[0],[0]], [1], [], 0, [], False, False ==> True,  False
    """
    current = known.index(guest)
    if current not in visited:
        visited.append(current)

        for friend in guest: # Iterate over friends that guest know
        # Invariant: len(guest)
        #   Variant: len(guest)-1
            if friend in A:
                friend_in_A = True
            elif friend in B:
                friend_in_B = True

            if not friend_in_A and not friend_in_B:
                for n_friend in known[friend]:
                # Invariant: len(known[friend])
                #   Variant: len(known[friend])-1
                    in_A, in_B = deep_search(known, A, B, known[n_friend], visited, friend_in_A, friend_in_B)
                    if in_A:
                        friend_in_A = True
                    if in_B:
                        friend_in_B = True

    return friend_in_A, friend_in_B

class PartySeatingTest(unittest.TestCase):
    """Test suite for party seating problem
    """

    def est_sanity(self):
        """Sanity test

        A minimal test case.
        """

        K = [[9], [3], [], [1], [], [18], [7], [19, 11, 6], [15], [0, 13], [], [13, 7], [22, 23], [9, 11], [], [8], [], [20], [5], [20, 7], [17, 19], [], [12], [12], []]

        (found, A, B) = party(K)
        self.assertEqual(
            len(A) + len(B),
            len(K),
            "wrong number of guests: {!s} guests, tables hold {!s} and {!s}".format(
                len(K),
                len(A),
                len(B)
                )
            )
        for g in range(len(K)):
            self.assertTrue(
                g in A or g in B,
                "Guest {!s} not seated anywhere".format(g))
        for a1 in A:
            for a2 in A:
                self.assertFalse(
                    a2 in K[a1],
                    "Guests {!s} and {!s} seated together, and know each other".format(
                        a1,
                        a2
                        )
                    )
        for b1 in B:
            for b2 in B:
                self.assertFalse(
                    b2 in K[b1],
                    "Guests {!s} and {!s} seated together, and know each other".format(
                        b1,
                        b2
                        )
                    )

    def test_multi(self):
        for i in range (0, 10000):
            K = generate_list()
            (found, A, B) = party(K)
            print("test number " + str(i))

            if (found):
                self.assertEqual(
                    len(A) + len(B),
                    len(K),
                    "wrong number of guests: {!s} guests, tables hold {!s} and {!s}".format(
                        len(K),
                        len(A),
                        len(B)
                    )
                )
                for g in range(len(K)):
                    self.assertTrue(
                        g in A or g in B,
                        "Guest {!s} not seated anywhere".format(g))
                    for a1 in A:
                        for a2 in A:
                            self.assertFalse(
                                a2 in K[a1],
                                "Guests {!s} and {!s} seated together, and know each other".format(
                                    a1,
                                    a2
                                )
                            )
                            for b1 in B:
                                for b2 in B:
                                    self.assertFalse(
                                        b2 in K[b1],
                                        "Guests {!s} and {!s} seated together, and know each other".format(
                                            b1,
                                            b2
                                        )
                                    )

if __name__ == '__main__':
    unittest.main()
