from datetime import datetime

import pytest

from folder_sync import folder_sync as uut


def test_calculate_md5(tmp_path):
    temp_file = tmp_path / "temp_file.bin"

    temp_file.write_bytes(b"Hello!")

    md5_hash = uut.FolderSync.calculate_md5(str(temp_file))

    assert md5_hash == "952d2c56d0485958336747bcdd98590d"


def test_validate_folders(tmp_path):
    log_file = tmp_path / "log.txt"

    # source and replica folders are the same
    same_folder = tmp_path / "same"
    same_folder.mkdir()
    folder_sync = uut.FolderSync(str(same_folder), str(same_folder), 1, str(log_file))
    with pytest.raises(
        ValueError, match="Source and replica folders cannot be the same."
    ):
        folder_sync.validate_folders()

    # source folder does not exist
    non_existent_folder = tmp_path / "non_existent"
    folder_sync = uut.FolderSync(
        str(non_existent_folder), str(tmp_path), 1, str(log_file)
    )
    with pytest.raises(
        FileNotFoundError,
        match=f"Source folder {str(non_existent_folder)} does not exist.",
    ):
        folder_sync.validate_folders()

    # source folder is not a directory
    not_a_directory = tmp_path / "not_a_directory.txt"
    not_a_directory.write_text("Hello!")
    folder_sync = uut.FolderSync(str(not_a_directory), str(tmp_path), 1, str(log_file))
    with pytest.raises(
        ValueError, match=f"Source folder {str(not_a_directory)} is not a directory."
    ):
        folder_sync.validate_folders()

    # replica folder is not a directory
    source_folder = tmp_path / "source"
    source_folder.mkdir()
    folder_sync = uut.FolderSync(
        str(source_folder), str(not_a_directory), 1, str(log_file)
    )
    with pytest.raises(
        ValueError, match=f"Replica folder {str(not_a_directory)} is not a directory."
    ):
        folder_sync.validate_folders()


def test_handle_directory(tmp_path):
    source_folder = tmp_path / "source"
    replica_folder = tmp_path / "replica"
    log_file = tmp_path / "log.txt"

    folder_sync = uut.FolderSync(
        str(source_folder), str(replica_folder), 1, str(log_file)
    )

    source_folder.mkdir()

    folder_sync.handle_directory(str(source_folder), str(replica_folder))

    assert replica_folder.exists()
    assert replica_folder.is_dir()


def test_handle_file(tmp_path):
    source_folder = tmp_path / "source"
    replica_folder = tmp_path / "replica"
    log_file = tmp_path / "log.txt"

    folder_sync = uut.FolderSync(
        str(source_folder), str(replica_folder), 1, str(log_file)
    )

    source_folder.mkdir()

    source_file = source_folder / "source_file.txt"
    source_file.write_text("Hello!")

    replica_file = replica_folder / "source_file.txt"

    folder_sync.handle_file(str(source_file), str(replica_file))

    assert replica_file.exists()
    assert replica_file.is_file()
    assert replica_file.read_text() == "Hello!"


def test_copy_files_to_replica(tmp_path):
    source_folder = tmp_path / "source"
    replica_folder = tmp_path / "replica"
    log_file = tmp_path / "log.txt"

    folder_sync = uut.FolderSync(
        str(source_folder), str(replica_folder), 1, str(log_file)
    )

    source_folder.mkdir()

    source_file1 = source_folder / "source_file1.txt"
    source_file1.write_text("Hello!")

    source_file2 = source_folder / "source_file2.txt"
    source_file2.write_text("World!")

    folder_sync.copy_files_to_replica()

    replica_file1 = replica_folder / "source_file1.txt"
    replica_file2 = replica_folder / "source_file2.txt"

    assert replica_file1.exists()
    assert replica_file1.is_file()
    assert replica_file1.read_text() == "Hello!"

    assert replica_file2.exists()
    assert replica_file2.is_file()
    assert replica_file2.read_text() == "World!"


def test_remove_extra_files_from_replica(tmp_path):
    source_folder = tmp_path / "source"
    replica_folder = tmp_path / "replica"
    log_file = tmp_path / "log.txt"

    folder_sync = uut.FolderSync(
        str(source_folder), str(replica_folder), 1, str(log_file)
    )

    source_folder.mkdir()
    replica_folder.mkdir()

    source_file = source_folder / "source_file.txt"
    source_file.write_text("Hello!")

    replica_file = replica_folder / "replica_file.txt"
    replica_file.write_text("Hello!")

    folder_sync.remove_extra_files_from_replica()

    assert not replica_file.exists()
    assert not replica_file.is_file()
    assert replica_folder.exists()
    assert replica_folder.is_dir()


def test_walk_folder(tmp_path):
    source_folder = tmp_path / "source"
    replica_folder = tmp_path / "replica"
    log_file = tmp_path / "log.txt"

    folder_sync = uut.FolderSync(
        str(source_folder), str(replica_folder), 1, str(log_file)
    )

    source_folder.mkdir()
    replica_folder.mkdir()

    source_file = source_folder / "source_file.txt"
    source_file.write_text("Hello!")

    walk = list(folder_sync.walk_folder(str(source_folder), topdown=True))

    assert walk == [(str(source_file), str(replica_folder / "source_file.txt"))]


def test_perform_synchronization(tmp_path):
    source_folder = tmp_path / "source"
    replica_folder = tmp_path / "replica"
    log_file = tmp_path / "log.txt"

    folder_sync = uut.FolderSync(
        str(source_folder), str(replica_folder), 1, str(log_file)
    )

    source_folder.mkdir()

    source_file = source_folder / "source_file.txt"
    source_file.write_text("Hello!")

    folder_sync.perform_synchronization()

    replica_file = replica_folder / "source_file.txt"

    assert replica_file.exists()
    assert replica_file.is_file()
    assert replica_file.read_text() == "Hello!"
    assert log_file.exists()
    assert log_file.is_file()
    assert (
        log_file.read_text()
        == f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: Copied {str(source_file)} to {str(replica_file)}\n"
    )
