from Patient import Patient
from Hospital import Hospital
from Diagnosis import Diagnosis


class MedicalRecord:
    def __init__(self, medical_record):
        self.__date = medical_record['date']
        self.__patient = Patient(medical_record['patient'])
        self.__hospital = Hospital(medical_record['hospital'])
        self.__diagnosis = Diagnosis(medical_record['diagnosis'])

    def __eq__(self, other):
        if isinstance(other, MedicalRecord):
            if self.__date == other.__date:
                if self.__patient == other.__patient:
                    if self.__hospital == other.__hospital:
                        if self.__diagnosis == other.__diagnosis:
                            return True
        return False

    def to_dict(self):
        return {
            "date": self.__date,
            "patient": self.__patient.to_dict(),
            "hospital": self.__hospital.to_dict(),
            "diagnosis": self.__diagnosis.to_dict()
        }
