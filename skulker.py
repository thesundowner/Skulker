from _modules import *
from _cryptor import Enc
from _imagedata import ImageData

WM_TITLE = "Skulker"


ABOUT_STRING = f"""\
{WM_TITLE} - A Steghide-like application
Version {VERSION_STR}
customtkinter {ctk.__version__}
Tkinter {TkVersion}
Python {platform.python_version()}

Uses Imagine - Image & Animation Viewer for Windows
Copyright (c) 2003-2023 Sejin Chun


Copyright (C) 2023  Bigg Smoke / The Lunar Surface


This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


Machine Details:

Windows {platform.win32_ver()[1]} {platform.win32_edition()}
{platform.processor()}
"""

HELP_STRING = f'''\
Skulker Help File

WHAT IS SKULKER?

Skulker is a program that lets you hide information inside jpeg photos.
The program won't alter the image in any way, so your precious family photos 
are safe. If you're fammiliar with Steghide, you'll know what Skulker does.
But the difference between Skulker is that it directly appends the text.

FEATURES

1. Maximum text length of {TEXT_MAX_CHAR} characters
2. UTF-8 support
3. AES + SHA256 Encryption 

Injection is pretty straightforward. Open a .jpeg image, type what you want to
hide (or paste from cliboard using CTRL+V), type your password (>8 chars) and
you're finished. To view, Click on "View from Image" and click the image you
injected text to. Type your password and you're done.

'''

