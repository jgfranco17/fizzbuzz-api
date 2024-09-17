from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class EnvironmentVariables:
    REDIS_HOST: Final[str] = "REDIS_HOST"
