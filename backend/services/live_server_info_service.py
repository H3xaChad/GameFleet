from typing import Union
from models.server_info import (
    BaseServerInfo, MinecraftServerInfo, FactorioServerInfo, 
    SatisfactoryServerInfo, ArkServerInfo, ServerStatus
)
from db.models.game_server_type import GameServerType
from lib.query.minecraft import get_minecraft_server_info
from lib.query.factorio import get_factorio_server_info
from lib.query.satisfactory import get_satisfactory_server_info
from lib.query.ark_ase import get_ark_ase_server_info
from lib.query.ark_asa import get_ark_asa_server_info


class LiveServerInfoService:
    """Service for fetching live server information from game servers."""
    
    @staticmethod
    def get_server_info(
        server_type: GameServerType, 
        address: str, 
        port: int
    ) -> BaseServerInfo:
        """
        Fetch live server information based on server type.
        
        Args:
            server_type: The type of game server
            address: Server IP address or hostname
            port: Server port
            
        Returns:
            Game-specific server info object
        """
        match server_type:
            case GameServerType.minecraft:
                return get_minecraft_server_info(address, port)
            
            case GameServerType.factorio:
                return get_factorio_server_info(address, port)
            
            case GameServerType.satisfactory:
                return get_satisfactory_server_info(address, port)
            
            case GameServerType.ark_ase:
                return get_ark_ase_server_info(address, port)
            
            case GameServerType.ark_asa:
                return get_ark_asa_server_info(address, port)
            
            case GameServerType.valheim:
                # TODO: Implement Valheim server querying
                return BaseServerInfo(
                    status=ServerStatus.UNKNOWN,
                    address=address,
                    port=port,
                    error_message="Valheim server querying not implemented yet"
                )
            
            case _:
                return BaseServerInfo(
                    status=ServerStatus.UNKNOWN,
                    address=address,
                    port=port,
                    error_message=f"Unsupported server type: {server_type}"
                )
    
    @staticmethod
    def get_basic_status(server_type: GameServerType, address: str, port: int) -> dict:
        """
        Get basic server status for legacy compatibility.
        
        Args:
            server_type: The type of game server
            address: Server IP address or hostname
            port: Server port
            
        Returns:
            Basic status dictionary
        """
        server_info = LiveServerInfoService.get_server_info(server_type, address, port)
        
        return {
            "online": server_info.status == ServerStatus.ONLINE,
            "address": server_info.address,
            "port": server_info.port,
            "players_online": server_info.players_online,
            "players_max": server_info.players_max,
            "game_version": server_info.game_version,
            "latency": server_info.latency,
            "error": server_info.error_message if server_info.status != ServerStatus.ONLINE else None
        }