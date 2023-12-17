################################################################################
# Environment
################################################################################
import platform
import sys
from enum import IntEnum
from pathlib import Path

from pydantic import ValidationError
from pydantic_settings import BaseSettings

ROOT_DIR = Path(__file__).parent.parent.parent.absolute()


class Os(IntEnum):
    WIN = 1
    MAC = 2
    LINUX = 3


plt = platform.system()
if plt == "Windows":
    OS = Os.WIN
elif plt == "Linux":
    OS = Os.LINUX
elif plt == "Darwin":
    OS = Os.MAC
else:
    print("Unidentified system")
    sys.exit(1)


class Environment(BaseSettings, extra="allow"):
    run_env: str
    log_level: str = "INFO"

    def __init__(self, **values):
        super().__init__(**values)

    def log_config(self) -> dict:
        cfg = self.model_dump(mode="json")
        skip_keys = ()
        sanitized_cfg = {k: v for k, v in cfg.items() if k not in skip_keys}
        return sanitized_cfg


try:
    config = Environment()
except ValidationError as e:
    print(f"Error loading config: {e}")
    print("Make sure all required environment variables are set.")
    sys.exit(1)
