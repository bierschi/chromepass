import os
import sqlite3
import platform

from chromepass import ChromeLinux, ChromeWindows, ChromeMac


class Chromepass:
    """ class Chromepass to get the passwords from the database file

        Usage:
            chpass = Chromepass()
            chpass.get_passwords()
    """
    def __init__(self):

        self.conn = None
        self.cursor = None
        self.results = list()

        if platform.system() == 'Windows':
            self.os = ChromeWindows()
        elif platform.system() == 'Linux':
            self.os = ChromeLinux()
        elif platform.system() == 'Darwin':
            self.os = ChromeMac()

        self.connect_to_database_file()

    def __del__(self):
        """destructor"""
        self.close_connection()

    def close_connection(self):
        """ closes the db connection

        """
        if self.conn:
            self.conn.close()

    def connect_to_database_file(self):
        """ connect to the database file

        """

        if os.path.exists(self.os.tmp_login_db_path):
            self.conn = sqlite3.connect(self.os.tmp_login_db_path)
            self.cursor = self.conn.cursor()
        else:
            print("File does not exist: {}".format(self.os.tmp_login_db_path))

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

                    # decrypt the password
                    password = self.os.decrypt_password(encrypted_password=encrypted_password)
                    if password:
                        account_details = dict()
                        account_details['url'] = url
                        account_details['username'] = username
                        account_details['password'] = password
                        self.results.append(account_details)

                return self.results
            else:
                print('No results returned from sql query')
                return self.results

        except sqlite3.OperationalError as ex:
            print('SQL Error {}'.format(ex))
            return self.results

