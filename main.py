from candidate import Candidate
from pdf_manipulation import Pdf

pdf = Pdf("Testing")


person = Candidate()
person.bmi_classifier()
person.macro_calc()
person.info_stats_pdf_gen()

print(person.kcal_breakdown)


#pdf.save_pdf()


