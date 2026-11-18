"""Terminal styling, ANSI colors, and themes."""

import os

# Makes ANSI colors work in older Windows consoles (harmless elsewhere)
if os.name == 'nt':
    os.system('')


class ThemeManager:
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
            # Banner gradient: crimson -> orange -> gold
            "gradient": [124, 160, 196, 202, 208, 214, 220, 226, 227, 229],
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
            "shadow": 28,                    # Banner shadow (dark green)
            # Banner gradient: forest -> neon -> lime
            "gradient": [22, 28, 34, 40, 46, 47, 83, 119, 155, 191],
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
            "shadow": 61,                    # Banner shadow (dusky indigo)
            # Banner gradient: violet -> blue -> cyan -> ice
            "gradient": [93, 57, 63, 69, 33, 39, 45, 51, 87, 123],
        }
    }

    current_theme_key = "1"

    @classmethod
    def get(cls):
        return cls.THEMES[cls.current_theme_key]

    @classmethod
    def set_theme(cls, key: str) -> bool:
        if key in cls.THEMES:
            cls.current_theme_key = key
            return True
        return False

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    # ---------- Optional helpers (use them anywhere in your menus) ----------

    @classmethod
    def gradient_text(cls, text: str, bold: bool = True) -> str:
        """Return text painted with the current theme's gradient."""
        t = cls.get()
        pal = t["gradient"]
        n = max(len(text) - 1, 1)
        out = []
        for i, ch in enumerate(text):
            code = pal[int(i / n * (len(pal) - 1))]
            out.append(f"\033[{'1;' if bold else ''}38;5;{code}m{ch}")
        return "".join(out) + t["reset"]

    @classmethod
    def divider(cls, width: int = 72, char: str = "━") -> str:
        """A gradient horizontal line, e.g. print(ThemeManager.divider())."""
        return cls.gradient_text(char * width, bold=False)

    @classmethod
    def header(cls, title: str, width: int = 72) -> str:
        """A centered section title between two dividers."""
        t = cls.get()
        return (f"{cls.divider(width)}\n"
                f"{t['accent']}{title.upper().center(width)}{t['reset']}\n"
                f"{cls.divider(width)}")

    # ---------- Banner ----------

    @classmethod
    def banner(cls):
        t = cls.get()
        pal = t["gradient"]
        art = [
            r"  ██████╗ ███████╗██████╗  ██████╗ ████████╗███████╗██████╗ ███╗   ███╗",
            r" ██╔════╝ ██╔════╝██╔══██╗██╔═══██╗╚══██╔══╝██╔════╝██╔══██╗████╗ ████║",
            r" ██║  ███╗█████╗  ██████╔╝██║   ██║   ██║   █████╗  ██████╔╝██╔████╔██║",
            r" ██║   ██║██╔══╝  ██╔══██╗██║   ██║   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║",
            r" ╚██████╔╝███████╗██║  ██║╚██████╔╝   ██║   ███████╗██║  ██║██║ ╚═╝ ██║",
            r"  ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝",
        ]
        width = max(len(line) for line in art)
        span = width + len(art) * 3  # diagonal sweep: color shifts across AND down

        print()
        for row, line in enumerate(art):
            out, last = [], None
            for col, ch in enumerate(line):
                if ch == " ":
                    out.append(ch)
                    continue
                if ch == "█":   # solid letter body -> diagonal gradient
                    code = pal[int((col + row * 3) / span * (len(pal) - 1))]
                    color = f"\033[1;38;5;{code}m"
                else:           # box-drawing edges -> shadow for depth
                    color = f"\033[38;5;{t['shadow']}m"
                if color != last:
                    out.append(color)
                    last = color
                out.append(ch)
            print("".join(out) + t["reset"])

        tagline = ">>> LABORATORY EQUIPMENT BORROWING MANAGEMENT SYSTEM <<<"
        print(cls.divider(width))
        print(f"{t['tagline']}{tagline.center(width)}{t['reset']}")
        print(cls.divider(width))
        print()
