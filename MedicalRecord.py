class MedicalRecord:
    def __init__(self, medical_record):
        self.__patient = medical_record['patient']
        self.__hospital = medical_record['hospital']
        self.__date = medical_record['date']
        self.__diagnosis = medical_record['diagnosis']
        self.__medications = medical_record['medications']
