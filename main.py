#!/usr/bin/env python3
import sys
import os

os.environ.setdefault("PYTHONPATH", os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk
from app.principal import PrimeToolXLinux

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = PrimeToolXLinux()
    app.mainloop()

if __name__ == "__main__":
    main()