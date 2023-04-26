class Hospital:
    def __init__(self, hospital):
        self.__name = hospital['name']
        self.__address = hospital['address']
        self.__phone_number = hospital['phone_number']

    def __eq__(self, other):
        if isinstance(other, Hospital):
            if self.__name == other.__name:
                if self.__address == other.__address:
                    if self.__phone_number == other.__phone_number:
                        return True
        return False

    def to_dict(self):
        return {
            "name": self.__name,
            "address": self.__address,
            "phone_number": self.__phone_number
        }
