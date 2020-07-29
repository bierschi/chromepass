import os
import sqlite3
import shutil

from chromepass import Cipher


class Chromepass:
    """
        class Chromepass to get the passwords from the database file

        Usage:
            chpass = Chromepass()
            chpass.get_passwords()
    """
    def __init__(self):

        self.conn = None
        self.cursor = None
        self.results = list()

        self.login_db_path = os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\default\Login Data'
        self.tmp_login_db_path = os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\default\Login_tmp'
        shutil.copy2(self.login_db_path, self.tmp_login_db_path)  # making a temp copy since login data db is locked while chrome is running

        self.connect_to_database_file()

        self.cipher = Cipher()

    def __del__(self):
        """destructor"""
        self.close_connection()
        os.remove(self.tmp_login_db_path)

    def close_connection(self):
        """ closes the db connection

        """
        if self.conn:
            self.conn.close()

    def connect_to_database_file(self):
        """

        :return:
        """

        if os.path.exists(self.tmp_login_db_path):
            print('\nOpening ' + self.tmp_login_db_path)
            self.conn = sqlite3.connect(self.tmp_login_db_path)
            self.cursor = self.conn.cursor()
        else:
            print("File does not exists: {}".format(self.tmp_login_db_path))

    def get_passwords(self):
        """ get passwords from database file

        :return: list containing account information (url, username, password)
        """

        try:
            self.cursor.execute('SELECT action_url, username_value, password_value FROM logins')
            data = self.cursor.fetchall()
            if len(data) > 0:
                for result in data:
                    url = result[0]
                    username = result[1]
                    encrypted_password = result[2]
                    password = None

                    # decrypt the password
                    try:
                        password = self.cipher.crypt_unprotected_data(encrypted_password=encrypted_password)
                        if isinstance(password, bytes):
                            password = str(password, 'utf-8')
                    except Exception as ex:
                        password = self.retry_with_masterkey(encrypted_password=encrypted_password)
                    finally:
                        if password:
                            account_details = dict()
                            account_details['url'] = url
                            account_details['username'] = username
                            account_details['password'] = password
                            self.results.append(account_details)

                return self.results
            else:
                print(' No results returned from sql query')

        except sqlite3.OperationalError as ex:
            print('Error {}'.format(ex))

    def retry_with_masterkey(self, encrypted_password):
        """ retry the encryption with the master key

        :return: decrypted password
        """
        master_key = self.cipher.get_master_key()
        decrypted_password = self.cipher.decrypt_password(encrypted_password, master_key)

        return decrypted_password


if __name__ == '__main__':
    chp = Chromepass()
    print(chp.get_passwords())
