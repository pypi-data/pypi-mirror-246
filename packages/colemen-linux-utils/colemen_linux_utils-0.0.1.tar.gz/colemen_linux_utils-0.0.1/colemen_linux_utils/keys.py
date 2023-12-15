# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

import colemen_utils as c
import colemen_linux_utils.settings as _settings
import subprocess
import time
from colemen_linux_utils.clipboard import get

def execute_cmd(cmd):
    if _settings.control.is_linux is False:
        return None
    cmd = cmd.replace("//","/")
    subprocess.call(["/bin/bash", "-c", cmd])



def select_all(get_selection:bool=False):
    execute_cmd("xdotool key Ctrl+a")
    time.sleep(.1)
    if get_selection is True:
        execute_cmd("xdotool key Ctrl+c")
        time.sleep(.1)
        return get()

def copy_all():
    return select_all(get_selection=True)

def delete_all():
    select_all(get_selection=False)
    execute_cmd("xdotool key Delete")


def select_line(get_selection:bool=False):
    execute_cmd("xdotool key --repeat 3 End")
    time.sleep(.1)
    execute_cmd("xdotool key Shift+Home")
    if get_selection is True:
        time.sleep(.1)
        execute_cmd("xdotool key Ctrl+c")
        time.sleep(.1)
        return get()

def copy_line():
    return select_line(get_selection=True)




