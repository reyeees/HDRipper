from sys import platform

if platform == "win32":
    from ._win import WinTUI as _TUI
else:
    from ._unix import UnixTUI as _TUI
