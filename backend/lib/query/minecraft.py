from mcstatus import JavaServer
from models.server_info import MinecraftServerInfo, ServerStatus


def get_minecraft_server_info(address: str, port: int = 25565) -> MinecraftServerInfo:
    try:
        server = JavaServer.lookup(f"{address}:{port}")
        status = server.status()
        
        print(status)
        
        return MinecraftServerInfo(
            status=ServerStatus.ONLINE,
            latency=status.latency,
            version=f"{status.version.name} (protocol: {status.version.protocol})",
            description=status.motd.to_minecraft(),
            icon=status.icon,
            mods=None,
            game_mode=None,
            map_name=None,
            password_protected=None,
            anti_cheat_enabled=None,
            players_online=status.players.online,
            players_max=status.players.max,
            player_list=[player.name for player in status.players.sample] if status.players.sample else None,
        )
        
    except Exception as e:
        return MinecraftServerInfo(
            status=ServerStatus.OFFLINE,
            error_message=str(e)
        )
