from satisfactory_api_client import SatisfactoryAPI
from satisfactory_api_client.exceptions import APIError
from satisfactory_api_client.data.minimum_privilege_level import MinimumPrivilegeLevel
from typing import cast, TypedDict

from gamefleet.models.server_info import SatisfactoryServerInfo, ServerStatus


class ServerGameState(TypedDict):
    activeSessionName: str
    numConnectedPlayers: int
    playerLimit: int
    techTier: int
    activeSchematic: str
    gamePhase: str
    isGameRunning: bool
    totalGameDuration: int
    isGamePaused: bool
    averageTickRate: float
    autoLoadSessionName: str


class ServerStateResponse(TypedDict):
    serverGameState: ServerGameState


async def get_satisfactory_server_info(address: str, port: int = 7777) -> SatisfactoryServerInfo:
    try:
        api = SatisfactoryAPI(host='play.code-support.de', port=7777)
        
        # health = cast(dict, api.health_check())
        # if not health['success'] or health['health'] != 'healthy':
        #     return SatisfactoryServerInfo(
        #         status=ServerStatus.OFFLINE,
        #         error_message="Server is reachable but unhealthy"
        #     )

        api.passwordless_login(MinimumPrivilegeLevel.CLIENT)
        server_data = cast(ServerStateResponse, api.query_server_state().data)
        status = server_data['serverGameState']
        
        print(server_data)
        
        return SatisfactoryServerInfo(
            status=ServerStatus.ONLINE,
            latency=None,
            players_online=status['numConnectedPlayers'],
            players_max=status['playerLimit'],
            player_list=None,
            map_name=None,
            game_mode=None,
            description=None,
            version=None,
            password_protected=None,
            anti_cheat_enabled=None,
            # Satisfactory-specific fields
            session_name=status['activeSessionName'],
            tech_tier=status['techTier'],
            game_phase=status['gamePhase'],
            total_game_duration=status['totalGameDuration'],
            avg_tick_rate=status['averageTickRate']
        )
    except ConnectionRefusedError:
        return SatisfactoryServerInfo(
            status=ServerStatus.OFFLINE,
            error_message="Server is offline or unreachable"
        )
    except TimeoutError:
        return SatisfactoryServerInfo(
            status=ServerStatus.OFFLINE,
            error_message="Connection timed out"
        )
    except APIError as e:
        return SatisfactoryServerInfo(
            status=ServerStatus.UNKNOWN,
            error_message=f"Internal API error occurred: {e}"
        )
    except Exception as e:
        return SatisfactoryServerInfo(
            status=ServerStatus.UNKNOWN,
            error_message=str(e)
        )


