import unittest

from game.__init__ import Monopoly as mon


class TestMonopoly(unittest.TestCase):
    def test_newPlayerList(self):
        basis = ['Michael', 'Kayla', 'Nathan', 'Summer']
        testing_list = []
        for i in range(1, 4):
            testing_list[i-1] = mon.newPlayer()
        self.assertEqual(basis, testing_list)


if __name__ == '__main__':
    TestMonopoly().test_newPlayerList()
