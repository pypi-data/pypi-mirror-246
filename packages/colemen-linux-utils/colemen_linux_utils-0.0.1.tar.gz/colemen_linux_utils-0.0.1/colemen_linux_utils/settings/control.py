
'''
The master control settings for colemen_linux_utils
'''


import platform


_os_platform = platform.system()

is_linux = False
if _os_platform == "Linux":
    is_linux = True


