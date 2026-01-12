"""
Simple CV Parser - Extract skills from CV documents
"""
import re
from pypdf import PdfReader

class CVParser:
    def __init__(self):
        self.common_sections = [
            'skills', 'technical skills', 'expertise', 'competencies',
            'technologies', 'tools', 'programming languages'
        ]
    
    def parse_pdf(self, file_path):
        """Extract text from PDF CV"""
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error parsing PDF: {e}")
            return ""
    
    def parse_text(self, file_path):
        """Extract text from TXT CV"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error parsing TXT: {e}")
            return ""
    
    def extract_name(self, cv_text):
        """Simple name extraction - first line usually"""
        lines = [line.strip() for line in cv_text.split('\n') if line.strip()]
        if lines:
            # Return first non-empty line as name
            return lines[0][:50]  # Limit to 50 chars
        return "Unknown"
    
    def extract_email(self, cv_text):
        """Extract email from CV"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(email_pattern, cv_text)
        return match.group(0) if match else None
    
    def extract_phone(self, cv_text):
        """Extract phone number from CV"""
        phone_pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
        match = re.search(phone_pattern, cv_text)
        return match.group(0) if match else None
    
    def get_cv_summary(self, cv_text):
        """Get summary info from CV"""
        return {
            "name": self.extract_name(cv_text),
            "email": self.extract_email(cv_text),
            "phone": self.extract_phone(cv_text),
            "length": len(cv_text)
        }
