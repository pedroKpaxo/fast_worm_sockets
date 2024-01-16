from fastapi import WebSocket, WebSocketDisconnect

from game.base_handler import BroadcastManager, GamePlayMode

from game.exceptions import MaxPlayerException
from game.events import BetEvent, InitEvent
from app.lib.utils.logger import setup_logger
from game.player.schema import Player


logger = setup_logger('GAME')


class RouletteGameManager(BroadcastManager):
    def __init__(self):
        self.games: dict[str, GamePlayMode] = {}
        self.connections = {}

    async def initial_game_handler(self, websocket: WebSocket):
        """
        Handle a connection and dispatch it according to who is connecting.

        """
        # NOTE We only call accept() once per connection.
        await websocket.accept()
        start_json = InitEvent(**await websocket.receive_json())

        if start_json.type == 'join':
            await self.join_game(websocket, start_json)
        else:
            await self.start_game(websocket, start_json)

    async def start_game(self, websocket: WebSocket, start_json: InitEvent):
        """
        Start a new game and add it to the list of games.
        A
        """
        # Here we create a new game and add it to our dictionary of games.
        game_on = GamePlayMode()
        self.games[game_on.id] = game_on
        logger.info(f'Starting game {game_on.id}')

        try:
            # NOTE The player name is sent to the server
            player = Player(name=start_json.player)
            game_on.add_player(player)

            game_on.connections[websocket] = player.name

            # Start the first round of the game.
            game_on.start_round()
            game_on.save_state()

            logger.debug(f'Players:{game_on.players} ')

            # NOTE 1: The game key is sent to the client

            await websocket.send_json(game_on.emmit_init_event().model_dump())  # noqa
            await self.play(websocket, game_on)

        except MaxPlayerException as e:
            # Handles a user that tries to join a full game.
            await self.send_error(websocket, str(e))

        finally:
            # TODO: Create a log to save the game results.
            logger.error('Deleting game')
            del self.games[game_on.id]

    async def join_game(self, websocket: WebSocket, init_event: InitEvent):
        try:
            game = self.games[init_event.game]
        except KeyError:
            await self.send_error(websocket, 'Game does not exist')
            return

        player = Player(name=init_event.player)
        game.connections[websocket] = player.name

        try:
            game.add_player(player)
            logger.info(f'Player {player.name} is Joining game')

        except MaxPlayerException as e:
            await self.send_error(websocket, str(e))
            return

        game.save_state()

        await self.broadcast(game, f'Player {player.name} is Joining game')
        await self.broadcast(game, game.emit_update_event().model_dump())
        try:
            await self.play(websocket, game)

        except WebSocketDisconnect:
            # Handle client disconnection
            logger.warn(f"Client disconnected: {websocket}")
            player = game.connections.pop(websocket)
            game.remove_player(player)

        finally:
            # TODO: Create a log to save the game results.
            if websocket in game.connections:
                player = game.connections.pop(websocket)
                game.remove_player(player)

    async def play(self, websocket: WebSocket, game: GamePlayMode):
        """
        The main game loop.
        Here we have to handle the different events that can happen.
        """
        try:
            # Receive a message as JSON
            message: dict = await websocket.receive_json()
            logger.debug(f"Message received: {message}")

            if message.get('type') == 'join':
                player = Player(name=message.get('player'))
                game.add_player(player)
                game.save_state()
                await self.play(websocket, game)

            if message.get('type') == 'bet':
                bet_event = BetEvent(**message)
                logger.info(f'Player {bet_event.player_name} is betting')
                await self.broadcast(game, game.emit_update_event().model_dump())  # noqa

                game.save_state()
                await self.play(websocket, game)

        except WebSocketDisconnect:
            # Handle client disconnection
            logger.warn(f"Client disconnected: {websocket}")
            # remove the player from the game
            player = game.connections.pop(websocket)
            game.remove_player(player)
            await self.broadcast(game, f'Player {player} has left the game')
            await self.broadcast(game, game.emit_update_event().model_dump())

        except Exception as e:
            # Handle other exceptions
            logger.error(f"Error occurred: {e}")
