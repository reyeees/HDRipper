import signal
from time import sleep
from threading import Thread


class RunningText:
    def __init__(self, platform, text: str, space: int = 30, framerate: int = 60) -> None:
        self.reverse: bool = False
        if framerate < 0:
            self.reverse = True

        self.text: str = text
        self.space: int = space
        self.framerate: float = 1 / abs(framerate)
        self.stop_process: bool = False
        self.thread: Thread = Thread(target = self.process)

        self.platform = platform

        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

    def start(self) -> "RunningText":
        self.stop_process = False
        self.thread = Thread(target = self.process, args = (self.text, self.space))
        self.thread.start()
        return self

    def stop(self, *args, end: str = "\n") -> "RunningText":
        self.stop_process = True
        print(end = end)
        if args != ():
            exit(args[0])
        return self
    
    def timer(self, time: float, end: str = "\n") -> "RunningText":
        self.start()
        sleep(time)
        self.stop(end = end)
        return self

    def process(self, text: str, space: int = 30) -> None:
        text = text.ljust(space)
        cur_pos: tuple[int] = self.platform.getcur()
        while not self.stop_process:
            if self.reverse:
                text = ''.join([text[-1], text[:-1]])
            else:
                text = ''.join([text[1:], text[0]])
            print(text, end = "\x1b[{};{}H".format(*cur_pos[::-1]), flush = True)
            sleep(self.framerate)


if __name__ == "__main__":
    from sys import platform

    if platform == "win32":
        from _win import WinTUI as _TUI
    else:
        from _unix import UnixTUI as _TUI

    floattext = RunningText(_TUI(), 30)
    floattext.start("Hello, world", 30)
    sleep(5)
    floattext.stop()
    print()
    
