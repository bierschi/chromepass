__title__ = "chromepass"
__version_info__ = ('1', '0', '3')
__version__ = ".".join(__version_info__)
__author__ = "Christian Bierschneider"
__email__ = "christian.bierschneider@web.de"
__license__ = "MIT"

import os
from chromepass.chrome import Chrome
from chromepass.chrome_linux import ChromeLinux
from chromepass.chrome_windows import ChromeWindows
from chromepass.chrome_mac import ChromeMac
from chromepass.chrome_passwords import Chromepass


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
