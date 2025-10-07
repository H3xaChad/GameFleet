from gamefleet.models.server_info import FactorioServerInfo, ServerStatus


def get_factorio_server_info(address: str, port: int = 34197) -> FactorioServerInfo:
    """
    Get live Factorio server information.
    
    Args:
        address: Server IP address or hostname
        port: Server port (default: 34197)
        
    Returns:
        FactorioServerInfo: Server information (not implemented yet)
    """
    # TODO: Implement Factorio server querying
    return FactorioServerInfo(
        status=ServerStatus.UNKNOWN,
        error_message="Factorio server querying not implemented yet"
    )