import argparse


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Synchronize two folders.")
    parser.add_argument("source_folder", type=str, help="Path to the source folder.")
    parser.add_argument("replica_folder", type=str, help="Path to the replica folder.")
    parser.add_argument(
        "--sync_interval",
        type=int,
        default=60,
        help="Synchronization interval in seconds. Default is 60 seconds.",
    )
    parser.add_argument(
        "--log_file",
        type=str,
        default="sync.log",
        help="Path to the log file. Default is 'sync.log' in the current directory.",
    )

    args = parser.parse_args()

    if args.sync_interval <= 0:
        raise ValueError("Sync interval must be a positive integer.")

    return args
