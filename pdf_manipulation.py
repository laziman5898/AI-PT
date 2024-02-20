from reportlab.pdfgen import canvas

class Pdf:
    def __init__(self , pdf_name):
        #create the pdf with an A4 Pagesize (595.27, 841.89)
        self.pdf = canvas.Canvas(f"{pdf_name}.pdf",pagesize=(595.27, 841.89))
        self.title = f"{pdf_name}.pdf"

    def add_text(self,posx,posy,text):
        self.pdf.drawString(x=posx,y=posy,text=text)




    #def edit_pdf(self):
        #with open(self.title) as pdf:


    def save_pdf(self):
        self.pdf.showPage()
        self.pdf.save()