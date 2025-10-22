from enum import Enum

class GameServerType(str, Enum):
    minecraft = "minecraft"
    factorio = "factorio"
    satisfactory = "satisfactory"
    ark_ase = "ark_ase"
    ark_asa = "ark_asa"
    valheim = "valheim"
