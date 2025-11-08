import os
import re
from pathlib import Path
import pandas as pd


class ImprovedSolidityAnalyzer:
    def __init__(self):
        self.results = []

    def remove_comments(self, content):
        """Remove comments and return clean code"""
        # Remove multi-line comments /* ... */
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        # Remove single-line comments //
        content = re.sub(r'//.*', '', content)
        return content

    def count_sloc_lloc(self, content):
        """Calculate SLOC and LLOC"""
        lines = content.split('\n')
        sloc = len(lines)

        # Calculate LLOC - logical lines of code (remove empty lines and comments)
        lloc = 0
        in_multiline_comment = False

        for line in lines:
            stripped = line.strip()

            # Skip empty lines
            if not stripped:
                continue

            # Handle multi-line comments
            if in_multiline_comment:
                if '*/' in stripped:
                    in_multiline_comment = False
                    # Check if there is code after the comment ends
                    after_comment = stripped.split('*/', 1)[1].strip()
                    if after_comment and not after_comment.startswith('//'):
                        lloc += 1
                continue

            # Skip single-line comments
            if stripped.startswith('//'):
                continue

            # Handle multi-line comment start
            if '/*' in stripped:
                in_multiline_comment = True
                # Check if there is code before the comment starts
                before_comment = stripped.split('/*')[0].strip()
                if before_comment:
                    lloc += 1
                continue

            lloc += 1

        return sloc, lloc

    def count_functions(self, content):
        """Count number of functions - improved version"""
        # Remove comments to avoid matching function in comments
        clean_content = self.remove_comments(content)

        # Match function definitions, including various modifiers and visibility
        function_pattern = r'\bfunction\s+([a-zA-Z_][a-zA-Z0-9_]*\s*)?\([^)]*\)'
        functions = re.findall(function_pattern, clean_content)

        # Exclude false matches in constructors and fallback/receive functions
        valid_functions = []
        for func in functions:
            func_name = func.strip() if func else ""
            # Exclude obvious false matches (empty function names might be constructors, etc.)
            if func_name and not func_name.startswith('('):
                valid_functions.append(func)

        return len(valid_functions)

    def count_state_variables(self, content):
        """Count state variables - improved version"""
        clean_content = self.remove_comments(content)
        lines = clean_content.split('\n')

        state_vars = 0
        in_contract = False
        in_function = False
        brace_count = 0

        # State variable pattern: type + variable name + semicolon or equal sign
        state_var_pattern = r'^\s*(\w+\s+)+(public|private|internal|constant|immutable)?\s*(\w+)\s*(=|;)'

        for line in lines:
            stripped = line.strip()

            # Detect contract start
            if re.match(r'^(contract|interface|library|abstract contract)\s+\w+', stripped):
                in_contract = True
                continue

            # Detect function start
            if in_contract and re.search(r'\bfunction\s+', stripped):
                in_function = True
                # Find the start of function body
                brace_count += stripped.count('{')
                continue

            if in_function:
                brace_count += stripped.count('{')
                brace_count -= stripped.count('}')
                if brace_count <= 0:
                    in_function = False
                    brace_count = 0
                continue

            # Inside contract but not in function, detect state variables
            if in_contract and not in_function and stripped:
                # Skip import, pragma, etc.
                if stripped.startswith(('import', 'pragma', 'using', 'struct', 'enum')):
                    continue

                # Match state variable declarations
                if re.search(state_var_pattern, stripped):
                    state_vars += 1

        return state_vars

    def analyze_solidity_file(self, file_path):
        """Analyze a single Solidity file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Calculate metrics
            sloc, lloc = self.count_sloc_lloc(content)
            nf = self.count_functions(content)
            state_vars = self.count_state_variables(content)

            return {
                'file_path': str(file_path),
                'sloc': sloc,
                'lloc': lloc,
                'nf': nf,
                'state_variables': state_vars
            }

        except Exception as e:
            print(f"Error analyzing file {file_path}: {e}")
            return None

    def analyze_project(self, project_path):
        """Analyze the entire project"""
        project_name = os.path.basename(project_path)
        sol_files = []

        # Recursively find all .sol files
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith('.sol'):
                    sol_files.append(os.path.join(root, file))

        if not sol_files:
            print(f"No .sol files found in project {project_name}")
            return

        print(f"Found {len(sol_files)} .sol files in project {project_name}")

        project_sloc = 0
        project_lloc = 0
        project_nf = 0
        project_sv = 0

        for sol_file in sol_files:
            result = self.analyze_solidity_file(sol_file)
            if result:
                project_sloc += result['sloc']
                project_lloc += result['lloc']
                project_nf += result['nf']
                project_sv += result['state_variables']

        # Only save project summary results
        self.results.append({
            'project': project_name,
            'sloc': project_sloc,
            'lloc': project_lloc,
            'nf': project_nf,
            'state_variables': project_sv
        })

        print(f"Project {project_name} analysis completed:")
        print(f"  SLOC: {project_sloc}")
        print(f"  LLOC: {project_lloc}")
        print(f"  Number of functions: {project_nf}")
        print(f"  Number of state variables: {project_sv}")
        print("-" * 50)

    def analyze_all_projects(self, base_directory):
        """Analyze all projects in the base directory"""
        base_path = Path(base_directory)

        if not base_path.exists():
            print(f"Directory {base_directory} does not exist")
            return

        # Get all subdirectories (each subdirectory is considered a project)
        projects = [d for d in base_path.iterdir() if d.is_dir()]

        if not projects:
            print(f"No project directories found in {base_directory}")
            return

        print(f"Found {len(projects)} projects, starting analysis...")
        print("=" * 60)

        for project in projects:
            self.analyze_project(project)

        # Generate summary report
        self.generate_report()

    def generate_report(self):
        """Generate analysis report"""
        if not self.results:
            print("No analysis results to generate report")
            return

        # Create DataFrame
        df = pd.DataFrame(self.results)

        # Save to CSV file
        output_file = "improved_solidity_analysis.csv"
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\nAnalysis report saved to: {output_file}")

        # Display project summary information
        print("\nProject Summary:")
        print("=" * 60)
        print(f"{'Project Name':<20} {'SLOC':<8} {'LLOC':<8} {'Functions':<10} {'State Vars':<10}")
        print("-" * 60)

        for row in self.results:
            print(
                f"{row['project']:<20} {row['sloc']:<8} {row['lloc']:<8} {row['nf']:<10} {row['state_variables']:<10}")


def main():
    # Set project folder path
    base_directory = "project_files"  # Change to your actual path

    analyzer = ImprovedSolidityAnalyzer()
    analyzer.analyze_all_projects(base_directory)


if __name__ == "__main__":
    main()