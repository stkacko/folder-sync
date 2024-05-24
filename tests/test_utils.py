from folder_sync import utils as uut


def test_parse_arguments(mocker):
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=uut.argparse.Namespace(
            source_folder="source_folder",
            replica_folder="replica_folder",
            sync_interval=1,
            log_file="log_file",
        ),
    )
    assert uut.parse_arguments() == uut.argparse.Namespace(
        source_folder="source_folder",
        replica_folder="replica_folder",
        sync_interval=1,
        log_file="log_file",
    )
