import time

from folder_sync.folder_sync import FolderSync
from folder_sync.utils import parse_arguments


def main() -> None:
    args = parse_arguments()

    sync = FolderSync(
        args.source_folder, args.replica_folder, args.sync_interval, args.log_file
    )

    while True:
        sync.perform_synchronization()
        time.sleep(sync.sync_interval)


if __name__ == "__main__":
    main()
