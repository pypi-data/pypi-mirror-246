from typing import Self
from doltcli import Dolt
import os
import tempfile
import atexit


class DoltRepo:
    def __init__(self: Self, repo_name: str, branch: str = "main") -> None:
        self.repo_name = repo_name
        self.branch = branch
        self.tmp_folder = tempfile.TemporaryDirectory()
        self.dolt = Dolt.clone(repo_name, self.tmp_folder.name, branch=branch)
        atexit.register(self.cleanup)

    def cleanup(self: Self) -> None:
        self.tmp_folder.cleanup()

    def ls(self: Self):
        return self.dolt.ls()
        # pass

    def get_csv(self: Self, table_name: str, save_path: str) -> None:
        # If save_path is relative, make it absolute
        if not os.path.isabs(save_path):
            save_path = os.path.join(os.getcwd(), save_path)
        self.dolt.table_export(table_name, save_path, force=True, file_type="csv")
