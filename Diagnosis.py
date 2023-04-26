class Diagnosis:
    def __init__(self, diagnosis):
        self.__doctor = diagnosis['doctor']
        self.__sickness = diagnosis['sickness']
        self.__code = diagnosis['code']
        self.__description = diagnosis['description']
        self.__treatments = diagnosis['treatments']
        self.__medications = diagnosis['medications']

    def __eq__(self, other):
        if isinstance(other, Diagnosis):
            if self.__doctor == other.__doctor:
                if self.__sickness == other.__sickness:
                    if self.__code == other.__code:
                        if self.__description == other.__description:
                            if self.__treatments == other.__treatments:
                                if self.__medications == other.__medications:
                                    return True
        return False

    def to_dict(self):
        return {
            "doctor": self.__doctor,
            "sickness": self.__sickness,
            "code": self.__code,
            "description": self.__description,
            "treatments": self.__treatments,
            "medications": self.__medications
        }
