from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime

def create_pdf(query, insights, file_path):

    filename = "VizAI_Report.pdf"

    c = canvas.Canvas(filename, pagesize=letter)

    c.drawString(100, 760, "VizAI - Data Visualization Report")
    c.drawString(100, 740, str(datetime.datetime.now()))

    c.drawString(100, 700, f"Query: {query}")

    c.drawString(100, 660, "Insights:")
    c.drawString(100, 640, insights[:100])

    c.drawString(100, 600, "Chart saved as interactive HTML file.")

    c.save()
    return filename
