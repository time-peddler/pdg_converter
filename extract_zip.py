import os
import zipfile
import rarfile
import concurrent.futures


def read_passwords(password_file):
    with open(password_file, encoding='utf-8') as f:
        return list(set(map(str.strip, f)))


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
            print("Real password is: %s" % password)
        except Exception as e:
            if password:
                print(f"Test password: {password}, failed!")
            else:
                print(f"An error occurred while extracting {self.file_path}: {e}")

    def decrypt_and_extract(self, password_file="passwords.txt"):
        print('Encrypted! Trying to decrypt it with Passbook.')
        pwd_lists = read_passwords(password_file)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.extract_file, pwd) for pwd in pwd_lists]

            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Thread error: {e}")

    def extract(self):
        if not self.is_encrypted:
            self.extract_file()
        else:
            self.decrypt_and_extract()
