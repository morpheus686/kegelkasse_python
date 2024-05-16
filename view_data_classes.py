from dataclasses import dataclass

@dataclass
class SumPerPlayer:
    date: str
    team: str
    player_name: str
    penalty: float


@dataclass
class SumPerTeam:
    team_name: str
    penalty_sum: float


@dataclass
class SumPerGame:
    date: str
    team_name: str
    penalty_sum: float