import sys
import time

from folder_sync.folder_sync import FolderSync
from folder_sync.utils import parse_arguments


def main() -> None:
    try:
        args = parse_arguments()

        sync = FolderSync(
            args.source_folder, args.replica_folder, args.sync_interval, args.log_file
        )

        while True:
            sync.perform_synchronization()
            time.sleep(sync.sync_interval)

    except (FileNotFoundError, OSError, PermissionError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("Interrupted by user", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
