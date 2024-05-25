# Folder Sync

Folder Sync is a Python application designed to synchronize files between two folders. It ensures that the source and replica folders exist and are not the same. It also handles directory synchronization, file synchronization, and removal of extra files from the replica folder.

## Features

- Validates that the source and replica folders exist and are not the same.
- Handles directory synchronization: If a directory exists in the source but not in the replica, it creates the directory in the replica.
- Handles file synchronization: If a file exists in the source but not in the replica, or if the file's content in the source and replica are not the same, it copies the file from the source to the replica.
- Removes extra files from the replica: If a file or directory exists in the replica but not in the source, it removes the file or directory from the replica.

## Project Management

This project is managed using [Rye](https://github.com/astral-sh/rye)

Installation of Rye varies depending on the operating system. For example, on Linux / macOS, you can install Rye using the following command:
```commandline
curl -sSf https://rye.astral.sh/get | bash
```

When Rye is installed, simply clone the project and run the following command to install the project dependencies:
```commandline
rye sync
```

## Usage

To use Folder Sync, run the following command:
```commandline
python main.py <source_folder> <replica_folder> --sync_interval <sync_interval> --log_file <log_file>
```

**Command Line Arguments:** 
>`source_folder`: Path to the source folder.
> 
>`replica_folder`: Path to the replica folder.
> 
>`--sync_interval`: Synchronization interval in seconds. Default is 60 seconds.
> 
>`--log_file`: Path to the log file. Default is 'sync.log' in the current directory.

