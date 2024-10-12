import sys
import os


def get_save_dir():
    system_paths = {
        "win32": "~/AppData/Roaming",
        "linux": "~/.local/share",
        "darwin": "~/Library/Application Support",
    }
    sys_path = system_paths.get(sys.platform)
    savefile = os.path.normpath(
        os.path.expanduser(os.path.join(sys_path, "jumping_game"))
    )
    return savefile
