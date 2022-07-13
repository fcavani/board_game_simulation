import pytest
from src.board import Board, BoardType, InvalidPosition
from src.player import Player, PlayerType
from src.behavior import Passive
from src.property import Property


def test_invalid_position():
    player = Player('player 1', Passive())
    board = _setup_board([player])
    with pytest.raises(InvalidPosition) as exec_info:
        board.position(player)


def test_move_by_zero():
    player = Player('player 1', Passive())
    board = _setup_board([player])
    with pytest.raises(InvalidPosition) as exec_info:
        board.move(player, 0)


def test_move():
    player = Player('player 1', Passive())
    board = _setup_board([player])
    board.move(player, 1)
    pos = board.position(player)
    assert pos.name == 'property 0'


def test_move_overflow():
    player = Player('player 1', Passive())
    board = _setup_board([player])
    board.move(player, 6)
    pos = board.position(player)
    assert pos.name == 'property 1'


def _setup_board(players: PlayerType) -> BoardType:
    properties = [
        Property('property 0', 10, 1),
        Property('property 1', 10, 1),
        Property('property 2', 10, 1),
        Property('property 3', 10, 1),
    ]
    return Board(
        players=players,
        properties=properties
    )
