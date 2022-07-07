class Attributes:
    gender = ""
    race = ""
    organ = ""
    disease_type = ""
    days_old_at_diagnosis = 0
    exposures_years_smoked = 0
    exposures_cigarettes_per_day = 0
    cancer_status = True
    file_id = ""

    def __init__(self, gender: str, race: str, organ: str, disease_type: str, days_old_at_diagnosis: int, exposures_years_smoked: int, exposures_cigarettes_per_day: float,file_id: str):
        """
        The __init__ function enables the creation of an object.
        :param gender: A string containing a gender.
        :param race: A string containing a race.
        :param organ: A string containing an organ.
        :param disease_type: A string containing a disease type.
        :param days_old_at_diagnosis: An int containing the days old at diagnosis.
        :param exposures_years_smoked: An int containing the amount of years smoked.
        :param exposures_cigarettes_per_day: An int containing the amount of cigarettes per day.
        :param file_id: A String containing a file_id.
        """
        self.gender = gender
        self.race = race
        self.organ = organ
        self.disease_type = disease_type
        self.days_old_at_diagnosis = days_old_at_diagnosis
        self.exposures_years_smoked = exposures_years_smoked
        self.exposures_cigarettes_per_day = exposures_cigarettes_per_day
        self.file_id = file_id

    def get_gender(self):
        """
        The function get_gender returns the gender of a object.
        :return: gender: A string containing a gender.
        """
        return self.gender
    
    def get_race(self):
        """
        The function get_race returns the race of a object.
        :return: race: A string containing a race.
        """
        return self.race
    
    def get_organ(self):
        """
        The function get_organ returns the organ of a object.
        :return: organ: A string containing an organ.
        """
        return self.organ

    def get_disease_type(self):
        """
        The function get_disease_type returns the disease type of a object.
        :return: disease_type: A string containing a disease type.
        """
        return self.disease_type

    def get_days_old_at_diagnosis(self):
        """
        The function get_days_old_at_diagnosis returns the days old at diagnosis for an object.
        :return: days_old_at_diagnosis: An int containing the days old at diagnosis.
        """
        return self.days_old_at_diagnosis

    def get_exposures_years_smoked(self):
        """
        The function get_exposures_years_smoked returns the amount of years smoked of a objects.
        :return: exposures_years_smoked: An int containing the amount of years smoked.
        """
        return self.exposures_years_smoked

    def exposures_cigarettes_per_day(self):
        """
        The function exposures_cigarettes_per_day returns the amount of cigarettes smoked per day of an object.
        :return: exposures_cigarettes_per_day: An int containing the amount of cigarettes per day.
        """
        return self.exposures_cigarettes_per_day

    def get_cancer_status(self):
        """
        The function get_cancer_status returns the cancer status of an object.
        :return: cancer: A boolean containing the cancer status.
        """
        return self.cancer

    def get_file_id(self):
        """
        The function get_file_ids returns the file_ids of an object.
        :return: file_ids: A String containing a file_id.
        """
        return self.file_ids

    def to_dict(self):
        """
        The function to_dict create a dictionary for all attributes of an object.
        :return: attribute_information: A dictionary containing all attributes for an object.
        """
        attribute_information = {
            "gender": self.gender,
            "days old": self.days_old,
            "race": self.race,
            "organ": self.organ,
            "disease_type": self.disease_type,
            "days_old_at_diagnosis": self.days_old_at_diagnosis,
            "exposures_years_smoked": self.exposures_years_smoked,
            "exposures_cigarettes_per_day": self.exposures_cigarettes_per_day,
            "file_ids": self.file_id
        }
        return attribute_information
