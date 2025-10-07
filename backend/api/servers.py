from fastapi import APIRouter, Depends, HTTPException
from typing import Sequence
from pydantic import BaseModel

from db.models.game_server_type import GameServerType
from db.models.game_server import GameServer
from services.game_server_service import GameServerService
from services.live_server_info_service import LiveServerInfoService
from dependencies import get_game_server_service
from models.server_info import BaseServerInfo


router = APIRouter()

class GameServerCreate(BaseModel):
    name: str
    game: GameServerType
    address: str
    port: int

class GameServerUpdate(BaseModel):
    name: str | None = None
    game: GameServerType | None = None
    address: str | None = None
    port: int | None = None
    

@router.get('', response_model=Sequence[GameServer])
async def get_servers(
    service: GameServerService = Depends(get_game_server_service)
):
    """Get all game servers from the database."""
    return await service.get_all_servers()


"""Create a new game server."""
@router.post('', response_model=GameServer)
async def create_server(
    server_data: GameServerCreate,
    service: GameServerService = Depends(get_game_server_service)
):
    return await service.create_server(server_data.model_dump())


"""Get a specific game server by ID."""
@router.get('/{server_id}', response_model=GameServer)
async def get_server(
    server_id: str,
    service: GameServerService = Depends(get_game_server_service)
):
    server = await service.get_server_by_id(server_id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    return server


"""Update an existing game server."""
@router.put('/{server_id}', response_model=GameServer)
async def update_server(
    server_id: str,
    server_data: GameServerUpdate,
    service: GameServerService = Depends(get_game_server_service)
):
    update_data = {k: v for k, v in server_data.model_dump().items() if v is not None}
    server = await service.update_server(server_id, update_data)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    return server


@router.delete('/{server_id}')
async def delete_server(
    server_id: str,
    service: GameServerService = Depends(get_game_server_service)
):
    """Delete a game server."""
    success = await service.delete_server(server_id)
    if not success:
        raise HTTPException(status_code=404, detail="Server not found")
    return {"message": "Server deleted successfully"}


@router.get('/by-type/{server_type}', response_model=Sequence[GameServer])
async def get_servers_by_type(
    server_type: GameServerType,
    service: GameServerService = Depends(get_game_server_service)
):
    """Get all servers of a specific game type."""
    return await service.get_servers_by_type(server_type)


@router.get('/{server_id}/live-info', response_model=BaseServerInfo)
async def get_server_live_info_by_id(
    server_id: str,
    service: GameServerService = Depends(get_game_server_service)
):
    """Get live information for a server by its database ID."""
    server = await service.get_server_by_id(server_id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    
    return LiveServerInfoService.get_server_info(
        server_type=server.game,
        address=server.address,
        port=server.port
    )

@router.get("/supported_types")
def supported_types() -> list[GameServerType]:
    """Get list of supported game server types."""
    return [game_server_type for game_server_type in GameServerType]