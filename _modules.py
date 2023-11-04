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
import http.server
import webview

ctk.set_default_color_theme("themes/theme.json")


# WM_ICON_PATH ="icons\\wm_icon1.ico" unused.
WM_WIDTH = 800
WM_HEIGHT = 400
WM_SIZE = f"{WM_WIDTH}x{WM_HEIGHT}"
INJECT_START_OFFSET = "FFD9"
END_INJECT_HEADER = "FFDF"
TEXT_MAX_CHAR = 2048
ENC_SALT = b"\x03\xab\x12K\xc9\xe7\x14\xec\xf0_\x1f4\xf9\xfc\x91\x08y\x81U\xcd\\\xc7\xe0(\xfd\xd9T\xba\xc6\xac!\xa8"


VERSION_MAJOR = 2
VERSION_MINOR = 2
VERSION_PATCH = 0
VERSION_STR = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}"
READY_FOR_PRODUCTION = True


def preview_image(path):
    messagebox.showinfo(
        title="Skulker", message="Now you'll be redirected to an external app."
    )
    os.system(f'start app\\Imagine_1.3.1_Unicode\\imagine.exe "{path}" ')


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
