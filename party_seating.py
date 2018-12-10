#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
'''
Assignment 3: Party seating problem

Team Number:
Student Names:
'''
import unittest

# If your solution needs a queue, you can use this one:
from collections import deque

def party(known):
    """
    Sig:    int[1..m, 1..n] ==> boolean, int[1..j], int[1..k]
    Pre:
    Post:
    Ex:     [[1,2],[0],[0]] ==> True, [0], [1,2]
    """
    A = []
    B = []
    guest_ID = 0;

    for guest in known:
        print "Looking at guest:", guest_ID, "With friends:", guest
        if len(guest) == 0: # If length of guest is 0, then they know no one.
            print "You have zero friends!"
            A.append(guest_ID)
        else:
            friend_in_A = False
            friend_in_B = False
            for friend in guest: # Iterate over friends that guest know
                print "Finding for friend", friend
                if friend in A:
                    print friend, "is in", A
                    friend_in_A = True
                elif friend in B:
                    print friend, "is in", B
                    friend_in_B = True

            if friend_in_A and friend_in_B:
                print "Friends in both tables!", A, B
                return False, [], []

            if friend_in_A:
                B.append(guest_ID)
            else:
                A.append(guest_ID)

        guest_ID += 1
        print "----------------------------"


    print "Table A:", A, "Table B:", B

    return True, A, B

class PartySeatingTest(unittest.TestCase):
    """Test suite for party seating problem
    """

    def test_sanity(self):
        """Sanity test

        A minimal test case.
        """
        #K = [[1,2],[0],[0]]
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

if __name__ == '__main__':
    unittest.main()
