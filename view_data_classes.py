from dataclasses import dataclass


@dataclass
class SumPerPlayer:
    game_id: int
    date: str
    team_name: str
    player_id: int
    player_name: str
    penalty_sum: float
    full: int
    clear: int
    errors: int
    played: int
    result: int


@dataclass
class SumPerTeam:
    team_name: str
    penalty_sum: float


@dataclass
class SumPerGame:
    game_id: int
    penalty_sum: float


@dataclass
class ResultOfGame:
    id: int
    totalFull: int
    totalClear: int
    totalResult: int
    totalErrors: int
