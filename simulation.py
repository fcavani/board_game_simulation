#! env python3

import copy
import random
from statistics import mean
from typing import Dict, List
from src.player import Player
from src.behavior import (
    Impulsive,
    Picky,
    Conservative,
    Random
)
from src.property import create_property
from src.bank import Bank
from src.board import Board
from src.game import Game


random.seed(42)


if __name__ == '__main__':
    timeout = 1000
    games = 300
    players = [
        Player('impulsive', Impulsive()),
        Player('picky', Picky()),
        Player('conservative', Conservative()),
        Player('random', Random())
    ]
    properties = [
        create_property(
            name=f'Property {i}',
            mu_value=2500,
            sigma_value=1500,
            mu_rent=0.02,
            sigma_rent=0.01
        )
        for i in range(1, 21)
    ]
    winners: Dict[str, int] = {
        player: 0
        for player in players
    }
    rounds: List[int] = list()
    for _ in range(games):
        p = copy.copy(players)
        bank = Bank(p, properties, open_balance=300)
        board = Board(p, properties)
        game = Game(p, bank, board, timeout=timeout, reward=100)
        winner, rounds_count = game.play()
        rounds.append(rounds_count)
        winners[winner] += 1
    timeouts = sum(map(lambda count: 1 if count == timeout else 0, rounds))
    mean_rounds = mean(rounds)
    rounds_no_timeout = [
        rounds_count
        for rounds_count in rounds
        if rounds_count < timeout
    ]
    mean_rounds_no_timeouts = mean(rounds_no_timeout if rounds_no_timeout else [0])
    print('Properties value and rent value:')
    for prop in properties:
        name = f'{prop}:'
        print(f'{name:<15} Value: ${prop.value:<13.2f} Rent: ${prop.rent:0.2f}')
    print('\nRounds finished by timeout:\t\t', timeouts)
    print('Mean rounds count:\t\t\t', round(mean_rounds, 2))
    print('Mean rounds count without timeouts:\t', round(mean_rounds_no_timeouts, 2))
    print('\nVictories percentage:')
    winners = {
        winner: round(100.0 * wins / games, 2)
        for winner, wins in sorted(
            winners.items(),
            key=lambda x: x[1],
            reverse=True
        )
    }
    for winner, wins in winners.items():
        name = str(winner)
        print(f'{name:<15}{wins}%')
    winner = next(iter(winners))
    print(f'\nWinner: {winner}')
