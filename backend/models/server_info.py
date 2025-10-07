from pydantic import BaseModel
from typing import Optional, Dict, List, Any
from enum import Enum


class ServerStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    UNKNOWN = "unknown"


class BaseServerInfo(BaseModel):
    """Base model for live server information that all game servers should provide."""
    # Basic server info
    status: ServerStatus
    latency: Optional[float] = None
    version: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None # Base64-encoded
    mods: Optional[List[Dict[str, Any]]] = None
    game_mode: Optional[str] = None
    map_name: Optional[str] = None
    password_protected: Optional[bool] = None
    anti_cheat_enabled: Optional[bool] = None
    
    # Player information
    players_online: Optional[int] = None
    players_max: Optional[int] = None
    player_list: Optional[List[str]] = None
    
    error_message: Optional[str] = None


class MinecraftServerInfo(BaseServerInfo):
    """Minecraft-specific server information."""


class FactorioServerInfo(BaseServerInfo):
    """Factorio-specific server information."""
    application_version: Optional[str] = None
    host_settings: Optional[Dict[str, Any]] = None
    require_user_verification: Optional[bool] = None
    allow_commands: Optional[str] = None


class SatisfactoryServerInfo(BaseServerInfo):
    """Satisfactory-specific server information."""
    sub_state: Optional[int] = None
    num_public_connections: Optional[int] = None
    max_public_connections: Optional[int] = None
    beacon_port: Optional[int] = None


class ArkServerInfo(BaseServerInfo):
    """ARK-specific server information."""
    server_name: Optional[str] = None
    game_id: Optional[str] = None
    steam_id: Optional[str] = None
    day_time: Optional[str] = None
    official: Optional[bool] = None
    pve: Optional[bool] = None
    battle_eye: Optional[bool] = None