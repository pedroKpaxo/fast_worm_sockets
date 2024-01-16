from pydantic import BaseModel
import secrets


class Player(BaseModel):
    """"A player in the game."""
    name: str
    money: float = 100
    id: str = secrets.token_urlsafe(12)

    def win(self, bet):
        """Win the bet."""
        self.money += bet

    def lose(self, bet):
        """Lose the bet."""
        self.money -= bet