class injector:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title(WM_TITLE)
        self.root.geometry(WM_SIZE)

        self.buttongrid = ctk.CTkFrame(self.root)
        self.openbutton = ctk.CTkButton(self.buttongrid , text="Open Image" , width=100 , command=self.openfile).grid(row=0,column=1 ,padx=10,pady=10)
        self.openbutton = ctk.CTkButton(self.buttongrid , text="View from Image" , width=110 , command=self.view).grid(row=0,column=2 ,padx=10,pady=10)
        self.aboutbutton = ctk.CTkButton(self.buttongrid , text="About" , width=100, command=self.about).grid(row=0,column=3 ,padx=10,pady=10)
        self.helpbutton = ctk.CTkButton(self.buttongrid , text="Help" , width=100,command=self.help).grid(row=0,column=4 ,padx=10,pady=10)
        self.buttongrid.place(relx=0.5,rely=0.5,anchor=ctk.CENTER)

        self.filesize_var = StringVar()
        self.path_var = StringVar()
       
        self.has_text_data = None

        self.aboutwindow = None
        self.helpwindow = None
        self.view_window = None


        self.path_label = ctk.CTkLabel(master=self.root,textvariable=self.path_var)
        self.filesize_label = ctk.CTkLabel(master=self.root,textvariable=self.filesize_var)

    def help(self):
        if self.helpwindow is None or not self.helpwindow.winfo_exists():
            self.helpwindow = ctk.CTkToplevel()
            self.helpwindow.resizable(False, False)
            self.helpwindow.geometry("600x475+1096+90")
            self.helpwindow.title("Help")
            self.textbox = ctk.CTkTextbox(
                master=self.helpwindow, width=650, height=400, font=TEXTFONT 
            )
            self.textbox.insert("1.0", HELP_STRING)
            self.textbox.pack()
            self.textbox.configure(state=ctk.DISABLED )
            self.helpwindow.focus()
            self.destroy_button = ctk.CTkButton(
                master=self.helpwindow,
                text="Exit",
                command=lambda: self.helpwindow.destroy(),
            ).place(relx=0.5, rely=0.9, anchor=ctk.CENTER)

        else:
            self.helpwindow.focus()

    def about(self):
        if self.aboutwindow is None or not self.aboutwindow.winfo_exists():
            self.aboutwindow = ctk.CTkToplevel()
            self.aboutwindow.resizable(False, False)
            self.aboutwindow.geometry("550x600+1096+90")
            self.aboutwindow.title("About")
            self.textbox = ctk.CTkTextbox(
                master=self.aboutwindow, width=650, height=550, font=TEXTFONT
            )
            self.textbox.insert(
                "1.0",
                ABOUT_STRING    
            )
            self.textbox.pack()
            self.textbox.configure(state=ctk.DISABLED)
            self.aboutwindow.focus()
            buttongrid = ctk.CTkFrame(self.aboutwindow)
            self.destroy_button = ctk.CTkButton(
                master=buttongrid,
                text="Exit",
                command=lambda: self.aboutwindow.destroy(),
            ).grid(row=0, column=1, padx=10, pady=10)
            self.destroy_button = ctk.CTkButton(
                master=buttongrid,
                text="View license",
                command=lambda: os.system("start notepad.exe LICENSE"),
            ).grid(row=0, column=2, padx=10, pady=10)
            buttongrid.place(relx=0.5, rely=0.9, anchor=ctk.CENTER)
            
        else:
            self.aboutwindow.focus()

    def select_all(self):
        self.text_label.tag_add("sel", "1.0","end")
        self.copybtn.grid(row=0 ,column=3 ,padx=10)


    def copy_text(self):
        if self.text_label.selection_get():
            self.text = self.text_label.selection_get()
            pyperclip.copy(self.text)
            self.copylabel.grid(row=0, column=4 ,padx=10,pady=10)
 


    def view(self):
        self.photo_file= None
        self.image_data = None

        try:
            self.photo_file = filedialog.askopenfile(mode='rb' , filetypes=[('JPEG Files', '*.jpg , *.jpeg')])
        except PermissionError as err:
            messagebox.showerror(title="Error" , message=f"{type(err).__name__}: You seem to not have the nesessary permissions to edit this image...")

        if self.photo_file is not None:
            
            self.path = os.path.abspath(self.photo_file.name)
            try:
                self.image_data = ImageData(self.path) # Object creation using imagedata class

                self.buttongrid.destroy()

                self.path_var.set(f"File: {self.path}")
                self.filesize_var.set(f"Size(In bytes): {self.image_data.filesize}")
                self.path_label.pack(padx=45,pady=20)
                self.filesize_label.pack()
            except ValueError:
                messagebox.showerror(title="Error",message="The image you chose doesn't have the correct headers needed for injection. Maybe the image is corrupted.")
                return 0

            self.obutton_frame = ctk.CTkFrame(master=self.root)
            self.previewimage_button = ctk.CTkButton(master=self.obutton_frame,text="Preview Image" , command=lambda :preview_image(self.path),width=100).grid(row=0,column=1,padx=10,pady=10)
            self.injecttext_button = ctk.CTkButton(master=self.obutton_frame , text="View Injected Text" , command=self.viewtext , width=100).grid(row=0,column=2,padx=10,pady=10) 
            self.getback_button =ctk.CTkButton(master=self.obutton_frame , text="Back" , command=self.revert , width=100).grid(row=0,column=3,padx=10,pady=10) 
            self.obutton_frame.place(relx=0.5,rely=0.5,anchor=ctk.CENTER)

    def viewtext(self):
        if self.view_window is None or not self.view_window.winfo_exists():
            self.d = self.image_data.get_data()
            self.password_dialog = ctk.CTkInputDialog(text="Please input the password." ,entry_text_color="#030515", title=f"{WM_TITLE}")
            _password = self.password_dialog.get_input()
            try:
                _e = Enc(_password)
                _k = _e.key
                _s = _e.decrypt(self.d , _k)
                self.str = str(_s ,encoding="utf-8" , errors='ignore' )
            except Exception as err:
                messagebox.showerror(title="Error" , message=f"{err}")
                return 0

            
            self.view_window = ctk.CTkToplevel()
            
            self.view_window.geometry("500x300+1096+90")
            self.view_window.title(f"{self.path} - View Text")
            self.text_label = ctk.CTkTextbox(master=self.view_window,width=(700 / 2))
            self.text_label.configure(state=ctk.NORMAL)
            self.text_label.insert(text=self.str , index='0.0')
            self.text_label.configure(state=ctk.DISABLED)
            self.text_label.place(relx=0.5,rely=0.4,anchor=ctk.CENTER)
            self.vbutton_frame = ctk.CTkFrame(master=self.view_window)
            self.exitbtn = ctk.CTkButton(master=self.vbutton_frame, text="Exit" , command=lambda: self.view_window.destroy()).grid(row=0 ,column=1 ,padx=10 , pady=10)
            self.selabtn = ctk.CTkButton(master=self.vbutton_frame, text="Select All" ,width=75 ,command=self.select_all).grid(row=0 ,column=2 ,padx=10 ,pady=10)
            self.copybtn = ctk.CTkButton(master=self.vbutton_frame, text="Copy" ,width=75 ,command=self.copy_text)
            self.copylabel = ctk.CTkLabel(master=self.vbutton_frame , text="Copied to Clipboard!")
            self.vbutton_frame.place(relx=0.5 , rely=0.9 , anchor=ctk.CENTER)

    def openfile(self):
        self.photo_file= None
        self.image_data = None

        try:
            self.photo_file = filedialog.askopenfile(mode='ab' , filetypes=[('JPEG Files', '*.jpg , *.jpeg')])
        except PermissionError as err:
            messagebox.showerror(title="Error" , message=f"{type(err).__name__}: You seem to not have the nesessary permissions to edit this image...")

        if self.photo_file is not None:
            
            self.path = os.path.abspath(self.photo_file.name)
            try:
                self.image_data = ImageData(self.path) # Object creation using imagedata class

                self.buttongrid.destroy()

                self.path_var.set(f"File: {self.path}")
                self.filesize_var.set(f"Size(In bytes): {self.image_data.filesize}")
                self.path_label.pack(padx=45,pady=20)
                self.filesize_label.pack()
            except ValueError:
                messagebox.showerror(title="Error",message="The image you chose doesn't have the correct headers needed for injection. Maybe the image is corrupted.")
                return 0

            self.obutton_frame = ctk.CTkFrame(master=self.root)
            self.previewimage_button = ctk.CTkButton(master=self.obutton_frame,text="Preview Image" , command=lambda :preview_image(self.path),width=100).grid(row=0,column=1,padx=10,pady=10)
            self.injecttext_button = ctk.CTkButton(master=self.obutton_frame , text="Inject Text" , command=self.injecttext , width=100).grid(row=0,column=2,padx=10,pady=10) 
            self.getback_button =ctk.CTkButton(master=self.obutton_frame , text="Back" , command=self.revert , width=100).grid(row=0,column=3,padx=10,pady=10) 
            self.obutton_frame.place(relx=0.5,rely=0.5,anchor=ctk.CENTER)

    def injecttext(self):
        self.injecttext_dialog = ctk.CTkInputDialog(text="Type the text you want to inject:" , title=f"{WM_TITLE} - InjectText")
        self.str = self.injecttext_dialog.get_input()
        if self.has_text_data is not None or not False:
                self.start_offset = self.image_data.start_offset
                self.endheader = self.image_data.end_head
                self.image_data.erase_data(self.start_offset,self.endheader)
        try:
            if len(self.str) == 0:
                 return 
            if not len(self.str) > TEXT_MAX_CHAR:
                self.password_dialog = ctk.CTkInputDialog(text="Please input a password(Requied)" ,entry_text_color="#030515" ,  title=f"{WM_TITLE} - InjectText")
                password = self.password_dialog.get_input()
                if not password:
                    return
                c = Enc(password)
                k = c.key
                self.image_data.write_data(c.encrypt(self.str,k))
                self.filesize_var.set(f"Size(In bytes): {self.image_data.filesize}")
                self.has_text_data = True
            else:
                messagebox.showerror(title="Error",message=f"The text you inputted is too long(>{TEXT_MAX_CHAR} characters)")
        except TypeError: 
                print("sdsdsdss")

    def revert(self):
        self.image_data = None
        self.obutton_frame.destroy()
        self.path_var.set(f"")
        self.filesize_var.set(f"")
        self.buttongrid = ctk.CTkFrame(self.root)
        self.openbutton = ctk.CTkButton(self.buttongrid , text="Open Image" , width=100 , command=self.openfile).grid(row=0,column=1 ,padx=10,pady=10)
        self.openbutton = ctk.CTkButton(self.buttongrid , text="View from Image" , width=110 , command=self.view).grid(row=0,column=2 ,padx=10,pady=10)
        self.aboutbutton = ctk.CTkButton(self.buttongrid , text="About" , width=100, command=self.about).grid(row=0,column=3 ,padx=10,pady=10)
        self.helpbutton = ctk.CTkButton(self.buttongrid , text="Help" , width=100,command=self.help).grid(row=0,column=4 ,padx=10,pady=10)
        self.buttongrid.place(relx=0.5,rely=0.5,anchor=ctk.CENTER)


    def run(self):
        self.root.mainloop()


injector().run()
