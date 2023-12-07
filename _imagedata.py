from _modules import *


class ImageData:
    def __init__(self, filepath):
        if type(filepath) != str:
            raise TypeError("Not a valid path.")

        self.filepath = filepath
        self.filesize = os.path.getsize(self.filepath)

        self.start_offset = self.get_offset(INJECT_START_OFFSET)
        try:
            self.end_head = self.get_eof()
        except ValueError:
            self.end_end = 0

    def erase_data(self, offset, length):
        with open(self.filepath, "rb+") as self.filep:
            self.filep.seek(offset + length)
            self.data = self.filep.read()
            self.filep.seek(offset)
            self.filep.write(self.data)
            self.filep.truncate()

    def get_offset(self, string):
        with open(self.filepath, "rb") as self.filep:
            l = len(string) / 2
            if l % 2 == 1:
                raise ValueError(
                    f"String '{string}' length is odd. provide a padding. (usually 0s) "
                )
            else:
                c = self.filep.read()
                o = c.index(bytes.fromhex(string))
                return int(o + l)

    def write_data(self, data):
        self.data = data
        with open(self.filepath, "ab") as self.filep:
            try:
                self.filep.write(self.data)
                messagebox.showinfo(title="Info", message="Injection Succsesful.")
                # self.filep.close()
            except Exception as e:
                messagebox.showerror(title="Error", message=f"{e}")

    def get_data(self):
        with open(self.filepath, "rb") as self.filep:
            self.filep.seek(self.start_offset)
            byte_data = self.filep.read()
            return byte_data

    def get_eof(self):
        with open(self.filepath, "rb") as self.filep:
            self.filep.seek(0, 2)
            return self.filep.tell()
