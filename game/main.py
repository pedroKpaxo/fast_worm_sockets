# Here we will define the main game loop and the main game class
# The game is a roulette game, where the player can bet on a number
# and win if the roulette lands on that number
# The game will be played in rounds, and each round will have a
# different number
# The player will start with a certain amount of money, and will
# be able to bet on the roulette
# If the player wins, the amount of money will be increased by the
# amount of the bet
# If the player loses, the amount of money will be decreased by the
# amount of the bet
# The game will end when the player runs out of money


import pickle

import secrets

from pydantic import BaseModel
from game.exceptions import MaxPlayerException
from game.game_parts import RoundSpin, Roulette
from game.player.schema import Player
from game.events.schemas import InitEvent
from app.lib.redis.client import RedisManager


class GameState(BaseModel):
    """The game state."""

    players: list[Player]
    round: int
    rounds: dict[int, RoundSpin]


class GameInitEvent(InitEvent):
    """The game state event."""

    state: GameState


class GameUpdateEvent(InitEvent):
    """The game state event."""
    type: str = "update"
    state: GameState


class Game:
    """The main game class."""
    MAX_PLAYERS = 4
    state_client = RedisManager()

    def __init__(self):
        """Initialize the game."""
        self.id = secrets.token_urlsafe(12)
        self.players: list[Player] = []
        self.roulette = Roulette()
        self.round = 0

        self.rounds: dict[int, RoundSpin] = {}
        self.current_round_spin: RoundSpin = None

    def add_player(self, player: Player):
        """
        Tries to add a player to the game.
        If the max number of players is reached, raises an exception.
        """
        if len(self.players) >= self.MAX_PLAYERS:
            raise MaxPlayerException()

        self.players.append(player)
        return True

    def remove_player(self, name: str):
        """Remove a player from the game."""
        for player in self.players:
            if player.name == name:
                self.players.remove(player)

    def get_player(self, name: str):
        """Get a player from the game."""
        return next((player for player in self.players if player.name == name), None)  # noqa

    def start_round(self):
        """Start a round."""
        # check if the round is over
        if self.current_round_spin and not self.current_round_spin.is_over:
            return self.current_round_spin

        # start a new round
        self.round += 1
        round_spin = RoundSpin(game_id=self.id,  round=self.round)
        self.rounds[self.round] = round_spin
        self.current_round_spin = round_spin
        return round_spin

    @property
    def state(self):
        """Get the current game state."""
        # trnasfor the rounds dict into list

        return GameState(**{
            'players': self.players,
            'round': self.round,
            'rounds': self.rounds,
            'id': self.id,
        })

    def emit_update_event(self):
        """Emit the update event."""
        return GameUpdateEvent(
            state=self.state,
            game=self.id,
        )

    def save_state(self):
        """Save the current game state to redis."""
        # NOTE: We are using the game id as the key
        # and the game state as the value and use redis mapping
        # to store the state
        pickle_state = pickle.dumps(self.state)
        self.state_client.set(self.id, pickle_state)

    def load_state(self):
        """Load the current game state from redis."""
        pickle_state = self.state_client.get(self.id)
        if pickle_state:
            state: GameState = pickle.loads(pickle_state)
            return state

    def emmit_init_event(self):
        """Emmit the init event."""
        return GameInitEvent(
            type="init",
            state=self.state,
            game=self.id,
        )
