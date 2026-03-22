from pathlib import Path
from typing import Any

import yaml


def load_yaml_config(file_path: Path) -> dict[str, Any]:
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)