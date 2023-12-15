# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

from typing import Union
import colemen_utils as c
import colemen_linux_utils.settings as _settings
import subprocess
import time
from colemen_linux_utils.clipboard import get





def execute_cmd(cmd):
    # if _settings.control.is_linux is False:
    #     return None
    cmd = cmd.replace("//","/")
    subprocess.call(["/bin/bash", "-c", cmd])

def send_keys(keys:Union[str,list]):
    if isinstance(keys,(list)):
        keys = ' '.join(keys)
    keys = keys.replace("home","Home")
    keys = keys.replace("end","End")
    keys = keys.replace("shift","Shift")
    keys = keys.replace("shft","Shift")
    keys = keys.replace("control","Ctrl")
    keys = keys.replace("ctrl","Ctrl")
    keys = keys.replace("alt","Alt")
    keys = keys.replace("copy","Ctrl+c")
    keys = keys.replace("paste","Ctrl+v")

    execute_cmd(f"xdotool key {keys}")


def select_all(get_selection:bool=False):
    # prefix = "xdotool key"
    keys = "Ctrl+a"
    if get_selection is True:
        keys = "Ctrl+a copy"
    # command = f"{prefix} {keys}"
    # execute_cmd(command)
    send_keys(keys)
    if get_selection is True:
        return get()

def copy_all():
    return select_all(get_selection=True)

def delete_all():
    select_all(get_selection=False)
    execute_cmd("xdotool key Delete")


def select_line(get_selection:bool=False):
    # execute_cmd("xdotool key End End End")
    # time.sleep(.1)
    # execute_cmd("xdotool key Shift+Home")

    # prefix = "xdotool key"
    keys = ["end","end","end","shift+home"]
    if get_selection is True:
        keys.append("copy")

    # command = f"{prefix} {keys}"
    send_keys(keys)

    if get_selection is True:
        return get()


def copy_line():
    return select_line(get_selection=True)




