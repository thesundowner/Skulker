from _modules import *

SALT = b'M\xa6\xf4\xd3\xf6\xd2L\xba\x0c<\xc5O\x98\x14\t\x19'
SALT = sha256(SALT).digest()

class Enc:
    def __init__(self, password):
        password = str(password)
        h = None
        if len(password) < 8:
            raise ValueError("Password too short.")
        
        h = sha256()
        h.update(password.encode('utf-8'))
        password = h.hexdigest()
        self.key = self.gen_key(password, SALT)

    def gen_key(self, password, salt):
        return PBKDF2(password, salt, dkLen=32)

    def pad(self, st):
        s = bytes(st, encoding="utf-8", errors="ignore")
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def decrypt(self, ciphertext, key):
        try:
            iv = ciphertext[: AES.block_size]
            cipher = AES.new(key, AES.MODE_CBC, iv)
            otext = cipher.decrypt(ciphertext[AES.block_size :])
            return otext.rstrip(b"\0")
        except Exception as err:
            messagebox.showerror(title='Error' , message=err)
            return 