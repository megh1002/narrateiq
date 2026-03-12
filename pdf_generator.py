from fpdf import FPDF
import re

def clean_text(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = text.replace('\u2014', '-')
    text = text.replace('\u2013', '-')
    text = text.replace('\u2018', "'")
    text = text.replace('\u2019', "'")
    text = text.replace('\u201c', '"')
    text = text.replace('\u201d', '"')
    text = text.replace('\u2022', '-')
    # Remove any remaining non-latin characters
    text = text.encode('latin-1', 'replace').decode('latin-1')
    return text


class ReportPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(30, 30, 30)
        self.set_x(10)
        self.cell(0, 12, "NarrateIQ - AI Analyst Report", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


def generate_pdf(report_text: str, dataset_name: str = "Dataset") -> bytes:
    pdf = ReportPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(15, 15, 15)

    pdf.set_font("Helvetica", "I", 11)
    pdf.set_text_color(100, 100, 100)
    pdf.set_x(15)
    pdf.multi_cell(0, 8, f"Dataset: {clean_text(dataset_name)}")
    pdf.ln(4)

    lines = report_text.split('\n')

    for line in lines:
        line = clean_text(line.strip())

        if not line:
            pdf.ln(3)
            continue

        if re.match(r'^\d+\.', line):
            pdf.ln(4)
            pdf.set_font("Helvetica", "B", 12)
            pdf.set_text_color(30, 30, 100)
            pdf.set_x(15)
            pdf.multi_cell(180, 8, line)
            pdf.ln(2)

        elif line.startswith('-') or line.startswith('•'):
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(40, 40, 40)
            pdf.set_x(20)
            pdf.multi_cell(170, 7, f"- {line.lstrip('-').strip()}")

        else:
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(40, 40, 40)
            pdf.set_x(15)
            pdf.multi_cell(180, 7, line)

    return bytes(pdf.output())