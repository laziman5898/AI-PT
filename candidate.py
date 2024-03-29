from pdf_manipulation import Pdf
from db_connection import DB_Handler


class Candidate:
    def __init__(self , data):

        self.kcal_breakdown = None
        self.db = DB_Handler()
        self.info = {
            'height': float(data['height']),
            'weight': float(data['weight']),
            'gender': data['gender'],
            'age': data['age']
        }
        self.info["BMI"] = (self.info['weight'] / ((self.info['height'] / 100) ** 2)).__round__(2)

        ## --------- HEIGHTS --------#
        self.height_ft = self.info['height'] / 30.48
        self.height_m = self.info['height'] / 100

    def bmi_classifier(self):
        if self.info["BMI"] < 18.5:
            self.info['BMI_classifier'] = "Underweight"
        elif 18.5 < self.info["BMI"] < 24.9:
            self.info['BMI_classifier'] = "Healthy"
        elif 25 < self.info["BMI"] < 29.9:
            self.info['BMI_classifier'] = "Overweight"
        elif 30 < self.info["BMI"] < 39.9:
            self.info['BMI_classifier'] = "Obese"
        elif self.info["BMI"] >= 40:
            self.info['BMI_classifier'] = "Serverly Obese"
    def set_goals(self,goal,lifestyle):
        self.info['goal'] = goal
        self.info['lifestyle'] = lifestyle

    def macro_calc(self):
        activity_mapper = {1: 1.2,
                           2: 1.375,
                           3: 1.550,
                           4: 1.725,
                           5: 1.9}


        if self.info["gender"].upper() == "MALE":
            self.info["BMR"] = (self.info["weight"] * 10) + (6.25 * self.info["height"]) - (5 * self.info["age"]) + 5
        elif self.info["gender"].upper() == "FEMALE":
            self.info["BMR"] = (self.info["weight"] * 10) + (6.25 * self.info["height"]) - (5 * self.info["age"]) - 161

        self.info["BMR"] = self.info["BMR"] * activity_mapper[self.info["lifestyle"]]

        if self.info["goal"] == "LW":
            self.info["Kcal Goal"] = self.info["BMR"] - (self.info["BMR"] / 100 * 15)

            self.info['kcal_breakdown']= {"carbohydrates": [int((self.info["Kcal Goal"] * 0.4) / 4), int(self.info["Kcal Goal"] * 0.4)],
                                   "proteins": [int((self.info["Kcal Goal"] * 0.4) / 4), int(self.info["Kcal Goal"] * 0.4)],
                                   "fats": [int((self.info["Kcal Goal"] * 0.2) / 9), int(self.info["Kcal Goal"] * 0.2)]}

        elif self.info["goal"] == "M":
            self.info["Kcal Goal"] = self.info["BMR"]
            self.info['kcal_breakdown'] = {"carbohydrates": [int((self.info["Kcal Goal"] * 0.4) / 4), int(self.info["Kcal Goal"] * 0.4)],
                                   "proteins": [int((self.info["Kcal Goal"] * 0.3) / 4), int(self.info["Kcal Goal"] * 0.3)],
                                   "fats": [int((self.info["Kcal Goal"] * 0.3) / 9), int(self.info["Kcal Goal"] * 0.3)]}
        elif self.info["goal"] == "GW":
            self.info["Kcal Goal"] = self.info["BMR"] + 500
            self.info['kcal_breakdown'] = {"carbohydrates": [int((self.info["Kcal Goal"] * 0.4) / 4), int(self.info["Kcal Goal"] * 0.4)],
                                   "proteins": [int((self.info["Kcal Goal"] * 0.3) / 4), int(self.info["Kcal Goal"] * 0.3)],
                                   "fats": [int((self.info["Kcal Goal"] * 0.3) / 9), int(self.info["Kcal Goal"] * 0.3)]}

    def info_stats_pdf_gen(self, name):
        new_pdf = Pdf(f"{name} BMI Stats")
        x_cursor_pdf = 50
        y_cursor_pdf = 700
        for i in self.info:
            new_pdf.add_text(posx=x_cursor_pdf, posy=y_cursor_pdf, text=f"{i} : {self.info[i]}")
            y_cursor_pdf -= 50

        new_pdf.save_pdf()

    def print_person(self):
        print(self.info)
