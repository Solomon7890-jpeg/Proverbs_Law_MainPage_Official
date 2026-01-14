"""
PDF Processing Utilities
"""

import io

class PDFProcessor:
    """Handles PDF text extraction."""
    
    def __init__(self):
        try:
            import PyPDF2
            self.PyPDF2 = PyPDF2
        except ImportError:
            self.PyPDF2 = None
            print("Warning: PyPDF2 not available")
    
    def extract_text(self, pdf_file):
        """Extract text from PDF file object."""
        if not self.PyPDF2:
            return "PDF processing not available. Please install PyPDF2."
        
        try:
            reader = self.PyPDF2.PdfReader(pdf_file)
            text = ""
            
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            return f"Error extracting PDF text: {str(e)}"
    
    def extract_text_from_bytes(self, pdf_bytes):
        """Extract text from PDF bytes."""
        if not self.PyPDF2:
            return "PDF processing not available. Please install PyPDF2."
        
        try:
            pdf_file = io.BytesIO(pdf_bytes)
            reader = self.PyPDF2.PdfReader(pdf_file)
            text = ""
            
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            return f"Error extracting PDF text: {str(e)}"
