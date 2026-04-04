from enum import Enum
from typing import Dict

class ServerKey(Enum):
    GLOBAL = 'global'
    TAIWAN = 'tw'

SERVERS: Dict[ServerKey, str] = {
    ServerKey.GLOBAL.value: 'Global',
    ServerKey.TAIWAN.value: 'TW',
}