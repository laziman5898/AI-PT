from candidate import Candidate

person = Candidate()

print(f'BMI : {person.info["BMI"]} \n'
      f'Height : {person.info["height"]}'
)

person.bmi_classifier()

print(person.info['BMI_classifier'])