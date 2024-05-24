import argparse


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Synchronize two folders.")
    parser.add_argument("source_folder", type=str, help="Path to the source folder.")
    parser.add_argument("replica_folder", type=str, help="Path to the replica folder.")
    parser.add_argument(
        "sync_interval", type=int, help="Synchronization interval in seconds."
    )
    parser.add_argument("log_file", type=str, help="Path to the log file.")

    return parser.parse_args()
