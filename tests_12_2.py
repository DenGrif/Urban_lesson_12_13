# -*- coding: utf-8 -*-
import unittest
from runner import Runner, Tournament

class TournamentTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.all_results = {}

    def setUp(self):
        self.usain = Runner("Усэйн", speed=10)
        self.andrey = Runner("Андрей", speed=9)
        self.nick = Runner("Ник", speed=3)

    @classmethod
    def tearDownClass(cls):
        print("\nРезультаты всех тестов:")
        for test_name, result in cls.all_results.items():
            readable_result = {place: participant.name for place, participant in result.items()}
            print(f"{test_name}: {readable_result}")

    def test_usain_and_nick(self):
        # Усэйн и Ник
        tournament = Tournament(90, self.usain, self.nick)
        results = tournament.start()

        self.all_results['Usain and Nick'] = results

    def test_andrey_and_nick(self):
        # Андрей и Ник
        tournament = Tournament(90, self.andrey, self.nick)
        results = tournament.start()

        self.all_results['Andrey and Nick'] = results

    def test_usain_andrey_nick(self):
        # Усэйн, Андрей и Ник"""
        tournament = Tournament(90, self.usain, self.andrey, self.nick)
        results = tournament.start()

        self.all_results['Usain, Andrey and Nick'] = results

# Запуск тестов
if __name__ == '__main__':
    unittest.main()
