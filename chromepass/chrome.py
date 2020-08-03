from abc import ABC, abstractmethod


class Chrome(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def decrypt_password(self, encrypted_password):
        """

        :param encrypted_password:
        :return:
        """
        pass
