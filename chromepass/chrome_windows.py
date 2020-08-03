import os
import shutil
import json
import base64
from Cryptodome.Cipher import AES
try:
    import win32crypt
except ImportError as ex:
    pass

from chromepass import Chrome


class ChromeWindows(Chrome):
    """ class ChromeWindows to get the passwords from the Windows Chrome browser

        Usage:
            chrome_win = ChromeWindows()
            chrome_win.decrypt_password(encrypted_password=encrypted_password)
    """
    def __init__(self):

        # init base class
        super().__init__()

        self.login_db_path = os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\default\Login Data'
        self.tmp_login_db_path = os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\default\Login_tmp'

        if os.path.exists(self.login_db_path):
            shutil.copy2(self.login_db_path, self.tmp_login_db_path)  # making a temp copy since login data db is locked while chrome is running
        else:
            print("It seems that no chrome browser is installed! Exiting...")
            exit(1)

        self.local_state_path = os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\Local State'

        self.master_key = self.__get_master_key()

    def __del__(self):
        """destructor"""
        try:
            os.remove(self.tmp_login_db_path)
        except FileNotFoundError as ex:
            pass

    def __get_master_key(self):
        """ get the master key from the Local State file

        :return: master_key
        """

        with open(self.local_state_path, "r", encoding='utf-8') as f:
            local_state = json.loads(f.read())
        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]

        return master_key

    def __decrypt_payload(self, cipher, payload):
        """ decrypts the given payload

        :param cipher: cipher
        :param payload: payload

        :return: decrypted payload
        """
        return cipher.decrypt(payload)

    def __generate_cipher(self, aes_key, iv):
        """ generates the AES cipher in GCM Mode

        :param aes_key: aes key
        :param iv: iv

        :return: AES cipher
        """
        return AES.new(aes_key, AES.MODE_GCM, iv)

    def __crypt_unprotected_data(self, encrypted_password):
        """ crypt unprotected data with the win32crypt module

        :return: decrypted password
        """
        return win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1]

    def decrypt_password(self, encrypted_password):
        """ decrypt the given encrypted password

        :param encrypted_password: encrypted  password

        :return: decrypted password
        """
        try:
            decrypted_password = self.__crypt_unprotected_data(encrypted_password=encrypted_password)
            if isinstance(decrypted_password, bytes):
                decrypted_password = str(decrypted_password, 'utf-8')

            return decrypted_password
        except Exception as ex:
            iv = encrypted_password[3:15]
            payload = encrypted_password[15:]
            cipher = self.__generate_cipher(self.master_key, iv)
            decrypted_password = self.__decrypt_payload(cipher, payload)
            decrypted_password = decrypted_password[:-16].decode()  # remove suffix bytes

            return decrypted_password


