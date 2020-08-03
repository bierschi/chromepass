import os
import shutil
from getpass import getuser

from chromepass import Chrome


class ChromeMac(Chrome):
    """ class ChromeMac to get the passwords from the Mac Chrome browser

        Usage:
            chrome_mac= ChromeMac()
            chrome_mac.decrypt_password(encrypted_password=encrypted_password)
    """
    def __init__(self):

        # init base class
        super().__init__()

        self.login_db_path = f"/Users/{getuser()}/Library/Application Support/Google/Chrome/Default/Login Data"
        self.tmp_login_db_path = f"/Users/{getuser()}/Library/Application Support/Google/Chrome/Default/Login_tmp"

        if os.path.exists(self.login_db_path):
            shutil.copy2(self.login_db_path, self.tmp_login_db_path)  # making a temp copy since login data db is locked while chrome is running
        else:
            print("It seems that no chrome browser is installed! Exiting...")
            exit(1)

    def __del__(self):
        """destructor"""
        try:
            os.remove(self.tmp_login_db_path)
        except FileNotFoundError as ex:
            pass

    def decrypt_password(self, encrypted_password):
        """ decrypt the given encrypted password

        :param encrypted_password:
        :return:
        """
        pass
