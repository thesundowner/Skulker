# (C) 2023 BIG SMOKE

# imports:
import os
import customtkinter as ctk
import platform
import webbrowser as wb
import pyperclip
from tkinter import Menu, StringVar, TkVersion, filedialog, messagebox
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from hashlib import sha256

TEXTFONT = ("Consolas" , 13)

if int(platform.win32_ver()[1].split(".")[2]) <= 22621:
    ctk.set_default_color_theme("theme11.json")
else:
    ctk.set_default_color_theme("theme10.json")


# WM_ICON_PATH ="icons\\wm_icon1.ico" unused.
WM_WIDTH = 550
WM_HEIGHT = 350
WM_SIZE = f"{WM_WIDTH}x{WM_HEIGHT}"
INJECT_START_OFFSET = "FFD9"
END_INJECT_HEADER = "FFDF"
TEXT_MAX_CHAR = 8192


VERSION_MAJOR = 2
VERSION_MINOR = 4
VERSION_PATCH = 0
VERSION_STR = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}"
READY_FOR_PRODUCTION = False


def preview_image(path):
    messagebox.showinfo(
        title="Skulker", message="Now you'll be redirected to an external app."
    )
    os.system(f'start imagine.exe "{path}" ')


def show_help():
    messagebox.showinfo(
        title="Skulker", message="Now you'll be redirected to an external website."
    )
    wb.open("https://thesundowner12.github.io")


def show_warning(state):
    if not state:
        messagebox.showwarning(
            title="Skulker",
            message=f"Please note that this version ({VERSION_STR}) might be unstable.\nProceed with caution.\n\n-From the dev.",
        )
    else:
        pass
