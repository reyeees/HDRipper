# under construction

import signal
from math import prod
from time import sleep
from threading import Thread
from collections.abc import Generator

class GradientBar:
    def __init__(self, platform, width: int = 80, symbol: str = '━',
                color: tuple[int] = (0, (0, 255), 0), 
                gradient_width: int = 5, framerate: int = 30, 
                double: bool = False, reverse: bool = False) -> None:

        self.width: int = width
        self.symbol: str = symbol
        self.framerate: int = framerate

        self.color: tuple[int] = color
        self.gwidth: int = gradient_width

        self.reverse: bool = reverse
        self.double: bool = double

        self.stop_bar: bool = False
        self.thread: Thread = Thread(target = self.process)

        if len(self.color) < 3:
            raise ValueError("Bro, color shape doesnt match with required one.")
        if self.gwidth < 2:
            raise ValueError("Gradient width is too small.")
        
        self.platform = platform
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

    def linspace(self, start: int, stop: int, num: int) -> Generator[int]:
        step: float = (stop - start) / (num - 1)
        for i in range(num):
            yield int(start + step * i)

    def reshape(self, arr: list, shape: tuple[int, int, int]) -> list[list]:
        """
        Reshape 1d arr into 3d arr.
        """
        if len(shape) != 3:
            raise Exception("Sorry mate, only 3 dimensial sizes.")
        if len(arr) != prod(shape):
            raise AssertionError(f"(Array with ({len(arr)}) can't be reshaped into {', '.join(shape)})")

        return [[[arr[i * shape[1] * shape[2] + j * shape[2] + k]
                    for k in range(shape[2])]
                    for j in range(shape[1])]
                    for i in range(shape[0])]
    
    def merge(self, arr: list, brr: list, crr: list) -> Generator[list[list]]:
        """
        Merging 3 arrays into one 3d array
        """
        if len(arr) != len(brr) or len(brr) != len(crr) or len(arr) != len(crr):
            raise Exception(f"Bro, sizes is not equal ({len(arr)},{len(brr)},{len(crr)})")
        for id in range(0, len(arr), 1):
            yield [arr[id], brr[id], crr[id]]

    def get_gradient(self) -> list[list[int]]:
        arr: list[list[int]] = list(self.merge(*[
            [ch for _ in range(0, self.gwidth, 1)] if type(ch) == int else \
             list(self.linspace(ch[0], ch[1], self.gwidth))
            for ch in self.color
        ]))

        if self.reverse:
            arr = arr[::-1]
        if self.double:
            arr = [*arr, *arr[::-1]]

        return arr * (self.width // len(arr) + 1)

    def start(self) -> "GradientBar":
        self.stop_bar = False
        self.thread.start()
        return self

    def stop(self, *args, end: str = "\n") -> "GradientBar":
        self.stop_bar = True
        print(end = end)
        if args != ():
            exit(args[0])
        return self
    
    def timer(self, time: float, end: str = "\n") -> "GradientBar":
        self.start()
        sleep(time)
        self.stop(end = end)
        return self

    def process(self) -> None:
        gradient: list[int] = self.get_gradient()
        cur_pos: tuple[int] = self.platform.getcur()
        while not self.stop_bar:
            if not self.reverse:
                gradient = [gradient[-1], *gradient[:-1]]
            else:
                gradient = [*gradient[1:], gradient[0]]
            
            temp = ''.join(map(lambda rgb: "\x1b[38;2;{};{};{}m{}\x1b[0m".format(*rgb, self.symbol), gradient[:self.width]))
            print(temp, end = "\x1b[{};{}H".format(*cur_pos[::-1]), flush = True)
            sleep(1 / self.framerate)


if __name__ == "__main__":
    from sys import platform

    if platform == "win32":
        from _win import WinTUI as _TUI
    else:
        from _unix import UnixTUI as _TUI

    bar = GradientBar(_TUI(), 57, '╱', ((0, 127), (0, 127), 0), 40, 60, False, False)
    bar.start()
    sleep(2)
    bar.stop()

    print("Hello ", end = '', flush = True)
    bar = GradientBar(_TUI(), 51, '━', (0, (25, 255), (25, 255)), 50, 30, True, False)
    bar.start()
    sleep(2)
    bar.stop()

    print(' ' * 50, "World!", end = "\r", flush = True)
    bar = GradientBar(_TUI(), 50, '═', (0, (127, 255), 0), 5, 20, True, True)
    bar.start()
    sleep(3)
    bar.stop()

    bar = GradientBar(_TUI(), 57, '╱', ((0, 255), (0, 255), (0, 255)), 57, 60, False, True)
    bar.start()
    sleep(2)
    bar.stop()

    from sys import argv
    if len(argv) > 1:
        from os import system, name
        system("cls" if name == 'nt' else 'clear')

        fshit = [GradientBar(_TUI(), 40, '╱', (0, (127, 255), 0), 5, 60, True, False) for _ in range(5)]
        for shit in fshit:
            shit.start()
            print()
            sleep(0.01)
        sleep(5)
        [shit.stop() for shit in fshit]
