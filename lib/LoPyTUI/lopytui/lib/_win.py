import struct
import msvcrt
from re import match as re
from sys import stdin, stdout

from ctypes import LibraryLoader, WinDLL, byref, create_string_buffer
from ctypes.wintypes import DWORD


class WinTUI:
    def __init__(self) -> None:
        # just enabling terminal vizualising
        # self.conin = msvcrt.get_osfhandle(stdin.fileno())
        # self.conout = msvcrt.get_osfhandle(stdout.fileno())
        self.kernel32 = LibraryLoader(WinDLL).kernel32
        
        self.conin = self.kernel32.GetStdHandle(-10)
        self.conout = self.kernel32.GetStdHandle(-11)

        mode = DWORD()
        self.kernel32.GetConsoleMode(self.conout, byref(mode))
        self.kernel32.SetConsoleMode(self.conout, mode.value | 0x0004)

    def hidecur(self) -> None:
        stdout.write("\x1b[?25l")

    def showcur(self) -> None:
        stdout.write("\x1b[?25h")

    def choose(self, data: list, style: callable) -> int:
        """
        User choose tool (Windows)
        """
        ind = 0
        self.hidecur()
        pos = self.getcur()
        buffer = style(pos, data, ind)
        print(buffer, end = '', flush = True)
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch()

                if key == b"\r": # Enter, then exit. Whatever
                    # slc = buffer.count("\n")
                    print(f"\x1b[{pos[1]-1};{pos[0]}H")
                    break

                if key in [b"\x00", b"\xe0"]:
                    key = msvcrt.getch()
                    if key == b'H' and ind > 0: # up key
                        ind -= 1
                    if key == b'P' and ind < len(data) - 1: # down key
                        ind += 1

                buffer = style(pos, data, ind)
                print(buffer, end = '', flush = True)
        self.showcur()
        return ind

    def terminal_size(self) -> tuple[int]:
        """
        Get terminal size (Windows)
        """
        csbi = create_string_buffer(22)
        self.kernel32.GetConsoleScreenBufferInfo(self.conout, csbi)

        res = struct.unpack("hhhhHhhhhhh", csbi.raw)
        left, top, right, bottom = res[5:9]
        return [right - left + 1, bottom - top + 1]

    def getcur(self) -> tuple[int]:
        """
        Get cursor position (Windows)
        """
        OldStdinMode = DWORD()
        OldStdoutMode = DWORD()

        self.kernel32.GetConsoleMode(self.conin, byref(OldStdinMode))
        self.kernel32.SetConsoleMode(self.conin, 0)
        self.kernel32.GetConsoleMode(self.conout, byref(OldStdoutMode))
        self.kernel32.SetConsoleMode(self.conout, 7)

        try:
            _ = ""
            stdout.write("\x1b[6n")
            stdout.flush()
            while not (_ := _ + stdin.read(1)).endswith('R'):
                True
            res = re(r".*\[(?P<y>\d*);(?P<x>\d*)R", _)
        finally:
            self.kernel32.SetConsoleMode(self.conin, OldStdinMode)
            self.kernel32.SetConsoleMode(self.conout, OldStdoutMode)

        if res:
            return tuple(map(int, (res.group("x"), res.group("y"))))
        return (-1, -1)

    def input(self, prompt: str, 
              cfcnt: callable = lambda x: x) -> str:
        """
        Input function (Windows)
        prompt: string
        cfcnt: buffer ̶c̶o̶n̶t̶r̶o̶l cooking function, the result is written while updating the screen
        Solution is easy, though. And it doesnt caught keys when terminal is unfocused
        """
        buffer = []
        lng = stdout.write(prompt)
        cur = [lng + 1, self.getcur()[1]] # well, we need to control cursor manually too.
        fpos = cur.copy()

        term_size = self.terminal_size()

        while True:
            if msvcrt.kbhit(): 
                key = msvcrt.getch() #
                if key == b"\r": # Enter, then exit. Whatever
                    stdout.write("\n\r")
                    break

                elif key == b"\x08":
                    if fpos[0] < cur[0]: # Backspace
                        del buffer[cur[0] - lng - 2]
                        cur[0] -= 1

                # ill implement this later, fuck it
                elif key in [b"\x7f", b"\x17"]: # ctrl + backspace
                    if fpos[0] < cur[0]:
                        pos = cur[0] - lng - 1
                        if " " in buffer[:pos][::-1]:
                            for ccr in range(len(buffer[:pos])-1, 0, -1):
                                if buffer[ccr] == ' ':
                                    break
                                cur[0] -= 1
                                del buffer[ccr]
                        else:
                            del buffer[:]
                            cur[0] = lng+1

                elif key in [b"\x00", b"\xe0"]: # control iniciated
                    key = msvcrt.getch()
                    if (key == b"K") and (fpos[0] < cur[0]): # left arrow
                        cur[0] -= 1
                    elif (key == b"M") and (len(buffer) > cur[0] - lng - 1): # right arrow
                        cur[0] += 1
                    elif (key == b"S") and (len(buffer) > cur[0] - lng - 1): # Delete
                        del buffer[cur[0] - lng - 1]

                else: # adding char, updating text
                    try:
                        buffer.insert(cur[0] - lng - 1, key.decode("utf-8"))
                    except: # bytes.fromhex(''.join(list(map(lambda x: hex(x)[2:],range(160, 160+87, 1))))).decode("cp866")
                        buffer.insert(cur[0] - lng - 1, key.decode("cp866"))
                    cur[0] += 1

                stdout.write(f"\x1b[0m\x1b[{fpos[1]};{fpos[0]}H"
                             f"{' ':>{term_size[0] - lng}}" # clearing trash
                             f"\x1b[{fpos[1]};{fpos[0]}H"
                             f"{cfcnt(''.join(buffer))}" # writing changed buffer
                             f"\x1b[{cur[1]};{cur[0]}H")
                
        return ''.join(buffer)
