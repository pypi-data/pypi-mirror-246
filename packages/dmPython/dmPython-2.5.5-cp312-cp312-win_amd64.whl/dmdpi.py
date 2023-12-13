import ctypes
import os
import sys

dpi_path = os.path.dirname(__file__) + '\\dpi'
dpi_path.replace('\\', '\\\\')
if dpi_path not in os.environ['PATH']:
    os.environ['PATH'] = dpi_path + ';' + os.environ['PATH']
if sys.version_info[:2] > (3,7):
    os.add_dll_directory(dpi_path)
else:
    ctypes.WinDLL('dmdpi.dll')
