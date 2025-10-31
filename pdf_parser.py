import fitz  # PyMuPDF
import re
import json
from typing import List, Dict, Any

class DomainAgnosticPDFProcessor:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.requirements = []
    
    def extract_text_from_pdf(self) -> str:
        """Extract all text from PDF document without domain assumptions"""
        doc = fitz.open(self.pdf_path)
        full_text = ""
        
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            full_text += page.get_text()
        
        doc.close()
        return full_text
    
    def parse_requirements(self, text: str) -> List[Dict[str, Any]]:
        """Parse extracted text to identify and structure requirements generically"""
        requirements = []
        
        # Split text into logical sections
        sections = self._split_into_sections(text)
        
        requirement_id = 1
        for section in sections:
            if self._is_requirement_section(section):
                requirement = {
                    'id': f"REQ_{requirement_id:03d}",
                    'content': section.strip(),
                    'type': self._classify_requirement_type(section),
                    'testability_score': self._calculate_testability_score(section),
                    'validation_rules': self._extract_validation_rules(section),
                    'keywords': self._extract_keywords(section),
                    'source': f"PDF_Section_{requirement_id}"
                }
                requirements.append(requirement)
                requirement_id += 1
        
        return requirements
    
    def _split_into_sections(self, text: str) -> List[str]:
        """Split text into logical sections using universal patterns"""
        # Universal section patterns across domains
        section_patterns = [
            r'\n\d+\.\s',      # "1. Section"
            r'\n\d+\.\d+\.\s', # "1.1. Subsection"
            r'\n•\s',          # "• Bullet points"
            r'\n-\s',          # "- Bullet points"
            r'\n[A-Z][a-z]+:', # "Validation:", "Requirements:"
            r'\nRequirements?:',
            r'\nBusiness Rules?:',
            r'\nValidation:',
            r'\nFunctional:',
            r'\n\n[A-Z][A-Za-z\s]{10,}:',  # Section headers
        ]
        
        combined_pattern = '|'.join(section_patterns)
        sections = re.split(combined_pattern, text)
        
        # Filter out empty sections and very short text
        return [section.strip() for section in sections if len(section.strip()) > 30]
    
    def _is_requirement_section(self, text: str) -> bool:
        """Determine if a section contains testable requirements using universal patterns"""
        requirement_keywords = [
            'shall', 'must', 'should', 'will', 'validate', 'verify', 'check',
            'ensure', 'require', 'condition', 'rule', 'business rule',
            'when', 'if', 'then', 'field', 'value', 'parameter', 'input', 'output',
            'user can', 'system shall', 'application must', 'if', 'else', 'otherwise'
        ]
        
        text_lower = text.lower()
        keyword_count = sum(1 for keyword in requirement_keywords if keyword in text_lower)
        
        # Also check for imperative sentence structure
        has_imperative = any(text.strip().startswith(word) for word in ['Validate', 'Check', 'Ensure', 'Verify'])
        
        return keyword_count >= 2 or has_imperative or len(text.split('.')) >= 2
    
    def _classify_requirement_type(self, text: str) -> str:
        """Classify requirement type using universal characteristics"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['validate', 'verify', 'check', 'must be', 'should be']):
            return 'validation'
        elif any(word in text_lower for word in ['user', 'click', 'button', 'screen', 'page', 'navigate']):
            return 'user_interface'
        elif any(word in text_lower for word in ['calculate', 'compute', 'formula', 'algorithm']):
            return 'computation'
        elif any(word in text_lower for word in ['if', 'when', 'then', 'else', 'condition']):
            return 'business_rule'
        elif any(word in text_lower for word in ['api', 'endpoint', 'request', 'response', 'service']):
            return 'integration'
        elif any(word in text_lower for word in ['store', 'save', 'database', 'field', 'record']):
            return 'data_management'
        else:
            return 'functional'
    
    def _calculate_testability_score(self, text: str) -> int:
        """Calculate how testable a requirement is (1-10 scale)"""
        score = 0
        text_lower = text.lower()
        
        # Positive indicators
        if any(word in text_lower for word in ['validate', 'verify', 'check']):
            score += 3
        if any(word in text_lower for word in ['must', 'shall', 'will']):
            score += 2
        if any(word in text_lower for word in ['if', 'when', 'then']):
            score += 2
        if any(word in text_lower for word in ['value', 'field', 'parameter']):
            score += 2
        if any(word in text_lower for word in ['number', 'string', 'date', 'boolean']):
            score += 1
        if any(word in text_lower for word in ['greater than', 'less than', 'between', 'equal to']):
            score += 2
        
        # Negative indicators
        if len(text.strip()) < 20:
            score -= 2
        if any(word in text_lower for word in ['may', 'could', 'should consider']):
            score -= 1
        
        return min(10, max(1, score))
    
    def _extract_validation_rules(self, text: str) -> List[str]:
        """Extract specific validation rules from requirement text"""
        rules = []
        
        # Universal validation patterns
        patterns = [
            r'must be between (.*?) and (.*?)',
            r'shall be (.*?)',
            r'must (.*?)',
            r'should be (.*?)',
            r'validate that (.*?)',
            r'check if (.*?)',
            r'ensure (.*?)',
            r'if (.*?) then (.*?)',
            r'when (.*?) then (.*?)',
            r'greater than (.*?)',
            r'less than (.*?)',
            r'equal to (.*?)',
            r'contains? (.*?)',
            r'matches? (.*?)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            rules.extend(matches)
        
        return rules
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract relevant keywords from requirement text"""
        # Common stop words to exclude
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        keywords = [word for word in words if word not in stop_words and word.isalpha()]
        
        # Return unique keywords, limited to top 10 most relevant
        from collections import Counter
        return [word for word, count in Counter(keywords).most_common(10)]
    
    def process_pdf(self) -> List[Dict[str, Any]]:
        """Main method to process PDF and extract requirements generically"""
        print(" Extracting text from PDF...")
        text = self.extract_text_from_pdf()
        
        print(" Parsing requirements...")
        self.requirements = self.parse_requirements(text)
        
        print(f" Extracted {len(self.requirements)} requirements from PDF")
        return self.requirements
    
    def save_requirements(self, output_path: str):
        """Save extracted requirements to JSON file"""
        with open(output_path, 'w') as f:
            json.dump(self.requirements, f, indent=2)
        print(f" Requirements saved to {output_path}")
    
    def print_summary(self):
        """Print summary of extracted requirements"""
        if not self.requirements:
            print("No requirements extracted yet. Run process_pdf() first.")
            return
        
        print(f"\n EXTRACTION SUMMARY:")
        print(f"   Total requirements: {len(self.requirements)}")
        
        type_counts = {}
        testability_scores = []
        
        for req in self.requirements:
            req_type = req['type']
            type_counts[req_type] = type_counts.get(req_type, 0) + 1
            testability_scores.append(req['testability_score'])
        
        print(f"   Requirement types:")
        for req_type, count in type_counts.items():
            print(f"     - {req_type}: {count}")
        
        avg_testability = sum(testability_scores) / len(testability_scores)
        print(f"   Average testability score: {avg_testability:.1f}/10")
        
        # Show sample requirements
        print(f"\n   Sample requirements:")
        for i, req in enumerate(self.requirements[:3]):
            print(f"     {i+1}. [{req['type']}] {req['content'][:80]}...")

# Example usage
if __name__ == "__main__":
    # Process any PDF - healthcare, finance, e-commerce, etc.
    processor = DomainAgnosticPDFProcessor("genai-testcase-generator/business_requirements_2.pdf")
    requirements = processor.process_pdf()
    
    # Save and show summary
    processor.save_requirements("genai-testcase-generator/extracted_requirements_2.json")
    processor.print_summary()
