# under construction

from threading import Thread
from time import sleep, time, timezone, localtime, altzone
from colorsys import hls_to_rgb
# from random import choice

class ProgressBar:
    def __init__(self, width: int = 20, colors: bool = True, symbols: str = " #") -> None:
        if not symbols.startswith(' '):
            symbols = ''.join([' ', symbols])

        self.width: int = width
        self.colors: list[tuple[int]] = [hls_to_rgb(v / 256, 0.5, 1.0) for v in range(256)]

        self.finished: bool = False
        self.thread = Thread(target = self.process)

    def begin(self) -> None:
        pass

    def finish(self) -> None:
        pass

    def update(self) -> None:
        pass

    def process(self) -> None:
        pass

class App:
    def __init__(self) -> None:
        self.bar_length = 20
        self.symbols_s = [
            " ▏▎▍▌▋▊▉█",
            " ⡀⡄⡆⡇⣇⣧⣷⣿",
            " ░▒▓█",
            " ▁▂▃▄▅▆▇█",
            " ○◔◑◕●",
            " ◷◶◵◴◵◶○",
            " ◑◒◐◓◐◒●",
            " ⎺⎻⎼⎽⎼⎻",
            " ⎺⎻⎼⎽▁▂▃▄▅▆▇█",
            " ⎺⎻⎼⎽▁▂▃▄▅▆▇█▉▊▋▌▍▎▏+"
        ]

        self.support_colors = True
        self.symbols = None
        # self.symbols_list = None # self.set_pairs(self.symbols)
        self.timezone = (timezone if (localtime().tm_isdst == 0) else altzone) / 60 / 60 * -1
        self.colors = [hls_to_rgb(i / 256, 0.5, 1.0) for i in range(0, 256, 1)]
        self.bar = ""

        self.color_pointer = 120
        self.color_step = 1

    def get_time(self, timestamp: float) -> str:
        return "{:0>2}:{:0>2}:{:0>2}.{:0>3}".format(
            int((timestamp / 60 / 60 % 24) + self.timezone), 
            int(timestamp / 60 % 60), 
            abs(int(timestamp % 60)), 
            int(str(timestamp).split('.')[-1]) % 1000
        )

    def lost_time(self, a: float, b: float) -> str:
        a = [float(i) for i in self.get_time(a).split(":")]
        b = [float(i) for i in self.get_time(b).split(":")]
        c = [b[i] - a[i] for i in range(0, 3, 1)]
        return "{:0>2}:{:0>2}:{:0>2}.{:0>3}".format(
            int(c[0]), int(c[1]), str(c[2]).split('.')[0],
            str(c[2]).split('.')[1][0:3]
        )

    def action(self, color: list[int] = None, sleep_: float = 0.01) -> bool:
        if self.bar.count(self.symbols[-1]) == self.bar_length:
            return True

        if color != None:
            color = [int(i * 255) for i in color]
            self.bar += f"\x1b[38;2;{color[0]};{color[1]};{color[2]}m "
        else:
            self.bar += " "
        for char in self.symbols:
            sleep(sleep_)
            self.bar = ''.join([self.bar[:-1], char])
            print(f"|{self.bar.ljust(self.bar_length * len(self.symbols) // 2)}| {self.get_time(time())}", end = "\r", flush = True)

        return False

    def main(self) -> None:
        start = time()
        print("\x1b[?25l", end = "", flush = True)

        for symbs in self.symbols_s:
            self.symbols = symbs
            self.symbols_list = self.symbols
            if self.support_colors:
                for color in self.colors[self.color_pointer:]:
                    if self.action(color):
                        break
            else:
                while True:
                    if self.action():
                        break
            self.bar = ""
            print(f"\x1b[{self.bar_length + 1}C - {self.symbols}", end = "\n", flush = True)

            self.color_pointer += self.color_step
            if self.color_pointer == 255:
                self.color_pointer = 0
        end = time()
        print(f"\x1b[?25h\x1b[0m\n\nstart time: {self.get_time(start)}\n  end time: {self.get_time(end)}\n lost time: {self.lost_time(start, end)}", flush = True)

if __name__ == "__main__":
    App().main()
    # a = ProgressBar().begin()
    # a.update()
    # a.finish()
