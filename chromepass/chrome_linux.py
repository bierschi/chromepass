import os
import shutil
import string
import secretstorage
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
        shutil.copy2(self.login_db_path, self.tmp_login_db_path)  # making a temp copy since login data db is locked while chrome is running

        self.iv = b' ' * 16
        self.password =  'peanuts'.encode('utf8')

        bus = secretstorage.dbus_init()
        collection = secretstorage.get_default_collection(bus)
        for item in collection.get_all_items():
            if item.get_label() == 'Chrome Safe Storage':
                self.password = item.get_secret()
                break

        self.key = PBKDF2(password=self.password, salt=b'saltysalt', dkLen=16, count=1)
        self.cipher = AES.new(self.key, AES.MODE_CBC, IV=self.iv)

    def __del__(self):
        """destructor"""
        os.remove(self.tmp_login_db_path)

    def decrypt_password(self, encrypted_password):
        """ decrypt the given encrypted password

        :param encrypted_password: encrypted passord

        :return decrypted password
        """

        enc_passwd = encrypted_password[3:]
        decrypted = self.cipher.decrypt(enc_passwd)
        password = decrypted.strip().decode('utf8')

        return ''.join(i for i in password if i in string.printable)
