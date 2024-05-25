import hashlib
import os
import shutil
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Generator


class FolderSync:
    """
    A class to synchronize two folders by copying files from the source folder to the replica folder
    and removing extra files from the replica folder.
    """

    def __init__(
        self, source_folder: str, replica_folder: str, sync_interval: int, log_file: str
    ) -> None:
        self.source_folder = source_folder
        self.replica_folder = replica_folder
        self.sync_interval = sync_interval
        self.log_file = log_file

    @staticmethod
    def calculate_md5(file_path: str) -> str:
        """Calculate the MD5 hash of a file.

        :param file_path: path to the file
        """
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def validate_folders(self) -> None:
        """Ensure that the source and replica folders exist and are not the same.

        :raises FileNotFoundError: if the source folder does not exist
        :raises ValueError: if the source or replica folder is not a directory (for replica only if it already exists)
        :raises ValueError: if the source and replica folders are the same
        """
        if self.source_folder == self.replica_folder:
            raise ValueError("Source and replica folders cannot be the same.")

        if not os.path.exists(self.source_folder):
            raise FileNotFoundError(
                f"Source folder {self.source_folder} does not exist."
            )
        if not os.path.isdir(self.source_folder):
            raise ValueError(f"Source folder {self.source_folder} is not a directory.")

        if not os.path.isdir(self.replica_folder) and os.path.exists(
            self.replica_folder
        ):
            raise ValueError(
                f"Replica folder {self.replica_folder} is not a directory."
            )

    def handle_directory(self, src_path: str, dst_path: str) -> None:
        """Handle directory synchronization."""
        if os.path.isdir(src_path) and not os.path.exists(dst_path):
            os.makedirs(dst_path)
            self.log_action(f"Created directory {dst_path}")

    def handle_file(self, src_path: str, dst_path: str) -> None:
        """Handle file synchronization."""
        if os.path.isfile(src_path):
            src_md5 = self.calculate_md5(src_path)
            if not os.path.exists(dst_path) or (
                os.path.exists(dst_path) and src_md5 != self.calculate_md5(dst_path)
            ):
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                shutil.copy2(src_path, dst_path)
                self.log_action(f"Copied {src_path} to {dst_path}")

    def copy_files_to_replica(self) -> None:
        """Copy files from the source folder to the replica folder."""
        with ThreadPoolExecutor() as executor:
            for src_path, dst_path in self.walk_folder(
                self.source_folder, topdown=True
            ):
                executor.submit(self.handle_directory, src_path, dst_path)
                executor.submit(self.handle_file, src_path, dst_path)

    def remove_extra_files_from_replica(self) -> None:
        """Remove extra files from the replica folder."""
        with ThreadPoolExecutor() as executor:
            for dst_path, src_path in self.walk_folder(
                self.replica_folder, topdown=False
            ):
                if not os.path.exists(src_path):
                    if os.path.isfile(dst_path):
                        executor.submit(os.remove, dst_path)
                        self.log_action(f"Removed {dst_path}")
                    elif os.path.isdir(dst_path):
                        executor.submit(os.rmdir, dst_path)
                        self.log_action(f"Removed directory {dst_path}")

    def walk_folder(
        self, folder: str, topdown: bool = True
    ) -> Generator[tuple[str, str], None, None]:
        """Walk through the folder and yield the path and relative path of each file or directory.

        :param folder: path to the folder
        :param topdown: flag indicating whether to walk the folder top-down or bottom-up
        """
        for root, dirs, files in os.walk(folder, topdown=topdown):
            for name in dirs + files:
                path = os.path.join(root, name)
                if topdown:
                    rel_path = os.path.join(
                        self.replica_folder,
                        os.path.relpath(path, start=self.source_folder),
                    )
                else:
                    rel_path = os.path.join(
                        self.source_folder,
                        os.path.relpath(path, start=self.replica_folder),
                    )
                yield path, rel_path

    def perform_synchronization(self) -> None:
        """Perform the synchronization process."""
        self.validate_folders()
        self.copy_files_to_replica()
        self.remove_extra_files_from_replica()

    def log_action(self, message: str) -> None:
        """Log an action to the log file and print it to the console."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{timestamp}: {message}\n"
        print(log_message)
        with open(self.log_file, "a") as file:
            file.write(log_message)
