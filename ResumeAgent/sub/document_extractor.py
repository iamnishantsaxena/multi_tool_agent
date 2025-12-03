"""
Document extraction utility for handling multiple file formats.

Supports: PDF, DOCX, TXT, and plain text extraction.
Provides classification of documents as Resume or Job Description.
"""

import io
import os
import docx
import PyPDF2


class DocumentExtractorTool:
    """Extracts and classifies text from various document formats."""
    
    # Keywords for identifying resume vs job description
    RESUME_KEYWORDS = {
        "experience", "education", "skills", "summary", "objective",
        "work history", "employment", "certifications", "projects"
    }
    
    JD_KEYWORDS = {
        "responsibilities", "requirements", "qualifications", "job description",
        "about the role", "what you'll do", "we're looking for", "must have",
        "nice to have", "benefits", "perks"
    }
    
    def __init__(self):
        self.name = "document_extractor"
        self.description = "Extracts and classifies text from resume and job description files (PDF, DOCX, TXT)"

    def __call__(self, file_path: str) -> str:
        """Extracts text from a document file."""
        try:
            return self.extract_text(file_path)
        except Exception as e:
            return f"Error extracting text from file: {str(e)}"

    @staticmethod
    def extract_text(file_path: str) -> str:
        """Extract text based on file extension."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.pdf':
            return DocumentExtractorTool._extract_from_pdf(file_path)
        elif file_ext == '.docx':
            return DocumentExtractorTool._extract_from_docx(file_path)
        elif file_ext in ['.txt', '.md']:
            return DocumentExtractorTool._extract_from_text(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")

    @staticmethod
    def _extract_from_pdf(file_path: str) -> str:
        """Extract text from PDF file."""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
        except Exception as e:
            raise ValueError(f"Failed to extract PDF: {str(e)}")
        return text

    @staticmethod
    def _extract_from_docx(file_path: str) -> str:
        """Extract text from DOCX file."""
        text = ""
        try:
            doc = docx.Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            raise ValueError(f"Failed to extract DOCX: {str(e)}")
        return text

    @staticmethod
    def _extract_from_text(file_path: str) -> str:
        """Extract text from TXT or MD file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise ValueError(f"Failed to extract text: {str(e)}")

    def classify_document(self, text: str) -> str:
        """
        Classify document as 'resume', 'job_description', or 'unknown'.
        
        Args:
            text: Document text content
            
        Returns:
            Classification string: 'resume', 'job_description', or 'unknown'
        """
        text_lower = text.lower()
        
        # Count keyword occurrences (case-insensitive)
        resume_score = sum(1 for keyword in self.RESUME_KEYWORDS if keyword in text_lower)
        jd_score = sum(1 for keyword in self.JD_KEYWORDS if keyword in text_lower)
        
        # Classification logic
        if resume_score > jd_score and resume_score >= 2:
            return "resume"
        elif jd_score > resume_score and jd_score >= 2:
            return "job_description"
        else:
            return "unknown"
