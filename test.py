import unittest
from game import Player
from game import Go

from game.__init__ import Monopoly as mon


class TestMonopoly(unittest.TestCase):
    def test_newPlayer(self):
        m = Player('Michael')
        k = Player('Kayla')
        n = Player('Nathan')
        s = Player('Summer')
        basis = [m.getName(), k.getName(), n.getName(), s.getName()]
        testing_list = []
        for i in range(0, 4):
            newPlayer = mon.new_player()
            testing_list.append(newPlayer.getName())
        self.assertEqual(basis, testing_list)




unittest.main()