from _modules import *


class Enc:
    def __init__(self, password):
        password = str(password)
        if len(password) < 8:
            messagebox.showwarning(
                title="Error",
                message="Password is too short. Specify a longer one. (longer than 8 chars)",
            )
            raise ValueError("Password too short.")

        self.key = self.gen_key(password, ENC_SALT)

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
        iv = ciphertext[: AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        otext = cipher.decrypt(ciphertext[AES.block_size :])
        return otext.rstrip(b"\0")
