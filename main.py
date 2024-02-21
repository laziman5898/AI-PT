import os
from candidate import Candidate
from pdf_manipulation import Pdf
from openai import OpenAI
from db_connection import DB_Handler


api_key = os.environ.get("API_KEY")

pdf = Pdf("Testing")
#client = OpenAI(api_key=api_key)
database = DB_Handler()


person = Candidate()
person.bmi_classifier()
person.macro_calc()

database.info_add(person.info)
# person.info_stats_pdf_gen()
#
# print(person.kcal_breakdown)
#
# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are a nutrionist, helping a form of athlete to achieve there goals"},
#     {"role": "user", "content": f"Compose a meal plan for a day for me a movement director, who needs to achieve the following macronutrients "
#                                 f":protien:{person.kcal_breakdown['proteins'][0]},carbs:{person.kcal_breakdown['carbohydrates'][0]}, fats{person.kcal_breakdown['fats'][0]} "}
#   ]
# )
#
# response = completion.choices[0].message.content
# print(response)

#pdf.save_pdf()


