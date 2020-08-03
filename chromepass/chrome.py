from abc import ABC, abstractmethod


class Chrome(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def decrypt_password(self, encrypted_password):
        """ decrypt the given encrypted password

        :param encrypted_password: encrypted password

        :return: decrypted password
        """
        pass
