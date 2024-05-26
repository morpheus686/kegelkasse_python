from dataclasses import dataclass


@dataclass
class DefaultTeamPlayer:
    id: int
    player: int
    team: int


@dataclass
class Game:
    id: int
    team: int
    date: str


@dataclass
class Penalty:
    id: int
    description: str
    type: int
    penalty: float
    lower_limit: int
    upper_limit: int
    get_value_by_parent: bool


@dataclass
class PenaltyKind:
    id: int
    description: str


@dataclass
class Player:
    id: int
    name: str


@dataclass
class PlayerPenalties:
    id: int
    game_player: int
    penalty: int
    value: int
    penalty_navigation: Penalty = None


@dataclass
class Team:
    id: int
    name: str


@dataclass
class TeamPenalties:
    id: int
    team: int
    penalty: int


@dataclass
class GamePlayers:
    id: int
    game: int
    player: int
    paid: float
    full: int
    clear: int
    sum_points: int
    errors: int
    player_penalties_navigation: list[PlayerPenalties] = None
