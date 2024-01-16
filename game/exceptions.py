class MaxPlayerException(Exception):
    """Exception raised when the max number of players is reached."""

    def __init__(self):
        super().__init__('Max number of players reached')
