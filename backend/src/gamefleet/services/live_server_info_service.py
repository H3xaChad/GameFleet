from typing import Union
from gamefleet.models.server_info import (
    BaseServerInfo, MinecraftServerInfo, FactorioServerInfo, 
    SatisfactoryServerInfo, ArkServerInfo, ServerStatus
)
from gamefleet.db.models.game_server_type import GameServerType
from gamefleet.lib.query.minecraft import get_minecraft_server_info
from gamefleet.lib.query.factorio import get_factorio_server_info
from gamefleet.lib.query.satisfactory import get_satisfactory_server_info
from gamefleet.lib.query.ark_ase import get_ark_ase_server_info
from gamefleet.lib.query.ark_asa import get_ark_asa_server_info


class LiveServerInfoService:
    """Service for fetching live server information from game servers."""
    
    @staticmethod
    def get_server_info(
        server_type: GameServerType, 
        address: str,
        port: int
    ) -> BaseServerInfo:
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
                    error_message="Valheim server querying not implemented yet"
                )
            
            case _:
                return BaseServerInfo(
                    status=ServerStatus.UNKNOWN,
                    address=address,
                    port=port,
                    error_message=f"Unsupported server type: {server_type}"
                )
