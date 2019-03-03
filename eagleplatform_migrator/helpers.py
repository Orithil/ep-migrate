import json
import shutil
import sys
import time
from colorama import init, deinit
from colorama import Fore


def savelist(filename, jsondict):
    """ Save dictionary as JSON file to local folder.

    Keyword arguments:
    filename -- file to write in
    jsondict -- dictionary to dump.
    """
    with open(filename, "w") as file:
        json.dump(jsondict, file, indent=2, ensure_ascii=False)
        cprint('success', f"JSON dumped to {filename}\nDone!")


def cprint(message_type='error', message='No input provided'):
    """ Print colored output.

    Keyword arguments:
    type -- type of message to be printed defines color.
            Possible values: 'error'(default), 'info', 'warning', 'success'
    message -- string to print.
    """
    init(autoreset=True)
    types = {'error': Fore.RED, 'info': Fore.CYAN,
             'warning': Fore.MAGENTA, 'success': Fore.GREEN}
    color = types[message_type]
    print(f"{color}{message}")
    deinit()


def home_size():
    """ Return space left /home partition in GB. """
    return int(shutil.disk_usage("/home")[2] / (1024**3))


def reporthook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration))
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" %
                     (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()
