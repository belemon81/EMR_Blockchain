class MedicalRecord:
    def __init__(self, medical_record):
        self.__patient = medical_record['patient']
        self.__hospital = medical_record['hospital']
        self.__date = medical_record['date']
        self.__diagnosis = medical_record['diagnosis']
        self.__medications = medical_record['medications']

        def get_patient(self):
            return self.__patient

        def get_hospital(self):
            return self.__hospital

        def get_date(self):
            return self.__date

        def get_diagnosis(self):
            return self.__address

        def set_patient(self, patient):
            self.__patient = patient

        def set_hospital(self, hospital):
            self.__hospital = hospital

        def set_date(self, date):
            self.__date = date

        def set_diagnosis(self, diagnosis):
            self.__diagnosis = diagnosis
