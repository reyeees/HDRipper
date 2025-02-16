# under construction

from colorsys import hls_to_rgb
from time import sleep
from sys import stdout

class Palens:
    def __init__(self, platform, fps: int = 30, step: int = 2) -> None:
        self.step = step
        self.trgb = lambda bd, h: hls_to_rgb(h * self.step / 255, 0.3 if bd else 0.5, 1.0)
        self.rgb = lambda r,g,b: f"\x1b[38;2;{round(r*255)};{round(g*255)};{round(b*255)}m"
        self.clr = "\x1b[0m"
        self.frame_duration = 1 / abs(fps)
        self.frame = "{cur}{a}\u2584{b}\u2584{c}\u2584{d}\u2584{e}\n" \
                     "{b}\u2588{c}\u2588{d}\u2588{e}\u2588{f}\u2588{g}\u258c\n" \
                     "{c}\u2588{d}\u2588{e}\u2588{f}\u2588{g}\u2588{h}\u258c\n" \
                     "{d}\u259d{e}\u2580{f}\u2580{g}\u2580{h}\u2580{i}\u2580\x1b[0m".format
        # self.shadow_map: list[int] = (
        #     0, 0, 0, 0,
        #     0, 0, 0, 0, 1,
        #     0, 0, 0, 0, 1,
        #     1, 1, 1, 1, 1
        # )

        self.platform = platform
        self.stop_process: bool = False

    # def generate_frame(self, hue: int) -> str:
    #     return self.frame(
    #         cur = "\x1b[{};{}H".format(*self.platform.getcur()[::-1]),
    #         a = self.rgb(*self.trgb(1, hue)),
    #         b = self.rgb(*self.trgb(1, hue + 1)),
    #         c = self.rgb(*self.trgb(1, hue + 2)),
    #         d = self.rgb(*self.trgb(1, hue + 3)),
    #         e = self.rgb(*self.trgb(1, hue + 4)),
    #         f = self.rgb(*self.trgb(1, hue + 5)),
    #         g = self.rgb(*self.trgb(1, hue + 6)),
    #         h = self.rgb(*self.trgb(1, hue + 7)),
    #         i = self.rgb(*self.trgb(1, hue + 8))
    #     )

    def init(self) -> None:
        while not self.stop_process:
            for h in range(0, 256, 9):
                data = "\x1b[s" \
    f"{self.rgb(*self.trgb(0, h))}\u2584{self.rgb(*self.trgb(0, h + 1))}\u2584{self.rgb(*self.trgb(0, h + 2))}\u2584{self.rgb(*self.trgb(0, h + 3))}\u2584{self.rgb(*self.trgb(0, h + 4))}\u2584{self.clr}\n" \
    f"{self.rgb(*self.trgb(0, h + 1))}\u2588{self.rgb(*self.trgb(0, h + 2))}\u2588{self.rgb(*self.trgb(0, h + 3))}\u2588{self.rgb(*self.trgb(0, h + 4))}\u2588{self.rgb(*self.trgb(0, h + 5))}\u2588{self.clr + self.rgb(*self.trgb(1, h + 6))}\u258c{self.clr}\n" \
    f"{self.rgb(*self.trgb(0, h + 2))}\u2588{self.rgb(*self.trgb(0, h + 3))}\u2588{self.rgb(*self.trgb(0, h + 4))}\u2588{self.rgb(*self.trgb(0, h + 5))}\u2588{self.rgb(*self.trgb(0, h + 6))}\u2588{self.clr + self.rgb(*self.trgb(1, h + 7))}\u258c{self.clr}\n" \
    f"{self.rgb(*self.trgb(1, h + 3))}\u259d{self.rgb(*self.trgb(1, h + 4))}\u2580{self.rgb(*self.trgb(1, h + 5))}\u2580{self.rgb(*self.trgb(1, h + 6))}\u2580{self.rgb(*self.trgb(1, h + 7))}\u2580{self.rgb(*self.trgb(1, h + 8))}\u2598{self.clr}"
                # data = self.generate_frame(hue)
                print(data, end = "\x1b[u", flush = True, file = stdout)
                sleep(self.frame_duration)

if __name__ == "__main__":
    Palens({}).init()

"""
U+2580 	▀ 	Upper half block
U+2581 	▁ 	Lower one eighth block
U+2582 	▂ 	Lower one quarter block
U+2583 	▃ 	Lower three eighths block
U+2584 	▄ 	Lower half block
U+2585 	▅ 	Lower five eighths block
U+2586 	▆ 	Lower three quarters block
U+2587 	▇ 	Lower seven eighths block
U+2588 	█ 	Full block
U+2589 	▉ 	Left seven eighths block
U+258A 	▊ 	Left three quarters block
U+258B 	▋ 	Left five eighths block
U+258C 	▌ 	Left half block
U+258D 	▍ 	Left three eighths block
U+258E 	▎ 	Left one quarter block
U+258F 	▏ 	Left one eighth block
U+2590 	▐ 	Right half block
U+2591 	░ 	Light shade
U+2592 	▒ 	Medium shade
U+2593 	▓ 	Dark shade
U+2594 	▔ 	Upper one eighth block
U+2595 	▕ 	Right one eighth block
U+2596 	▖ 	Quadrant lower left
U+2597 	▗ 	Quadrant lower right
U+2598 	▘ 	Quadrant upper left
U+2599 	▙ 	Quadrant upper left and lower left and lower right
U+259A 	▚ 	Quadrant upper left and lower right
U+259B 	▛ 	Quadrant upper left and upper right and lower left
U+259C 	▜ 	Quadrant upper left and upper right and lower right
U+259D 	▝ 	Quadrant upper right
U+259E 	▞ 	Quadrant upper right and lower left
U+259F 	▟ 	Quadrant upper right and lower left and lower right
"""
