"""
OCR Utilities for document processing
"""

import cv2
import numpy as np
from PIL import Image

class OCRProcessor:
    """Handles OCR processing for images including handwriting detection."""
    
    def __init__(self):
        try:
            import pytesseract
            self.pytesseract = pytesseract
        except ImportError:
            self.pytesseract = None
            print("Warning: pytesseract not available")
    
    def detect_handwriting(self, image):
        """Detect if image contains handwriting."""
        try:
            # Convert PIL Image to numpy array
            img_array = np.array(image)
            
            # Convert to grayscale
            if len(img_array.shape) == 3:
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = img_array
            
            # Apply edge detection
            edges = cv2.Canny(gray, 50, 150)
            
            # Count edges
            edge_pixels = np.sum(edges > 0)
            total_pixels = edges.size
            edge_ratio = edge_pixels / total_pixels
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Handwriting typically has more irregular contours
            is_handwritten = edge_ratio > 0.05 and len(contours) > 20
            
            return {
                'is_handwritten': is_handwritten,
                'confidence': edge_ratio * 10,  # Normalize to 0-1 range
                'edge_ratio': edge_ratio,
                'contour_count': len(contours)
            }
        except Exception as e:
            return {
                'is_handwritten': False,
                'confidence': 0,
                'edge_ratio': 0,
                'error': str(e)
            }
    
    def extract_text(self, image, enhance=True):
        """Extract text from image using standard OCR."""
        if not self.pytesseract:
            return "OCR not available"
        
        try:
            if enhance:
                image = self._enhance_image(image)
            
            text = self.pytesseract.image_to_string(image)
            return text
        except Exception as e:
            return f"OCR error: {str(e)}"
    
    def extract_from_handwriting(self, image):
        """Extract text from handwritten image."""
        if not self.pytesseract:
            return "OCR not available"
        
        try:
            # Enhance for handwriting
            enhanced = self._enhance_for_handwriting(image)
            
            # Use specific OCR config for handwriting
            custom_config = r'--oem 3 --psm 6'
            text = self.pytesseract.image_to_string(enhanced, config=custom_config)
            return text
        except Exception as e:
            return f"Handwriting OCR error: {str(e)}"
    
    def extract_text_with_confidence(self, image):
        """Extract text with confidence scores."""
        if not self.pytesseract:
            return {'text': 'OCR not available', 'confidence': 0, 'word_count': 0}
        
        try:
            data = self.pytesseract.image_to_data(image, output_type=self.pytesseract.Output.DICT)
            
            # Filter by confidence
            text_parts = []
            confidences = []
            
            for i, conf in enumerate(data['conf']):
                if int(conf) > 30:  # Threshold
                    text_parts.append(data['text'][i])
                    confidences.append(int(conf))
            
            text = ' '.join(text_parts)
            avg_confidence = np.mean(confidences) if confidences else 0
            
            return {
                'text': text,
                'confidence': avg_confidence,
                'word_count': len(text_parts)
            }
        except Exception as e:
            return {
                'text': f"Error: {str(e)}",
                'confidence': 0,
                'word_count': 0
            }
    
    def _enhance_image(self, image):
        """Enhance image for better OCR."""
        try:
            # Convert PIL to numpy
            img_array = np.array(image)
            
            # Convert to grayscale
            if len(img_array.shape) == 3:
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = img_array
            
            # Apply thresholding
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Convert back to PIL
            return Image.fromarray(binary)
        except Exception:
            return image
    
    def _enhance_for_handwriting(self, image):
        """Enhance image specifically for handwriting recognition."""
        try:
            img_array = np.array(image)
            
            if len(img_array.shape) == 3:
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = img_array
            
            # Apply adaptive thresholding for handwriting
            binary = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )
            
            # Denoise
            denoised = cv2.fastNlMeansDenoising(binary)
            
            return Image.fromarray(denoised)
        except Exception:
            return image
