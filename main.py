from candidate import Candidate

person = Candidate()

def BMI():
    height = input("What is your height")
    person.set_height(height)
    weight = input("What is your weight")
    person.set_weight(weight)
    print(f'Height = {person.height} & Weight = {person.weight}')

BMI()