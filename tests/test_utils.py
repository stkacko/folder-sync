import sys

import pytest

from folder_sync import utils as uut


@pytest.mark.parametrize(
    "argv, expected",
    [
        (
            ["prog", "source_folder", "replica_folder"],
            {
                "source_folder": "source_folder",
                "replica_folder": "replica_folder",
                "sync_interval": 60,
                "log_file": "sync.log",
            },
        ),
        (
            [
                "prog",
                "source_folder",
                "replica_folder",
                "--sync_interval",
                "1",
                "--log_file",
                "log_file",
            ],
            {
                "source_folder": "source_folder",
                "replica_folder": "replica_folder",
                "sync_interval": 1,
                "log_file": "log_file",
            },
        ),
    ],
)
def test_parse_arguments(argv, expected):
    sys.argv = argv
    args = uut.parse_arguments()
    assert vars(args) == expected


def test_parse_arguments_invalid_sync_interval():
    sys.argv = ["prog", "source_folder", "replica_folder", "--sync_interval", "0"]
    with pytest.raises(ValueError, match="Sync interval must be a positive integer."):
        uut.parse_arguments()
