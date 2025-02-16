import os
import fcntl
import struct
import termios
import tty
from re import match as re
from sys import stdin, stdout


class UnixTUI:
    """
    Under construction and something wont work properly
    Huh, bcz im writing it on shitty windows
    """
    def __init__(self) -> None:
        self.fd = os.open(os.ttyname(0), os.O_RDONLY)

    def hidecur(self) -> None:
        stdout.write("\x1b[?25l")

    def showcur(self) -> None:
        stdout.write("\x1b[?25h")

    def choose(self, data: list, style: str) -> int:
        """
        User choosing tool (Unix)
        """
        ind = 0
        self.hidecur()
        pos = self.getcur()
        buffer = style(pos, data, ind)
        print(buffer, end = '', flush = True)

        old_settings = termios.tcgetattr(self.fd)
        tty.setraw(self.fd)
        try:
            while True:
                char = stdin.read(1)

                if char == "\r": # enter
                    print(f"\x1b[{pos[1]-1};{pos[0]}H")
                    break

                elif char == "\x1b":
                    sym = stdin.read(2)
                    if sym[-1] == "1": #   #[1;5A ctrl + arrow, [1;6A ctrl + shift + arrow
                        sym = ''.join([sym, stdin.read(3)])
                    elif sym[-1] == "3":
                        stdin.read(1)
                    elif sym[-1] not in ['D', 'A', 'B', 'C']:
                        continue
                    
                    key = sym[-1]
                    if key == "A" and ind > 0:
                        ind -= 1
                    if key == "B" and ind < len(data) - 1:
                        ind += 1
                
                buffer = style(pos, data, ind)

                print(buffer, end = '', flush = True)
        finally:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, old_settings)
            self.showcur()
        return ind

    def terminal_size(self) -> None:
        try:
            res = fcntl.ioctl(self.fd, termios.TIOCGWINSZ, b"\x00" * 4)
        except IOError as e:
            raise OSError(e)
        lines, columns = struct.unpack("hh", res)
        return (columns, lines)

    def getcur(self) -> tuple[int]:
        """
        Get cursor position (*nix)
        """
        OldStdinMode = termios.tcgetattr(stdin)
        _ = termios.tcgetattr(stdin)
        _[3] = _[3] & ~(termios.ECHO | termios.ICANON)
        termios.tcsetattr(stdin, termios.TCSAFLUSH, _)

        try:
            _ = ""
            stdout.write("\x1b[6n")
            stdout.flush()
            while not (_ := _ + stdin.read(1)).endswith('R'):
                True
            res = re(r".*\[(?P<y>\d*);(?P<x>\d*)R", _)
        finally:
            termios.tcsetattr(stdin, termios.TCSAFLUSH, OldStdinMode)

        if res:
            return tuple(map(int, (res.group("x"), res.group("y"))))
        return (-1, -1)

    def input(self, prompt: str, cfcnt: callable) -> str:
        """
        Input function for *nix. Under construction.
        prompt: string
        cfcnt: recycling control function
        """

        buffer = []
        lng = stdout.write(prompt)
        cur = [lng + 1, self.getcur()[1]]
        fpos = cur.copy()

        term_size = self.terminal_size()
        
        old_settings = termios.tcgetattr(self.fd)
        tty.setraw(self.fd)

        try:
            while True:
                char = stdin.read(1)
                if char == '\r': # return
                    stdout.write("\r\n")
                    break

                elif char == "\x7f": # backspace
                    if fpos[0] < cur[0]:
                        del buffer[cur[0] - lng - 2]
                        cur[0] -= 1
                
                elif char == "\x08": # ctrl + backspace
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
                
                elif char == "\x1b":
                    sym = stdin.read(2)
                    if sym[-1] == "1": #   #[1;5A ctrl + arrow, [1;6A ctrl + shift + arrow
                        sym = ''.join([sym, stdin.read(3)])
                    elif sym[-1] == "3":
                        stdin.read(1)
                    elif sym[-1] not in ['D', 'A', 'B', 'C']:
                        continue
                    
                    key = sym[-1]
                    if (key == "D") and (fpos[0] < cur[0]): # left arrow
                        cur[0] -= 1
                    elif (key == "C") and (len(buffer) > cur[0] - lng - 1): # right arrow
                        cur[0] += 1
                    elif (key == "3") and (len(buffer) > cur[0] - lng - 1): # delete
                        del buffer[cur[0] - lng - 1]
                else:
                    buffer.insert(cur[0] - lng - 1, char)
                    cur[0] += 1
                
                stdout.write(f"\x1b[0m\x1b[{fpos[1]};{fpos[0]}H"
                             f"{' ':>{term_size[0] - lng}}" # clearing trash
                             f"\x1b[{fpos[1]};{fpos[0]}H"
                             f"{cfcnt(''.join(buffer))}" # writing changed buffer
                             f"\x1b[{cur[1]};{cur[0]}H")
                stdout.flush()
        finally:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, old_settings)
        return ''.join(buffer)
