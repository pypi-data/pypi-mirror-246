"""Searches a given file's parents for a directory with a given name and adds it to sys.path."""

__version__ = "0.3"

import sys
from pathlib import Path

def add_to_sys_path(file, root_dir_name, min_depth=0, debug=False):
    parents = Path(file).resolve().parents
    for i in range(min_depth, len(parents)):
        if parents[i].name == root_dir_name:
            if debug:
                print(f"add-root-to-sys-path: Found root dir '{root_dir_name}' at '{parents[i]}'")
            sys.path.append(str(Path(file).resolve().parents[i]))
            return
    if debug:
        print(f"add-root-to-sys-path: WARNING: root dir '{root_dir_name}' not found.")
