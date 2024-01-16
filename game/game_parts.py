from pydantic import BaseModel
import secrets
import random


class Bet(BaseModel):
    """
    A class to represent a bet in the game.
    It has a player, a number and an amount.
    Also, a auto-generated id, to identify the bet, with
    a random string of 16 characters.
    """

    id: str = secrets.token_hex(16)
    """The bet id."""
    player: str
    """The player that placed the bet."""
    number: int
    """The number the player bet on."""
    amount: int
    """The amount of the bet."""


class RoundSpin(BaseModel):
    """A class to represent a spin record."""

    game_id: str
    number: int = None
    bets: list[Bet] = []
    round: int = 0
    is_over: bool = False

    def terminate(self):
        """Terminate the round."""
        self.is_over = True

    def add_bet(self, bet: Bet):
        """Add a bet to the round."""
        self.bets.append(bet)


class Roulette:
    """A roulette game."""

    def __init__(self):
        """Initialize the roulette."""
        self.number = 0

    def spin(self):
        """Spin the roulette."""
        self.number = random.randint(0, 36)
