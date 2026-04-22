import cx_Freeze
import sys
import os


include_files = ["watticon.ico","C:\\Users\\tape\\AppData\\Local\\Programs\\Python\\Python37-32\\DLLs\\tcl86t.dll","C:\\Users\\tape\\AppData\\Local\\Programs\\Python\\Python37-32\\DLLs\\tk86t.dll"]
# include_files = ["watt.ico","C:\\Users\\Quincy N\\AppData\\Local\\Programs\\Python\\Python37-32\\DLLs\\tcl86t.dll","C:\\Users\\Quincy N\\AppData\\Local\\Programs\\Python\\Python37-32\\DLLs\\tk86t.dll"]

os.environ['TCL_LIBRARY'] = "C:\\Users\\tape\\AppData\\Local\\Programs\\Python\\Python37-32\\tcl\\tcl8.6"
# os.environ['TCL_LIBRARY'] = "C:\\Users\\Quincy N\\AppData\\Local\\Programs\\Python\\Python37-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\tape\\AppData\\Local\\Programs\\Python\\Python37-32\\tcl\\tk8.6"
# os.environ['TK_LIBRARY'] = "C:\\Users\\Quincy N\\AppData\\Local\\Programs\\Python\\Python37-32\\tcl\\tk8.6"

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("wattApplicationBeta.py", base=base,icon="watticon.ico")]



cx_Freeze.setup(
    name = "WATT",
    options = {"build_exe": {"packages": ["tkinter","pyodbc"], "include_files": include_files}},
    verion = "0.10",
    description = "Workload Awareness Tracking Tool",
    executables = executables
)

# include_files - include any files included in the script (images)
