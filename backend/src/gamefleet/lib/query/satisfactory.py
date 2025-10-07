from gamefleet.models.server_info import SatisfactoryServerInfo, ServerStatus


def get_satisfactory_server_info(address: str, port: int = 7777) -> SatisfactoryServerInfo:
    """
    Get live Satisfactory server information.
    
    Args:
        address: Server IP address or hostname
        port: Server port (default: 7777)
        
    Returns:
        SatisfactoryServerInfo: Server information (not implemented yet)
    """
    # TODO: Implement Satisfactory server querying
    return SatisfactoryServerInfo(
        status=ServerStatus.UNKNOWN,
        error_message="Satisfactory server querying not implemented yet"
    )