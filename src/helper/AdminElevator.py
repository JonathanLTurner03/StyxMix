#################################################
#   Class is used to help elevate the script    #
#   to admin permissions if it is not already   #
#################################################
#
# Unsure if needed, made for potential future
# use cases, developed in 0.0.1-ALPHA

import sys
import ctypes


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def elevate_admin():
    if os.name is 'nt':
        if not is_admin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    else:
        if os.getuid() != 0:
            print(f'Script must run with sudo permissions. Attempting to elevate permissions...')
            os.execvp('sudo', ['sudo'] + sys.argv)