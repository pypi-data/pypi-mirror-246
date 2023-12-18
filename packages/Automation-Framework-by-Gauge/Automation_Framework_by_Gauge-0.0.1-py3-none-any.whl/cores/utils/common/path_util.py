import os
from pathlib import Path


class PathUtil:

    @staticmethod
    def get_prj_root_path() -> str:
        return os.path.dirname(Path(__file__).parent.parent)

    @staticmethod
    def join_prj_root_path(path: str) -> str:
        """Return root path: in same place as src"""
        return os.path.join(PathUtil.get_prj_root_path(), path)

    @staticmethod
    def is_path_correct(path: str) -> bool:
        return os.path.exists(path)
