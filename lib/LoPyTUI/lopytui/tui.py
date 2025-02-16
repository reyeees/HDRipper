from .lib import _TUI
from .lib.widgets import GradientBar, RunningText, Palens

class TUI:
    def __init__(self) -> None:
        self.platform = _TUI()

    # def __play_gradient(self, x: int, y: int, chars = "0123456789ABCDEF", 
    #                 radius: float = 0.7, size: tuple[int] = (70, 25)) -> None:
    #     height: int = 4
    #     width = len(chars)

    #     for y1 in range(-y, size[1] - y, 1):
    #         for x1 in range(-x, size[0] - x, 1):
    #             end = int((y1*y1*height+x1*x1)**radius*width/size[0])
    #             char = chars[min(width-1, end)]
    #             color = (round(255*abs(x1)/(size[0]-1)),
    #                     round(255*abs(y1)/(size[1]-1)), 150)
    #             print("\x1b[38;2;{};{};{}m{}\x1b[0m".format(*color, char), end = '', flush = True)
    #         print()

    def palens(self, fps: int = 30, step: int = 2) -> None:
        Palens(self.platform, fps, step).init()

    def gradient_bar(self, width: int = 80, symbol: str = '━',
                color: tuple[int] = (0, (0, 255), 0), 
                gradient_width: int = 5, framerate: int = 30, 
                double: bool = False, reverse: bool = False) -> GradientBar:
        """
        GradientBar - An animated gradient bar with configuration
        """
        return GradientBar(self.platform, width, symbol, color, gradient_width, 
                           framerate, double, reverse)

    def running_text(self, text: str, space: int = 30, framerate: int = 30) -> RunningText:
        """
        To create floating running text
        """
        return RunningText(self.platform, text, space, framerate)

    def hide_cursor(self) -> None:
        """
        To hide terminal cursor
        """
        self.platform.hidecur()

    def show_cursor(self) -> None:
        """
        To show terminal cursor
        """
        self.platform.showcur()

    def choose(self, data: list, style: callable) -> int:
        """
        User selecting tool.
        data: list of something, need the __repr__ function for *fancy* being
        style: Selecting style. It can be.. table, dwm, boxes, arrow
        """
        return self.platform.choose(list(map(str, data)), style)

    def get_terminal_size(self) -> tuple[int]:
        """
        To get terminal size
        """
        return self.platform.terminal_size()

    def get_cursor(self) -> tuple[int]:
        """
        To get terminal cursor position
        """
        return self.platform.getcur()

    def input(self, prompt: str, cfcnt: callable) -> str:
        """
        Advanced user input tool
        prompt: Prompt text, appearing in the beginning
        cfcnt: buffer ̶c̶o̶n̶t̶r̶o̶l cooking function, the return value is displayed.
        """
        return self.platform.input(prompt, cfcnt)
