"""Terminal styling, ANSI colors, and themes."""

import os
import re

# Makes ANSI colors work in older Windows consoles (harmless elsewhere)
if os.name == 'nt':
    os.system('')

_ANSI = re.compile(r"\033\[[0-9;]*m")


def _vlen(text: str) -> int:
    """Visible length of a string (ignores color codes)."""
    return len(_ANSI.sub("", text))


class ThemeManager:
    # ------------------------------------------------------------------
    #  THEMES  (colors are 256-color ANSI codes)
    #  "font" = default banner font for the theme (see FONTS below)
    # ------------------------------------------------------------------
    THEMES = {
        "1": {
            "name": "Classic Amber CRT",
            "primary": "\033[1;38;5;208m",   # Vivid sunset orange
            "secondary": "\033[38;5;221m",   # Warm golden yellow
            "accent": "\033[1;38;5;231m",    # Bold bright white
            "muted": "\033[38;5;137m",       # Soft bronze grey
            "error": "\033[1;38;5;203m",     # Coral red
            "success": "\033[1;38;5;114m",   # Soft mint green
            "reset": "\033[0m",
            "info": "\033[38;5;215m",        # Peach
            "warning": "\033[1;38;5;226m",   # Bright yellow
            "border": "\033[38;5;166m",      # Burnt orange
            "tagline": "\033[1;38;5;230m",   # Cream white
            "shadow": 130,                   # Banner shadow (darker orange)
            "gradient": [124, 160, 196, 202, 208, 214, 220, 226, 227, 229],
            "font": "1",                     # Shadow
        },
        "2": {
            "name": "Retro Green Terminal",
            "primary": "\033[1;38;5;47m",    # Neon green
            "secondary": "\033[38;5;157m",   # Pale mint
            "accent": "\033[1;38;5;231m",    # Bold bright white
            "muted": "\033[38;5;65m",        # Moss grey-green
            "error": "\033[1;38;5;210m",     # Soft salmon red
            "success": "\033[1;38;5;118m",   # Lime green
            "reset": "\033[0m",
            "info": "\033[38;5;121m",        # Aqua mint
            "warning": "\033[1;38;5;190m",   # Lemon lime
            "border": "\033[38;5;35m",       # Forest green
            "tagline": "\033[1;38;5;157m",   # Pale mint
            "shadow": 28,                    # Dim green (LED "off" dots / shadow)
            "gradient": [22, 28, 34, 40, 46, 47, 83, 119, 155, 191],
            "font": "3",                     # LED
        },
        "3": {
            "name": "Cyber Blue Matrix",
            "primary": "\033[1;38;5;51m",    # Electric cyan
            "secondary": "\033[38;5;147m",   # Soft periwinkle
            "accent": "\033[1;38;5;231m",    # Bold bright white
            "muted": "\033[38;5;103m",       # Slate lavender grey
            "error": "\033[1;38;5;204m",     # Neon pink-red
            "success": "\033[1;38;5;86m",    # Aqua green
            "reset": "\033[0m",
            "info": "\033[38;5;117m",        # Sky blue
            "warning": "\033[1;38;5;221m",   # Amber
            "border": "\033[38;5;69m",       # Royal blue
            "tagline": "\033[1;38;5;159m",   # Ice blue
            "shadow": 61,                    # Dusky indigo
            "gradient": [93, 57, 63, 69, 33, 39, 45, 51, 87, 123],
            "font": "2",                     # Compact
        }
    }

    # ------------------------------------------------------------------
    #  BANNER FONTS
    #  Note: the *terminal's* typeface is set in your terminal settings.
    #  These are the big title lettering styles drawn by the program.
    # ------------------------------------------------------------------
    FONTS = {
        "1": "Shadow",    # Big 3D block letters
        "2": "Compact",   # Sleek 3-line half-block letters
        "3": "LED",       # Dot-matrix display
    }

    _WORD = "GEROTERM"
    _GLYPHS = {
        "G": [".###.", "#....", "#.###", "#...#", ".###."],
        "E": ["#####", "#....", "####.", "#....", "#####"],
        "R": ["####.", "#...#", "####.", "#..#.", "#...#"],
        "O": [".###.", "#...#", "#...#", "#...#", ".###."],
        "T": ["#####", "..#..", "..#..", "..#..", "..#.."],
        "M": ["#...#", "##.##", "#.#.#", "#...#", "#...#"],
    }
    _SHADOW_ART = [
        r"  ██████╗ ███████╗██████╗  ██████╗ ████████╗███████╗██████╗ ███╗   ███╗",
        r" ██╔════╝ ██╔════╝██╔══██╗██╔═══██╗╚══██╔══╝██╔════╝██╔══██╗████╗ ████║",
        r" ██║  ███╗█████╗  ██████╔╝██║   ██║   ██║   █████╗  ██████╔╝██╔████╔██║",
        r" ██║   ██║██╔══╝  ██╔══██╗██║   ██║   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║",
        r" ╚██████╔╝███████╗██║  ██║╚██████╔╝   ██║   ███████╗██║  ██║██║ ╚═╝ ██║",
        r"  ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝",
    ]

    current_theme_key = "1"
    current_font_key = "auto"   # "auto" = use the theme's default font

    @classmethod
    def get(cls):
        return cls.THEMES[cls.current_theme_key]

    @classmethod
    def set_theme(cls, key: str) -> bool:
        if key in cls.THEMES:
            cls.current_theme_key = key
            return True
        return False

    @classmethod
    def set_font(cls, key: str) -> bool:
        """Pick a banner font: "1" Shadow, "2" Compact, "3" LED, or "auto"."""
        if key == "auto" or key in cls.FONTS:
            cls.current_font_key = key
            return True
        return False

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    # ------------------------------------------------------------------
    #  Helpers you can use anywhere in your menus
    # ------------------------------------------------------------------

    @classmethod
    def gradient_text(cls, text: str, bold: bool = True) -> str:
        """Return text painted with the current theme's gradient."""
        t = cls.get()
        pal = t["gradient"]
        n = max(len(text) - 1, 1)
        out, last = [], None
        for i, ch in enumerate(text):
            code = pal[int(i / n * (len(pal) - 1))]
            if code != last:
                out.append(f"\033[{'1;' if bold else ''}38;5;{code}m")
                last = code
            out.append(ch)
        return "".join(out) + t["reset"]

    @classmethod
    def divider(cls, width: int = 78, char: str = "━") -> str:
        """A gradient horizontal line."""
        return cls.gradient_text(char * width, bold=False)

    @classmethod
    def header(cls, title: str, width: int = 78) -> str:
        """A centered section title between two gradient dividers."""
        t = cls.get()
        spaced = "  ".join(title.upper())
        return (f"{cls.divider(width)}\n"
                f"{t['accent']}{spaced.center(width)}{t['reset']}\n"
                f"{cls.divider(width)}")

    @classmethod
    def status(cls, kind: str, message: str) -> str:
        """Icon + message. kind: success | error | warning | info"""
        t = cls.get()
        icons = {"success": "✔", "error": "✖", "warning": "▲", "info": "●"}
        color = t.get(kind, t["info"])
        return f"{color}{icons.get(kind, '●')}{t['reset']} {t['secondary']}{message}{t['reset']}"

    @classmethod
    def tag(cls, text: str, kind: str = "primary") -> str:
        """A highlighted label, e.g. print(ThemeManager.tag('AVAILABLE', 'success'))."""
        t = cls.get()
        return f"\033[7m{t.get(kind, t['primary'])} {text} {t['reset']}"

    @classmethod
    def panel(cls, title: str, lines, width: int = 0) -> str:
        """A rounded box with a title, e.g. for menus.

        print(ThemeManager.panel("Main Menu", ["[1] Borrow", "[2] Return"]))
        """
        t = cls.get()
        lines = list(lines)
        inner = max([_vlen(title) + 4] + [_vlen(l) for l in lines]) + 2
        inner = max(inner, width - 2)
        b, r = t["border"], t["reset"]
        head = f"{b}╭─ {t['primary']}{title}{r}{b} " + "─" * (inner - _vlen(title) - 3) + f"╮{r}"
        body = [f"{b}│{r} {l}{' ' * (inner - _vlen(l) - 1)}{b}│{r}" for l in lines]
        foot = f"{b}╰" + "─" * inner + f"╯{r}"
        return "\n".join([head] + body + [foot])

    # ------------------------------------------------------------------
    #  Banner
    # ------------------------------------------------------------------

    @classmethod
    def _build_art(cls, font: str):
        """Return the banner lettering as a list of plain-text lines."""
        if font == "1":
            return list(cls._SHADOW_ART)

        gap = 2 if font == "3" else 1
        rows = [(" " * gap).join(cls._GLYPHS[c][r] for c in cls._WORD) for r in range(5)]

        if font == "3":  # LED dot-matrix
            return [row.replace("#", "●").replace(".", "·") for row in rows]

        # Compact: squeeze 5 pixel rows into 3 lines with half-blocks
        rows.append("." * len(rows[0]))
        blocks = {(0, 0): " ", (1, 0): "▀", (0, 1): "▄", (1, 1): "█"}
        art = []
        for r in (0, 2, 4):
            art.append("".join(blocks[(a == "#", b == "#")] for a, b in zip(rows[r], rows[r + 1])))
        return art

    @classmethod
    def _paint(cls, line: str, row: int, width: int, total_rows: int) -> str:
        t = cls.get()
        pal = t["gradient"]
        span = width + total_rows * 3
        out, last = [], None
        for col, ch in enumerate(line):
            if ch == " ":
                out.append(ch)
                continue
            if ch in "█▀▄●":   # solid parts -> diagonal gradient
                code = pal[min(int((col + row * 3) / span * (len(pal) - 1)), len(pal) - 1)]
                color = f"\033[1;38;5;{code}m"
            else:              # edges / "off" dots -> shadow shade for depth
                color = f"\033[38;5;{t['shadow']}m"
            if color != last:
                out.append(color)
                last = color
            out.append(ch)
        return "".join(out) + t["reset"]

    @classmethod
    def banner(cls):
        t = cls.get()
        font = t["font"] if cls.current_font_key == "auto" else cls.current_font_key
        art = cls._build_art(font)

        W = 76  # inside width of the frame
        art_w = max(len(l) for l in art)
        pad = (W - art_w) // 2
        b, r = t["border"], t["reset"]

        def framed(content: str = "", plain_len: int = 0, left: int = 0) -> str:
            right = W - left - plain_len
            return f"{b}│{r}{' ' * left}{content}{' ' * right}{b}│{r}"

        tagline = ">>> LABORATORY EQUIPMENT BORROWING MANAGEMENT SYSTEM <<<"
        sub = f"◆  {t['name']}  ◆"

        print()
        print(cls.gradient_text("╭" + "─" * W + "╮", bold=False))
        print(framed())
        for i, line in enumerate(art):
            print(framed(cls._paint(line, i, art_w, len(art)), len(line), pad))
        print(framed())
        print(framed(f"{t['tagline']}{tagline}{r}", len(tagline), (W - len(tagline)) // 2))
        print(framed(f"{t['muted']}{sub}{r}", len(sub), (W - len(sub)) // 2))
        print(cls.gradient_text("╰" + "─" * W + "╯", bold=False))
        print()
