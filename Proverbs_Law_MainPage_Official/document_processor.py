"""
Document Processing Module for ProVerBs Law
Adapted from Streamlit to work with Gradio
"""

import io
import requests
from PIL import Image
import tempfile
import os
import uuid
from datetime import datetime
import re

class DocumentProcessor:
    """Handles processing of various document types including files, URLs, and direct text input."""
    
    def __init__(self):
        try:
            from utils.ocr_utils import OCRProcessor
            self.ocr_processor = OCRProcessor()
        except ImportError:
            self.ocr_processor = None
            print("Warning: OCR utilities not available")
            
        try:
            from utils.pdf_utils import PDFProcessor
            self.pdf_processor = PDFProcessor()
        except ImportError:
            self.pdf_processor = None
            print("Warning: PDF utilities not available")
    
    def process_file(self, file_path):
        """Process an uploaded file and extract text content."""
        try:
            # Get file type from extension
            filename = os.path.basename(file_path)
            ext = os.path.splitext(filename)[1].lower()
            
            # Create a unique ID for this document
            doc_id = str(uuid.uuid4())
            
            # Process based on file type
            if ext == ".pdf":
                content = self._process_pdf(file_path)
            elif ext in [".png", ".jpg", ".jpeg", ".gif", ".bmp"]:
                content = self._process_image(file_path)
            elif ext == ".txt":
                content = self._process_text_file(file_path)
            elif ext == ".docx":
                content = self._process_docx(file_path)
            else:
                return None, f"Unsupported file type: {ext}"
            
            if content:
                return {
                    'id': doc_id,
                    'filename': filename,
                    'content': content,
                    'file_type': ext,
                    'upload_date': datetime.now().isoformat(),
                    'source_type': 'file_upload'
                }, None
            else:
                return None, f"Failed to extract content from {filename}"
                
        except Exception as e:
            return None, f"Error processing file: {str(e)}"
    
    def process_url(self, url):
        """Process content from a URL."""
        try:
            # Basic URL validation
            if not url.startswith(('http://', 'https://')):
                return None, "Please enter a valid URL starting with http:// or https://"
            
            # Fetch content from URL
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            content_type = response.headers.get('content-type', '').lower()
            
            if 'text/html' in content_type or 'text/plain' in content_type:
                content = self._extract_text_from_html(response.text)
            elif 'application/pdf' in content_type:
                content = self._process_pdf_from_bytes(response.content)
            else:
                return None, f"Unsupported content type: {content_type}"
            
            if content:
                doc_id = str(uuid.uuid4())
                return {
                    'id': doc_id,
                    'filename': f"URL_Content_{url.split('/')[-1] or 'webpage'}",
                    'content': content,
                    'file_type': content_type,
                    'upload_date': datetime.now().isoformat(),
                    'source_type': 'url',
                    'source_url': url
                }, None
            else:
                return None, "Failed to extract content from URL"
                
        except requests.RequestException as e:
            return None, f"Error fetching URL: {str(e)}"
        except Exception as e:
            return None, f"Error processing URL content: {str(e)}"
    
    def process_text(self, text_content, source_name="Direct Input"):
        """Process direct text input."""
        try:
            if not text_content.strip():
                return None, "Please enter some text to process"
            
            doc_id = str(uuid.uuid4())
            return {
                'id': doc_id,
                'filename': source_name,
                'content': text_content.strip(),
                'file_type': 'text/plain',
                'upload_date': datetime.now().isoformat(),
                'source_type': 'direct_input'
            }, None
            
        except Exception as e:
            return None, f"Error processing text input: {str(e)}"
    
    def _process_pdf(self, file_path):
        """Extract text from PDF file."""
        try:
            if self.pdf_processor:
                with open(file_path, 'rb') as f:
                    return self.pdf_processor.extract_text(f)
            else:
                # Fallback to PyPDF2 if available
                try:
                    import PyPDF2
                    text = ""
                    with open(file_path, 'rb') as f:
                        reader = PyPDF2.PdfReader(f)
                        for page in reader.pages:
                            text += page.extract_text() + "\n"
                    return text
                except ImportError:
                    return "PDF processing not available. Please install PyPDF2."
        except Exception as e:
            return f"Error processing PDF: {str(e)}"
    
    def _process_pdf_from_bytes(self, pdf_bytes):
        """Extract text from PDF bytes."""
        try:
            if self.pdf_processor:
                return self.pdf_processor.extract_text_from_bytes(pdf_bytes)
            else:
                try:
                    import PyPDF2
                    text = ""
                    pdf_file = io.BytesIO(pdf_bytes)
                    reader = PyPDF2.PdfReader(pdf_file)
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
                    return text
                except ImportError:
                    return "PDF processing not available. Please install PyPDF2."
        except Exception as e:
            return f"Error processing PDF from URL: {str(e)}"
    
    def _process_image(self, file_path):
        """Extract text from image using OCR."""
        try:
            image = Image.open(file_path)
            
            if self.ocr_processor:
                # Try handwriting detection first
                handwriting_info = self.ocr_processor.detect_handwriting(image)
                
                if handwriting_info['is_handwritten']:
                    text = self.ocr_processor.extract_from_handwriting(image)
                    if not text.strip():
                        text = self.ocr_processor.extract_text(image, enhance=True)
                else:
                    text = self.ocr_processor.extract_text(image, enhance=True)
                
                if not text.strip():
                    confidence_result = self.ocr_processor.extract_text_with_confidence(image)
                    text = confidence_result['text']
            else:
                # Fallback to basic pytesseract if available
                try:
                    import pytesseract
                    text = pytesseract.image_to_string(image)
                except ImportError:
                    return "OCR processing not available. Please install pytesseract."
            
            if not text.strip():
                return "No text could be extracted from the image."
            
            return text
            
        except Exception as e:
            return f"Error processing image: {str(e)}"
    
    def _process_text_file(self, file_path):
        """Extract text from plain text file."""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # Try to decode as UTF-8, fall back to other encodings if needed
            try:
                text = content.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    text = content.decode('latin-1')
                except UnicodeDecodeError:
                    text = content.decode('utf-8', errors='ignore')
            
            return text
            
        except Exception as e:
            return f"Error processing text file: {str(e)}"
    
    def _process_docx(self, file_path):
        """Extract text from Word document."""
        try:
            try:
                from docx import Document
                doc = Document(file_path)
                text = "\n".join([para.text for para in doc.paragraphs])
                return text
            except ImportError:
                return "Word document processing requires python-docx. Please install it or convert to PDF."
            
        except Exception as e:
            return f"Error processing Word document: {str(e)}"
    
    def _extract_text_from_html(self, html_content):
        """Extract text content from HTML."""
        try:
            # Remove script and style elements
            clean_html = re.sub(r'<(script|style)[^<]*?</\1>', '', html_content, flags=re.IGNORECASE | re.DOTALL)
            
            # Remove HTML tags
            text = re.sub(r'<[^>]+>', '', clean_html)
            
            # Clean up whitespace
            text = re.sub(r'\s+', ' ', text).strip()
            
            # Limit length for processing
            if len(text) > 10000:
                text = text[:10000] + "..."
            
            return text
            
        except Exception as e:
            return f"Error extracting text from HTML: {str(e)}"
