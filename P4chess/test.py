import unittest

from controller import RunTournamentController
from model import Player, Match


class TestTournament(unittest.TestCase):
    def setUp(self):
        self.player1 = Player("Player 1", "JD", "01/08/2000", "ZZ12345")
        self.player2 = Player("Player 2", "AA", "10/08/2000", "TT45678")
        self.player3 = Player("Player 3", "YY", "01/10/2005", "II67895")
        self.player4 = Player("Player 4", "ZZ", "05/08/1990", "YU54321")

        self.controller = RunTournamentController()
        self.controller.tournament_players = [self.player1, self.player2, self.player3, self.player4]

    def test_match_creation(self):
        match = Match(self.player1, self.player2)
        self.assertEqual(match.player1, self.player1)
        self.assertEqual(match.player2, self.player2)

    def test_generate_pairs(self):
        pairs = self.controller.generate_pair_by_score(0)
        self.assertEqual(len(pairs), 2)
        self.assertEqual(pairs[0][0], pairs[0][1])

if __name__ == '__main__':
    unittest.main