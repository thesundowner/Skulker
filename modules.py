# (C) 2023 BIGG SMOKE
"""
needed imports and macros for the app to function

imageData is a module so it's not imported here b/c it needs this file's import statments
"""

import os # file size and other
from tkinter import Menu, StringVar, TkVersion, filedialog,messagebox #gui and file dialog elts
import customtkinter as ctk # base gui classes
import platform #get python version
import webbrowser as wb # externaal http link to navigate using browser
import pyperclip # copy & paste functions

# encryption
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import  PBKDF2


# macros

WM_ICON_PATH ="icons\\wm_icon1.ico"
WM_WIDTH = 800
WM_HEIGHT = 400
WM_SIZE = f"{WM_WIDTH}x{WM_HEIGHT}"
INJECT_START_OFFSET = 'FFD9' 
END_INJECT_HEADER = 'FFDF'
TEXT_MAX_CHAR = 1024
SALT = b'\xf9}\xc7\x86\x88\xb5K\xec:\xedf\x97`\xfe3\x9cRv\xf09\xa3\xb8Y),\xb6i\xdaS\x0f\xf4\x9e'


VERSION_MAJOR = 2
VERSION_MINOR = 1
VERSION_PATCH = 0
READY_FOR_PRODUCTION = False


# shared functions


def preview_image(path):
        messagebox.showinfo(title="Skulker",message="Now you'll be redirected to an external app.")
        os.system(f'start app\\Imagine_1.3.1_Unicode\\imagine.exe "{path}" ')


def show_help():
        messagebox.showinfo(title="Skulker",message="Now you'll be redirected to an external website.")
        wb.open("https://thesundowner12.github.io")
