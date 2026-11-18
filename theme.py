"""Terminal styling, ANSI colors, and themes."""

import os

class ThemeManager:
    THEMES = {
        "1": {
            "name": "Classic Amber CRT",
            "primary": "\033[38;5;214m",   # Amber / Orange
            "secondary": "\033[38;5;220m", # Yellow-amber
            "accent": "\033[1;37m",        # Bold white
            "muted": "\033[38;5;244m",     # Dim grey
            "error": "\033[1;31m",         # Red
            "success": "\033[1;32m",       # Green
            "reset": "\033[0m"
        },
        "2": {
            "name": "Retro Green Terminal",
            "primary": "\033[38;5;46m",    # Bright green
            "secondary": "\033[38;5;120m", # Light green
            "accent": "\033[1;37m",        # Bold white
            "muted": "\033[38;5;240m",     # Dark grey
            "error": "\033[1;31m",         # Red
            "success": "\033[1;32m",       # Green
            "reset": "\033[0m"
        },
        "3": {
            "name": "Cyber Blue Matrix",
            "primary": "\033[38;5;45m",    # Cyan / Neon blue
            "secondary": "\033[38;5;111m", # Sky blue
            "accent": "\033[1;37m",        # Bold white
            "muted": "\033[38;5;243m",     # Grey
            "error": "\033[1;31m",         # Red
            "success": "\033[1;32m",       # Green
            "reset": "\033[0m"
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
        print(f"{t['primary']}")
        print(r"""
  ██████╗ ███████╗██████╗  ██████╗ ████████╗███████╗██████╗ ███╗   ███╗
 ██╔════╝ ██╔════╝██╔══██╗██╔═══██╗╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
 ██║  ███╗█████╗  ██████╔╝██║   ██║   ██║   █████╗  ██████╔╝██╔████╔██║
 ██║   ██║██╔══╝  ██╔══██╗██║   ██║   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║
 ╚██████╔╝███████╗██║  ██║╚██████╔╝   ██║   ███████╗██║  ██║██║ ╚═╝ ██║
  ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝
        >>> LABORATORY EQUIPMENT BORROWING MANAGEMENT SYSTEM <<<
        """)
        print(f"{t['reset']}")
