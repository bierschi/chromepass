import os
import shutil
import subprocess
import secretstorage
from time import sleep
from getpass import getuser
from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import PBKDF2

from chromepass import Chrome


class ChromeLinux(Chrome):
    """ class ChromeLinux to get the passwords from the Linux Chrome browser

        Usage:
            chrome_linux = ChromeLinux()
            chrome_linux.decrypt_password(encrypted_password=encrypted_password)
    """
    def __init__(self):

        # init base class
        super().__init__()

        self.login_db_path = f"/home/{getuser()}/.config/google-chrome/Default/Login Data"
        self.tmp_login_db_path = f"/home/{getuser()}/.config/google-chrome/Default/Login_tmp"

        if os.path.exists(self.login_db_path):
            shutil.copy2(self.login_db_path, self.tmp_login_db_path)  # making a temp copy since login data db is locked while chrome is running
        else:
            print("It seems that no chrome browser is installed! Exiting...")
            exit(1)

        self.iv = b' ' * 16
        self.password = 'peanuts'.encode('utf8')

        bus = secretstorage.dbus_init()
        collection = secretstorage.get_default_collection(bus)
        for item in collection.get_all_items():
            if item.get_label() == 'Chrome Safe Storage':
                try:
                    self.password = item.get_secret()
                except secretstorage.exceptions.LockedException as ex:
                    print("Chrome database file is locked. Opening browser as background process. Terminating after 1 sec ...")
                    self.open_chrome()
                    self.password = item.get_secret()
                break

        self.key = PBKDF2(password=self.password, salt=b'saltysalt', dkLen=16, count=1)
        self.cipher = AES.new(self.key, AES.MODE_CBC, IV=self.iv)
        self.bytechars = [b'\x01', b'\x02', b'\x03', b'\x04', b'\x05', b'\x06', b'\x07', b'\x08', b'\x09']

    def __del__(self):
        """destructor"""
        try:
            os.remove(self.tmp_login_db_path)
        except FileNotFoundError as ex:
            pass

    def open_chrome(self):
        """ opens chrome as a background process and terminates it after one second

        """
        proc = subprocess.Popen(["/usr/bin/google-chrome"])
        sleep(1)
        proc.terminate()

    def replace_chars(self, decrypted):
        """ replaces specific bytestring characters from decrypted bytestring

        :param decrypted: bytestring

        :return: bytestring without special chars
        """
        for c in self.bytechars:
            decrypted = decrypted.replace(c, b'')
        return decrypted

    def decrypt_password(self, encrypted_password):
        """ decrypt the given encrypted password

        :param encrypted_password: encrypted password

        :return decrypted password
        """

        enc_passwd = encrypted_password[3:]
        decrypted = self.cipher.decrypt(enc_passwd)

        try:
            decrypted = self.replace_chars(decrypted=decrypted)
            password = decrypted.decode(encoding='utf-8', errors='surrogateescape')
        except UnicodeDecodeError as ex:
            print("Could not decode the password in 'utf-8' encoding. Ignoring errors...")
            password = decrypted.strip().decode(encoding='utf-8', errors='ignore')

        return password
