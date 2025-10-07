from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_session
from services.game_server_service import GameServerService


async def get_game_server_service(
    session: AsyncSession = Depends(get_session)
) -> GameServerService:
    """Dependency to get GameServerService instance."""
    return GameServerService(session)