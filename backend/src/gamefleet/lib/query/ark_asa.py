from gamefleet.models.server_info import ArkServerInfo, ServerStatus


def get_ark_asa_server_info(address: str, port: int = 7778) -> ArkServerInfo:
    """
    Get live ARK: Survival Ascended server information.
    
    Args:
        address: Server IP address or hostname
        port: Server port (default: 7778)
        
    Returns:
        ArkServerInfo: Server information (not implemented yet)
    """
    # TODO: Implement ARK: SA server querying
    return ArkServerInfo(
        status=ServerStatus.UNKNOWN,
        error_message="ARK: Survival Ascended server querying not implemented yet"
    )