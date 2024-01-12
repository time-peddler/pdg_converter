import os
import zipfile
import rarfile


class CompressionHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_type = file_path.split('.')[-1].lower()
        self.unzip2path = os.path.splitext(file_path)[0]
        self.is_encrypted = self.check_encryption()

    def check_encryption(self):
        try:
            if self.file_type in ["zip", "uvz"]:
                with zipfile.ZipFile(self.file_path) as zp:
                    for l in zp.infolist():
                        if l.flag_bits & 0x1:
                            return True
            elif self.file_type == "rar":
                with rarfile.RarFile(self.file_path, mode='r') as zp:
                    if zp.needs_password():
                        return True
            else:
                print("Unsupported file type: %s" % self.file_type)
                exit(0)
        except Exception as e:
            print("Error checking encryption:", e)
        return False

    def extract_file(self, password=''):
        try:
            if self.file_type in ["zip", "uvz"]:
                with zipfile.ZipFile(self.file_path, 'r') as zip_file:
                    zip_file.extractall(path=self.unzip2path, pwd=password.encode('utf-8'))
            elif self.file_type == "rar":
                with rarfile.RarFile(self.file_path, 'r') as rar_file:
                    rar_file.extractall(path=self.unzip2path, pwd=password.encode('utf-8'))
            return True
        except Exception as e:
            if password:
                print(f"Test password: {password}, failed!")
            else:
                print(f"An error occurred while extracting {self.file_path}: {e}")

    def decrypt_and_extract(self, password_file="passwords.txt"):
        print('Encrypted! Trying to decrypt it with Passbook.')

        try:
            with open(password_file, encoding='utf-8') as f:
                pwd_list = list(map(str.strip, f))
        except FileNotFoundError:
            print(f"Error: Password file '{password_file}' not found.")
            return

        while pwd_list:
            pwd = pwd_list.pop()
            if self.extract_file(pwd):
                print(f"Password '{pwd}' successfully decrypted.")
                return

        print('There is no correct password in the password book')
        exit(0)

    def extract(self):
        if self.is_encrypted:
            self.decrypt_and_extract()
        else:
            self.extract_file()
