class Diagnosis:
    def __init__(self, diagnosis):
        self.__date = diagnosis['date']
        self.__doctor = diagnosis['doctor']
        self.__sickness = diagnosis['sickness']
        self.__code = diagnosis['code']
        self.__description = diagnosis['description']
        self.__treatments = diagnosis['treatments']
