"""Terminal styling, ANSI colors, and themes."""

import os

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
            # Banner gradient (top -> bottom): red -> orange -> yellow
            "gradient": [196, 202, 208, 214, 220, 226],
            "tagline": "\033[1;38;5;230m",
        },
        "2": {
            "name": "Retro Green Terminal",
            "primary": "\033[1;38;5;47m",     # Neon green
            "secondary": "\033[38;5;157m",   # Pale mint
            "accent": "\033[1;38;5;231m",    # Bold bright white
            "muted": "\033[38;5;65m",        # Moss grey-green
            "error": "\033[1;38;5;210m",     # Soft salmon red
            "success": "\033[1;38;5;118m",   # Lime green
            "reset": "\033[0m",
            # Banner gradient: deep green -> lime
            "gradient": [28, 34, 40, 46, 82, 118],
            "tagline": "\033[1;38;5;157m",
        },
        "3": {
            "name": "Cyber Blue Matrix",
            "primary": "\033[1;38;5;51m",     # Electric cyan
            "secondary": "\033[38;5;147m",   # Soft periwinkle
            "accent": "\033[1;38;5;231m",    # Bold bright white
            "muted": "\033[38;5;103m",       # Slate lavender grey
            "error": "\033[1;38;5;204m",     # Neon pink-red
            "success": "\033[1;38;5;86m",    # Aqua green
            "reset": "\033[0m",
            # Banner gradient: violet -> blue -> cyan
            "gradient": [93, 63, 33, 39, 45, 51],
            "tagline": "\033[1;38;5;159m",
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

    @classmethod
    def banner(cls):
        t = cls.get()
        art = [
            r"  ██████╗ ███████╗██████╗  ██████╗ ████████╗███████╗██████╗ ███╗   ███╗",
            r" ██╔════╝ ██╔════╝██╔══██╗██╔═══██╗╚══██╔══╝██╔════╝██╔══██╗████╗ ████║",
            r" ██║  ███╗█████╗  ██████╔╝██║   ██║   ██║   █████╗  ██████╔╝██╔████╔██║",
            r" ██║   ██║██╔══╝  ██╔══██╗██║   ██║   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║",
            r" ╚██████╔╝███████╗██║  ██║╚██████╔╝   ██║   ███████╗██║  ██║██║ ╚═╝ ██║",
            r"  ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝",
        ]
        print()
        for line, code in zip(art, t["gradient"]):
            print(f"\033[1;38;5;{code}m{line}{t['reset']}")
        print(f"{t['tagline']}        >>> LABORATORY EQUIPMENT BORROWING MANAGEMENT SYSTEM <<<{t['reset']}")
        print()
