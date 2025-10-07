import uuid
from sqlmodel import SQLModel, Field

from db.models.game_server_type import GameServerType

class GameServer(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    game: GameServerType
    name: str = Field(max_length=100)
    address: str = Field(max_length=100)
    port: int = Field(ge=1, le=65535)