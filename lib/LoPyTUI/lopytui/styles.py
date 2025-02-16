from .tui import _TUI

class Choose:
    @staticmethod
    def dwm(pos: tuple[int], data: str, index: int) -> str:
        """
        Example: # Simple, minimalistic, suckless
          123 ███ 789
              (choosed 456, just changed fg color)
        """
        buffer = ""
        selected = "\x1b[37;44m{}\x1b[0m".format

        for id in range(0, len(data), 1):
            buffer = ' '.join([
                buffer, 
                selected(data[id]) if id == index else data[id]
            ])
        return '\n'.join([buffer, f"\x1b[{pos[1]-buffer.count('\n')-1};{pos[0]}H"]).strip()
    
    @staticmethod
    def dwm_vertical(pos: tuple[int], data: str, index: int) -> str:
        """
        Example: # Simple, minimalistic, suckless
          123
          ███
          789 (choosed 456, just changed fg color)
        """
        buffer = ""
        selected = "\x1b[37;44m{}\x1b[0m".format
        for id in range(0, len(data), 1):
            buffer = '\n'.join([
                buffer, 
                selected(data[id]) if id == index else data[id]
            ])
        return '\n'.join([buffer, f"\n\x1b[{pos[1]-buffer.count('\n')-1};{pos[0]}H"]).strip()

    @staticmethod
    def table(pos: tuple[int], data: str, index: int) -> str:
        """
        Example: # Perfect for some small elements
         +-----+
         | 123 |
         +-----+
        >> 456 <<
         +-----+
         | 789 |
         +-----+
        """
        _temp = map(len, data)
        sze = 0 if max(_temp) == min(_temp) else max(_temp)
        print(f"\x1b[{pos[0]+1}G", end = '', flush = True)

        buffer = ""
        selected = " +{a:{a}>{l}}+\n>> {b} <<\n +{a:{a}>{l}}+".format
        unselected = " +{a:{a}>{l}}+\n | {b} | \n +{a:{a}>{l}}+".format

        for id in range(0, len(data), 1):
            buffer = '\n'.join([
                buffer, 
                selected(a = '-', l = sze + 2, b = data[id].center(sze)) \
                    if id == index else \
                unselected(a = '-', l = sze + 2, b = data[id].center(sze))
            ])
        return '\n'.join([buffer, f"\n\x1b[{pos[1]-buffer.count('\n')-1};{pos[0]+1}H"]).strip()

    @staticmethod
    def block(pos: tuple[int], data: str, index: int) -> str:
        """
        Example: # Minecraft lol
        ▗▄▄▄▄▄▖
        ▌ 123 ▐
        ▝▀▀▀▀▀▘
        ▟▀▀▀▀▀▙
        ▌ 456 ▐
        ▜▄▄▄▄▄▛
        ▗▄▄▄▄▄▖
        ▐ 789 ▌
        ▝▀▀▀▀▀▘
        """
        _temp = map(len, data)
        sze = 0 if max(_temp) == min(_temp) else max(_temp)

        buffer = ""
        selected = "▟{a:{a}>{l}}▙\n▌ {b} ▐\n▜{c:{c}>{l}}▛".format
        unselected = "▗{a:{a}>{l}}▖\n▌ {b} ▐\n▝{c:{c}>{l}}▘".format

        for id in range(0, len(data), 1):
            buffer = '\n'.join([
                buffer, 
                selected(a = '▀', c = '▄', l = sze + 2, b = data[id].center(sze)) \
                    if id == index else \
                unselected(a = '▄', c = '▀', l = sze + 2, b = data[id].center(sze))
            ])
        return '\n'.join([buffer, f"\n\x1b[{pos[1]-buffer.count('\n')-1};{pos[0]}H"]).strip()

    @staticmethod
    def arrow(pos: tuple[int], data: str, index: int) -> str:
        """
        Example: # Classic
        123>
        456 <--
        789>
        """
        buffer = ""
        selected = "{} <--".format
        unselected = "{}>   ".format
        for id in range(0, len(data), 1):
            buffer = '\n'.join([
                buffer, 
                selected(data[id]) if id == index else unselected(data[id])
            ])
        return '\n'.join([buffer, f"\n\x1b[{pos[1]-buffer.count('\n')-1};{pos[0]}H"]).strip()
