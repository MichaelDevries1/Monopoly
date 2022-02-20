import unittest

from Monopoly.game import Monopoly as mon


class TestMonopoly(unittest.TestCase):
    def test_newPlayerList(self):
        Basis = ['Michael', 'Kayla', 'Nathan', 'Summer']
        testing_list = []
        testing_list = mon.newPlayerList(testing_list)
        result = [testing_list[0].]
        self.assertEqual()
