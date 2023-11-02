from _modules import *
from _imagedata import *
from _cryptor import *

WM_TITLE = "Skulker Viewer"



class Viewer:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title(WM_TITLE)
        self.root.geometry(WM_SIZE)
        
        # menubar
        self.menubar = Menu(self.root) #  base object
        self.file_menu = Menu(self.menubar , tearoff=False)
        self.help_menu = Menu(self.menubar , tearoff=False)

        self.menubar.add_cascade(label="File" , menu=self.file_menu)
        self.menubar.add_cascade(label="Help" , menu=self.help_menu)

        self.file_menu.add_command(label="Open File" , command=self.open_file)
        # self.file_menu.add_separator()
        # self.file_menu.add_command(label="Exit" , command=lambda :exit(0))
        self.help_menu.add_command(label="Help" , command=lambda :show_help())
        self.help_menu.add_command(label="About" , command=self.show_about)


        # Welcome Screen
        self.welcome_frame = ctk.CTkFrame(master=self.root)
        self.welcome_label = ctk.CTkLabel(master=self.welcome_frame , text=f"Welcome to {WM_TITLE}!\nPlease Open an image to get started.").pack(padx=10,pady=10)
        self.wbutton_frame = ctk.CTkFrame(master= self.welcome_frame)
        self.openfile_button = ctk.CTkButton(master=self.wbutton_frame , text="Open" , command=self.open_file , width=100).grid(row=0 , column=1 , padx=10 , pady=10)
        self.help_button =     ctk.CTkButton(master=self.wbutton_frame , text="Help" , command=lambda :show_help(), width=100).grid(row=0 , column=2 , padx=10 , pady=10)
        self.about_button =    ctk.CTkButton(master=self.wbutton_frame , text="About Skulker" , command=self.show_about , width=100).grid(row=0 , column=3 , padx=10 ,pady=10)

        self.wbutton_frame.pack(padx=10,pady=10)
        self.welcome_frame.place(relx=0.5,rely=0.5,anchor=ctk.CENTER)



        # Variables
        self.filesize_var = StringVar()
        self.path_var = StringVar()
        self.about_window = None
        self.view_window = None
        self.has_text_data = None


        self.path_label = ctk.CTkLabel(master=self.root,textvariable=self.path_var)
        self.filesize_label = ctk.CTkLabel(master=self.root,textvariable=self.filesize_var)


    def open_file(self):
        self.photo_file= None
        self.image_data = None

        self.photo_file = filedialog.askopenfile(mode='ab' , filetypes=[('JPEG Files', '*.jpg , *.jpeg')])

        if self.photo_file is not None:
            
            self.path = os.path.abspath(self.photo_file.name)
            self.image_data = ImageData(self.path) # Object creation using imagedata class

            self.welcome_frame.destroy()
            self.wbutton_frame.destroy()

            self.path_var.set(f"File: {self.path}")
            self.filesize_var.set(f"Size(In bytes): {self.image_data.filesize}")
            self.path_label.pack(padx=45,pady=20)
            self.filesize_label.pack()

            self.root.config(menu=self.menubar)

            self.obutton_frame = ctk.CTkFrame(master=self.root)
            self.previewimage_button = ctk.CTkButton(master=self.obutton_frame,text="Preview Image" , command=lambda :preview_image(self.path),width=100).grid(row=0,column=1,padx=10,pady=10)
            self.injecttext_button = ctk.CTkButton(master=self.obutton_frame , text=" View Injected Text" , command=self.view_text , width=100).grid(row=0,column=2,padx=10,pady=10) 
            self.obutton_frame.place(relx=0.5,rely=0.4,anchor=ctk.CENTER)


    



    def view_text(self):
        if self.view_window is None or not self.view_window.winfo_exists():
            self.view_window = ctk.CTkToplevel()
            self.d = self.image_data.get_data()
            self.password_dialog = ctk.CTkInputDialog(text="Please input the password." ,entry_text_color="#333", title=f"{WM_TITLE}")
            password = self.password_dialog.get_input()
            e = Enc(password)
            k = e.key
            self.str = str(e.decrypt(self.d , k) ,encoding="utf-8" , errors='ignore' )
            self.view_window.geometry("500x300+1096+90")
            self.view_window.title(f"{self.path} - View Text")
            self.text_label = ctk.CTkTextbox(master=self.view_window,width=(700 / 2))
            self.text_label.configure(state=ctk.NORMAL)
            self.text_label.insert(text=self.str , index='0.0')
            self.text_label.configure(state=ctk.DISABLED)
            self.text_label.place(relx=0.5,rely=0.4,anchor=ctk.CENTER)
            self.vbutton_frame = ctk.CTkFrame(master=self.view_window)
            self.exitbtn = ctk.CTkButton(master=self.vbutton_frame, text="Exit" , command=lambda: self.view_window.destroy()).grid(row=0 ,column=1 ,padx=10 , pady=10)
            self.selabtn = ctk.CTkButton(master=self.vbutton_frame, text="Select All" ,width=75 ,command=self.select_all)
            self.selabtn.grid(row=0 ,column=2 ,padx=10 ,pady=10)
            self.copybtn = ctk.CTkButton(master=self.vbutton_frame, text="Copy" ,width=75 ,command=self.copy_text)
            self.vbutton_frame.place(relx=0.5 , rely=0.9 , anchor=ctk.CENTER)

        else:
            self.view_window.focus()

    def select_all(self):
        self.text_label.tag_add("sel", "1.0","end")
        self.copybtn.grid(row=0 ,column=3 ,padx=10)


    def copy_text(self):
        if self.text_label.selection_get():
            self.text = self.text_label.selection_get()
            pyperclip.copy(self.text)
            messagebox.showinfo(title=WM_TITLE , message="Copied to Clipboard!")           


    def show_about(self):
        if self.about_window is None or not self.about_window.winfo_exists():
            self.about_window = ctk.CTkToplevel()
            self.about_window.resizable(False,False)
            self.about_window.geometry("400x300+1096+90")
            self.about_window.title(f"About {WM_TITLE}")
            self.about_label = ctk.CTkLabel(master=self.about_window,text=f"{WM_TITLE}\nVersion: {VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}\n\nMade by Bigg Smoke\nPublished by The Lunar Surface (c) 2023\nuses 'Imagine': Copyright (c) 2003-2023 Sejin Chun\n\nTkinter version: {TkVersion}\nPython Version: {platform.python_version()}\nImagine Version:1.3.1",font=("Roboto",14)).place(relx=0.5,rely=0.4,anchor=ctk.CENTER)
            self.destroy_button = ctk.CTkButton(master=self.about_window , text="Exit" , command=lambda: self.about_window.destroy()).place(relx=0.5 , rely=0.9 , anchor=ctk.CENTER)
            self.about_window.focus()
        else:
            self.about_window.focus()


    def run(self):
        self.root.mainloop()




Viewer().run()