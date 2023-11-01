# (C) 2023 BIGG SMOKE
"""
Image Data Class for handling special imagefile operations such
as deleting part of the data and injecting new ones.
"""

from modules import *

class ImageData:
    def __init__(self , filepath):
        if type(filepath) != str:
            raise TypeError("Not a valid path")
        
        self.file_path = filepath
        self.file_size = os.path.getsize(self.file_path)
        self.start_o = self.get_offset(INJECT_START_OFFSET)
        try:
            self.end_head = self.get_eof()
        except ValueError:
            self.end_head = 0

    def erase_data(self, offset,length):
        with open(self.file_path , 'rb+') as self.filep:
            self.filep.seek(offset + length)
            self.data = self.filep.read()
            self.filep.seek(offset)
            self.filep.write(self.data)
            self.filep.truncate()


    def get_offset(self,string):
        with open(self.file_path , 'rb') as self.filep:
            self.length = len(string) / 2
            if self.length % 2 == 1:
                raise ValueError("String length is of odd value")
            else:
                self.c = self.filep.read()
                self.o = self.c.index(bytes.fromhex(string))
                return int(self.o + self.length)
            
    def write_data(self , data):
        self.data = data
        with open(self.file_path , 'ab') as self.filep:
            try:
                self.data = self.data #+ bytes.fromhex(END_INJECT_HEADER)
                self.filep.write(self.data)
                messagebox.showinfo(title="Info" , message="Injection Successful")

            except:
                messagebox.showerror(title="Error" , message="Injection unsuccessful")

    def get_data(self):
        with open(self.file_path , 'rb') as self.filep:
            self.c = self.filep.read()
            self.filep.seek(self.start_o)
            self.byte_data = self.filep.read()
            # self.data = str(self.byte_data, encoding='utf-8' , errors='ignore')
            # if self.data == "":
            #     return "<NO DATA AVAILABLE>"
            # return self.data.replace("ÿß" , " ")
            return self.byte_data
        

    def get_eof(self):
        with open(self.file_path , 'rb') as self.filep:
            self.filep.seek(0,2)
            return self.filep.tell()
        
class Enc:
    def __init__(self , password):
        self.password = str(password)

    def gen_key(self):
        return PBKDF2(self.password, SALT,dkLen=32)

    def pad(self,st):
        s = bytes(st , encoding='utf-8' , errors='ignore')
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)
    

    def encrypt(self,message,key,key_size=256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC , iv)
        return iv + cipher.encrypt(message)
    

    def decrypt(self, ciphertext,key):
        iv= ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC , iv)
        ptext = cipher.decrypt(ciphertext[AES.block_size:])
        return ptext.rstrip(b"\0")