import enum
from typing import Annotated, Any, Literal, Mapping, Union

from pydantic import BaseModel, Field, TypeAdapter


class MessageType(str, enum.Enum):
    AUTHENTICATED = 'authenticated'
    GAME_MOVE = 'game_move'
    GAME_STATE = 'game_state'
    GAME_CREATED = 'game_created'
    CONNECTED = 'connected'
    DISCONNECTED = 'disconnected'
    INVALID_MOVE = 'invalid_move'


class AuthenticatedMessageBody(BaseModel):
    message: str
    success: bool


class ConnectedMessageBody(BaseModel):
    message: str


class DisconnectedMessageBody(BaseModel):
    message: str


class GameMoveMessageBody(BaseModel):
    game_move: Mapping[Any, Any]


class GameCreatedMessageBody(BaseModel):
    message: str


class GameStateMessageBody(BaseModel):
    game_state: Mapping[Any, Any]


class InvalidMoveMessageBody(BaseModel):
    message: str


class AuthenticatedMessage(BaseModel):
    type: Literal[MessageType.AUTHENTICATED] = MessageType.AUTHENTICATED
    body: AuthenticatedMessageBody


class ConnectedMessage(BaseModel):
    type: Literal[MessageType.CONNECTED] = MessageType.CONNECTED
    body: ConnectedMessageBody


class DisconnectedMessage(BaseModel):
    type: Literal[MessageType.DISCONNECTED] = MessageType.DISCONNECTED
    body: DisconnectedMessageBody


class GameMoveMessage(BaseModel):
    type: Literal[MessageType.GAME_MOVE] = MessageType.GAME_MOVE
    body: GameMoveMessageBody


class GameCreatedMessage(BaseModel):
    type: Literal[MessageType.GAME_CREATED] = MessageType.GAME_CREATED
    body: GameCreatedMessageBody


class GameStateMessage(BaseModel):
    type: Literal[MessageType.GAME_STATE] = MessageType.GAME_STATE
    body: GameStateMessageBody


class InvalidMoveMessage(BaseModel):
    type: Literal[MessageType.INVALID_MOVE] = MessageType.INVALID_MOVE
    body: InvalidMoveMessageBody


GameMessage = Annotated[
    Union[
        AuthenticatedMessage,
        ConnectedMessage,
        DisconnectedMessage,
        GameMoveMessage,
        GameCreatedMessage,
        GameStateMessage,
        InvalidMoveMessage,
    ],
    Field(discriminator='type'),
]
GameMessageAdapter = TypeAdapter[GameMessage](GameMessage)
