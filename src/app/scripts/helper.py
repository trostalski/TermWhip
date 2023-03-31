import logging
from pathlib import Path

from app.scripts.constants import DOWNLOAD_DIR

logger = logging.getLogger(__name__)


def get_dir_in_downloads(startswith: str, dir_path: str) -> Path:
    result = None
    downlaods_path = Path(DOWNLOAD_DIR)
    for dir in downlaods_path.iterdir():
        if dir.is_dir() and dir.name.startswith(startswith):
            result = dir / dir_path
            break

    if result is None:
        raise FileNotFoundError("Could not find Snomed CT terminology directory")
    else:
        return result
