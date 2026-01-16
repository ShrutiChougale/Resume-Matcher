import PyPDF2
import docx

def extract_text(file):
    if file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        return " ".join(page.extract_text() for page in reader.pages)

    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return " ".join(p.text for p in doc.paragraphs)

    else:
        return file.read().decode("utf-8")
