import io
import os
import docx
import PyPDF2

# File signature mappings
FILE_SIGNATURES = {
    "%PDF-": "application/pdf",
    b"\x89PNG\r\n\x1a\n": "image/png",
    b"PK\x03\x04": "application/zip",  # generic zip file
    b"PK\x03\x04\x14\x00\x06\x00": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # .docx
}

# Keywords for identifying resume and job descriptions
RESUME_KEYWORDS = ["Experience", "Education", "Skills", "Summary", "Objective"]
JD_KEYWORDS = ["Responsibilities", "Requirements", "Qualifications", "Job Description"]

def detect_file_type(file_path):
    mime_type = None
    with open(file_path, "rb") as f:
        header = f.read(32)  # Read the first 32 bytes
        for signature, mt in FILE_SIGNATURES.items():
            if isinstance(signature, str):
                if header.startswith(signature.encode()):
                    mime_type = mt
                    break
            else:
                if header.startswith(signature):
                    mime_type = mt
                    break

    if mime_type:
        text = extract_text_from_file(file_path)
        if text:
            resume_score = sum(keyword in text for keyword in RESUME_KEYWORDS)
            jd_score = sum(keyword in text for keyword in JD_KEYWORDS)

            if resume_score > jd_score and resume_score > 1:
                return "resume"
            elif jd_score > resume_score and jd_score > 1:
                return "job_description"
            else:
                return mime_type  # if content analysis is inconclusive, return mime type
    return None

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def extract_text_from_file(file_path):
    file_mime_type = detect_file_type(file_path)

    if file_mime_type == 'application/pdf' or file_mime_type == 'resume' or file_mime_type == 'job_description':
        return extract_text_from_pdf(file_path)
    elif file_mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file type")

class ResumeExtractorTool:
    def __init__(self):
        # self.__name__ = "ResumeExtractorTool"
        self.name = "resume_file_extractor"
        self.description = "Extracts text from resume files (PDF, DOCX)"

    def __call__(self, file_path: str) -> str:
        """Extracts text from a resume file."""
        try:
            return extract_text_from_file(file_path)
        except Exception as e:
            return f"Error extracting text from file: {str(e)}"