import ollama
import json
import os
from typing import List, Dict
from datetime import datetime

class CucumberTestGenerator:
    def __init__(self, vector_store, model: str = "mistral:7b"):
        self.vector_store = vector_store
        self.model = model
        self.output_dir = "generated_features"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def create_domain_context_prompt(self, requirement: Dict, similar_reqs: List[Dict]) -> str:
        """Create a prompt that understands domain context from similar requirements"""
        
        # Build context from similar requirements
        context_lines = []
        for i, req in enumerate(similar_reqs, 1):
            context_lines.append(f"{i}. {req['content'][:200]}...")
            context_lines.append(f"   Type: {req['metadata']['type']}, Score: {req['metadata']['testability_score']}")
        
        context = "\n".join(context_lines)
        
        prompt = f"""<s>[INST] You are an expert QA engineer. Generate comprehensive Cucumber/Gherkin test scenarios based on the business requirement.

**CONTEXT FROM RELATED REQUIREMENTS:**
{context}

**GENERATION RULES:**
1. Analyze the domain from the requirements context
2. Create realistic test scenarios with appropriate domain terminology
3. Include both positive and negative test cases
4. Use proper Gherkin syntax: Feature, Scenario, Given/When/Then
5. Include data tables where appropriate for test data
6. Cover boundary conditions and error scenarios
7. Make scenarios executable and specific

**REQUIREMENT TO TEST:**
ID: {requirement['id']}
Type: {requirement['type']}
Testability: {requirement['testability_score']}/10
Content: {requirement['content']}

**Generate 2-4 comprehensive Cucumber scenarios.** Focus on the specific validation rules and business logic.
Respond with clean Gherkin syntax only, no explanations. [/INST]"""

        return prompt
    
    def generate_cucumber_tests(self, requirement: Dict) -> Dict:
        """Generate Cucumber tests for a single requirement"""
        
        print(f"Generating tests for {requirement['id']} ({requirement['type']})...")
        
        # Find similar requirements for context
        similar_reqs = self.vector_store.search_similar_requirements(
            requirement['content'], 
            n_results=3
        )
        
        # Create contextual prompt
        prompt = self.create_domain_context_prompt(requirement, similar_reqs)
        
        try:
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'temperature': 0.1,
                    'top_p': 0.9,
                    'num_ctx': 8192
                }
            )
            
            return {
                'success': True,
                'requirement_id': requirement['id'],
                'requirement_type': requirement['type'],
                'cucumber_features': response['response'],
                'similar_requirements_count': len(similar_reqs),
                'testability_score': requirement['testability_score']
            }
            
        except Exception as e:
            return {
                'success': False,
                'requirement_id': requirement['id'],
                'error': str(e),
                'similar_requirements_count': len(similar_reqs)
            }
    
    def save_cucumber_file(self, content: str, requirement: Dict):
        """Save generated Cucumber tests to feature file"""
        # Create filename from requirement ID and type
        filename = f"{requirement['id']}_{requirement['type']}.feature"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        return filepath
    
    def generate_all_tests(self, requirements: List[Dict]):
        """Generate tests for all requirements and create summary report"""
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'total_requirements': len(requirements),
            'successful_generations': 0,
            'failed_generations': 0,
            'generated_files': [],
            'details': []
        }
        
        print(f"\nGenerating Cucumber tests for {len(requirements)} requirements...")
        print("=" * 60)
        
        for i, requirement in enumerate(requirements, 1):
            print(f"\nProcessing {i}/{len(requirements)}: {requirement['id']} ({requirement['type']})")
            print(f"   Testability: {requirement['testability_score']}/10")
            print(f"   Content: {requirement['content'][:80]}...")
            
            # Generate Cucumber tests
            result = self.generate_cucumber_tests(requirement)
            
            if result['success']:
                results['successful_generations'] += 1
                
                # Save to feature file
                filepath = self.save_cucumber_file(result['cucumber_features'], requirement)
                results['generated_files'].append(filepath)
                
                # Add to details
                result_detail = {
                    'requirement_id': requirement['id'],
                    'type': requirement['type'],
                    'testability_score': requirement['testability_score'],
                    'status': 'success',
                    'file_path': filepath,
                    'similar_requirements_used': result['similar_requirements_count']
                }
                results['details'].append(result_detail)
                
                print(f"    Generated: {os.path.basename(filepath)}")
                print(f"    Used {result['similar_requirements_count']} similar requirements for context")
                
                # Show sample of generated content
                lines = result['cucumber_features'].split('\n')
                print("   Sample:")
                for line in lines[:4]:
                    if line.strip():
                        print(f"      {line}")
                if len(lines) > 4:
                    print("      ...")
                    
            else:
                results['failed_generations'] += 1
                result_detail = {
                    'requirement_id': requirement['id'],
                    'type': requirement['type'],
                    'status': 'failed',
                    'error': result['error'],
                    'similar_requirements_used': result['similar_requirements_count']
                }
                results['details'].append(result_detail)
                print(f"   Failed: {result['error']}")
        
        # Save generation report
        self._save_generation_report(results)
        self._print_summary_report(results)
        
        return results
    
    def _save_generation_report(self, results: Dict):
        """Save detailed generation report"""
        report_file = f"generation_report_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        with open(report_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n Detailed report saved: {report_file}")
    
    def _print_summary_report(self, results: Dict):
        """Print summary of test generation results"""
        print("\n" + "=" * 60)
        print(" CUCUMBER TEST GENERATION SUMMARY")
        print("=" * 60)
        print(f" Total Requirements: {results['total_requirements']}")
        print(f" Successful: {results['successful_generations']}")
        print(f" Failed: {results['failed_generations']}")
        
        # Breakdown by requirement type
        type_success = {}
        for detail in results['details']:
            if detail['status'] == 'success':
                req_type = detail['type']
                type_success[req_type] = type_success.get(req_type, 0) + 1
        
        print(f"\n Success by Requirement Type:")
        for req_type, count in type_success.items():
            print(f"   - {req_type}: {count} generated")
        
        print(f"\n Generated Feature Files:")
        for file_path in results['generated_files']:
            print(f"   - {os.path.basename(file_path)}")
        
        print(f"\n All feature files saved in: {self.output_dir}/")

# Main execution function
def main():
    """Main function to run the complete test generation pipeline"""
    
    # Load extracted requirements
    try:
        with open("aiqa-generator-ds/extracted_requirements/extracted_requirements.json", "r") as f:
            requirements = json.load(f)
    except FileNotFoundError:
        print(" extracted_requirements.json not found. Run PDF processor first.")
        return
    
    # Initialize vector store
    from vector_store import RequirementVectorStore
    vector_store = RequirementVectorStore()
    
    vector_store.add_requirements(requirements)

    # Add requirements to vector store (if not already done)
    if len(vector_store.collection.get()['ids']) == 0:
        vector_store.add_requirements(requirements)
    
    # Initialize and run test generator
    generator = CucumberTestGenerator(vector_store)
    
    # Generate tests for all requirements
    results = generator.generate_all_tests(requirements)
    
    print(f"\n Pipeline completed! Check '{generator.output_dir}' for Cucumber feature files.")

if __name__ == "__main__":
    main()
