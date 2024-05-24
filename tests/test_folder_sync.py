from datetime import datetime

from folder_sync import folder_sync as uut


def test_calculate_md5(tmp_path):
    temp_file = tmp_path / "temp_file.bin"

    temp_file.write_bytes(b"Hello, Veeam team!")

    md5_hash = uut.FolderSync.calculate_md5(str(temp_file))

    assert md5_hash == "f6c28204890ae63b52a4271d5b88cbb8"


def test_ensure_replica_exists(tmp_path):
    source_folder = tmp_path / "source"
    replica_folder = tmp_path / "replica"
    log_file = tmp_path / "log.txt"

    folder_sync = uut.FolderSync(
        str(source_folder), str(replica_folder), 1, str(log_file)
    )

    folder_sync.ensure_replica_exists()

    assert replica_folder.exists()
    assert replica_folder.is_dir()


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
    source_file.write_text("Hello, Veeam team!")

    replica_file = replica_folder / "source_file.txt"

    folder_sync.handle_file(str(source_file), str(replica_file))

    assert replica_file.exists()
    assert replica_file.is_file()
    assert replica_file.read_text() == "Hello, Veeam team!"


def test_copy_files_to_replica(tmp_path):
    source_folder = tmp_path / "source"
    replica_folder = tmp_path / "replica"
    log_file = tmp_path / "log.txt"

    folder_sync = uut.FolderSync(
        str(source_folder), str(replica_folder), 1, str(log_file)
    )

    source_folder.mkdir()

    source_file = source_folder / "source_file.txt"
    source_file.write_text("Hello, Veeam team!")

    folder_sync.copy_files_to_replica()

    replica_file = replica_folder / "source_file.txt"

    assert replica_file.exists()
    assert replica_file.is_file()
    assert replica_file.read_text() == "Hello, Veeam team!"


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
    source_file.write_text("Hello, Veeam team!")

    replica_file = replica_folder / "replica_file.txt"
    replica_file.write_text("Hello, Veeam team!")

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
    source_file.write_text("Hello, Veeam team!")

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
    source_file.write_text("Hello, Veeam team!")

    folder_sync.perform_synchronization()

    replica_file = replica_folder / "source_file.txt"

    assert replica_file.exists()
    assert replica_file.is_file()
    assert replica_file.read_text() == "Hello, Veeam team!"
    assert log_file.exists()
    assert log_file.is_file()
    assert (
        log_file.read_text()
        == f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: Copied {str(source_file)} to {str(replica_file)}\n"
    )
