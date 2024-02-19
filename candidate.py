class Candidate:
    def __init__(self):

        self.info = {
            'height': float(input("Height in CM \n" )),
            'weight': float(input("Weight in KG \n")),
            'gender': input("Gender | M or F ? \n"),
            'age' : int(input("Age plsss?? \n"))
        }
        self.info["BMI"] = self.info['weight'] / ((self.info['height']/100) ** 2)


        ## --------- HEIGHTS --------#
        self.height_ft = self.info['height']/30.48
        self.height_m = self.info['height']/100

    def bmi_classifier(self):
        if self.info["BMI"]< 18.5:
            self.info['BMI_classifier'] = "Underweight"
        elif 18.5 < self.info["BMI"] < 24.9:
            self.info['BMI_classifier'] = "Healthy"
        elif 25 < self.info["BMI"] < 29.9:
            self.info['BMI_classifier'] = "Overweight"
        elif 30 < self.info["BMI"] <39.9 :
            self.info['BMI_classifier'] = "Obese"
        elif self.info["BMI"] >= 40:
            self.info['BMI_classifier'] = "Serverly Obese"





