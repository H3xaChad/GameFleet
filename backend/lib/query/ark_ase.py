from models.server_info import ArkServerInfo, ServerStatus


def get_ark_ase_server_info(address: str, port: int = 7778) -> ArkServerInfo:
    """
    Get live ARK: Survival Evolved server information.
    
    Args:
        address: Server IP address or hostname
        port: Server port (default: 7778)
        
    Returns:
        ArkServerInfo: Server information (not implemented yet)
    """
    # TODO: Implement ARK: SE server querying
    return ArkServerInfo(
        status=ServerStatus.UNKNOWN,
        address=address,
        port=port,
        error_message="ARK: Survival Evolved server querying not implemented yet"
    )