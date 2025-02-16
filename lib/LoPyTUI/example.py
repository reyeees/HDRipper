from time import sleep

from lopytui.tui import TUI
from lopytui.styles import Choose
# from lopytui.lib import _TUI
# from lopytui.lib.widgets import GradientBar, RunningText, Palens


tui = TUI()
raw_tui = tui.platform # or _TUI()


# Hide cursor
tui.hide_cursor()


# Show cursor
tui.show_cursor()


# Get cursor position in terminal (XY)
cur_pos = tui.get_cursor()
print("Cursor position:", cur_pos)


# Get size of terminal screen
buff_size = tui.get_terminal_size()
print("Terminal size:", buff_size)


# Selecting element from array
arr = [0, 561, 361, "tt", (3), {1: 3}]
idx = tui.choose(arr, Choose.dwm)
print(idx, arr[idx])


# Running text
run_text = tui.running_text("Hello", 30, 30) # Or RunningText
run_text.timer(2)
run_text.text = "World!"
run_text.start()
sleep(1)
run_text.stop()


# Gradient bar
grad = tui.gradient_bar(80, "-", (0, (127, 255), 0), 5, 30, False, False) # Or GradientBar
grad.timer(2)
# ^-- Also supports .start() and .stop()


# Interactive user input
def input_control(text: str) -> str:
    return list(map(lambda x: chr(ord(x) + 13), text))

text = tui.input("Input text here > ", input_control)
print(text)

# Fun
tui.palens(30, 2)
