from _modules import *
from _imagedata import *
from _cryptor import *

WM_TITLE = "Skulker Injector"



class Injector:
    def __init__(self):
        show_warning(READY_FOR_PRODUCTION)
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
        # self.file_menu.add_command(label="Exit" , command=lambda :exit())
        self.help_menu.add_command(label="Help" , command=lambda :show_help())
        self.help_menu.add_command(label="About" , command=self.show_about)

        # welcome screen

        self.welcome_frame = ctk.CTkFrame(master=self.root)
        self.welcome_label = ctk.CTkLabel(master=self.welcome_frame , text=f"Welcome to {WM_TITLE}!\nPlease Open an image to get started.").pack(padx=10,pady=10)
        self.wbutton_frame = ctk.CTkFrame(master= self.welcome_frame)
        self.openfile_button = ctk.CTkButton(master=self.wbutton_frame , text="Open" , command=self.open_file , width=100).grid(row=0 , column=1 , padx=10 , pady=10)
        self.help_button =     ctk.CTkButton(master=self.wbutton_frame , text="Help" , command=lambda :show_help() , width=100).grid(row=0 , column=2 , padx=10 , pady=10)
        self.about_button =    ctk.CTkButton(master=self.wbutton_frame , text="About Skulker" , command=self.show_about , width=100).grid(row=0 , column=3 , padx=10 ,pady=10)

        self.wbutton_frame.pack(padx=10,pady=10)
        self.welcome_frame.place(relx=0.5,rely=0.5,anchor=ctk.CENTER)


        # variables
        self.filesize_var = StringVar()
        self.path_var = StringVar()
        self.about_window = None
        
        self.has_text_data = None


        self.path_label = ctk.CTkLabel(master=self.root,textvariable=self.path_var)
        self.filesize_label = ctk.CTkLabel(master=self.root,textvariable=self.filesize_var)







    def open_file(self):
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

                    self.welcome_frame.destroy()
                    self.wbutton_frame.destroy()

                    self.path_var.set(f"File: {self.path}")
                    self.filesize_var.set(f"Size(In bytes): {self.image_data.filesize}")
                    self.path_label.pack(padx=45,pady=20)
                    self.filesize_label.pack()
                except ValueError:
                    messagebox.showerror(title="Error",message="The image you chose doesn't have the correct headers needed for injection. Maybe the image is corrupted.")
                    return 0

                self.root.config(menu=self.menubar)

                self.obutton_frame = ctk.CTkFrame(master=self.root)
                self.previewimage_button = ctk.CTkButton(master=self.obutton_frame,text="Preview Image" , command=lambda :preview_image(self.path),width=100).grid(row=0,column=1,padx=10,pady=10)
                self.injecttext_button = ctk.CTkButton(master=self.obutton_frame , text="Inject Text" , command=self.inject_text , width=100).grid(row=0,column=2,padx=10,pady=10) 
                self.obutton_frame.place(relx=0.5,rely=0.4,anchor=ctk.CENTER)


    def show_about(self):
        if self.about_window is None or not self.about_window.winfo_exists():
            self.about_window = ctk.CTkToplevel()
            self.about_window.resizable(False,False)
            self.about_window.geometry("400x300+1096+90")
            self.about_window.title(f"About {WM_TITLE}")
            self.about_label = ctk.CTkLabel(master=self.about_window,text=f"{WM_TITLE}\nVersion: {VERSION_STR}\n\nMade by Bigg Smoke\nPublished by The Lunar Surface (c) 2023\nuses 'Imagine': Copyright (c) 2003-2023 Sejin Chun\n\nTkinter version: {TkVersion}\nPython Version: {platform.python_version()}\nImagine Version:1.3.1",font=("Roboto",14)).place(relx=0.5,rely=0.4,anchor=ctk.CENTER)
            self.destroy_button = ctk.CTkButton(master=self.about_window , text="Exit" , command=lambda: self.about_window.destroy()).place(relx=0.5 , rely=0.9 , anchor=ctk.CENTER)
            self.about_window.focus()
        else:
            self.about_window.focus()



    def inject_text(self):
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
                c = Enc(password)
                k = c.key
                self.image_data.write_data(c.encrypt(self.str,k))
                self.filesize_var.set(f"Size(In bytes): {self.image_data.filesize}")
                self.has_text_data = True
            else:
                messagebox.showerror(title="Error",message="The text you inputted is too long(>1024 characters)")

        except TypeError:
            # messagebox.showerror(title="Error" , message="Can't inject nothing...")  
                return 


    def run(self):
        self.root.mainloop()



Injector().run()