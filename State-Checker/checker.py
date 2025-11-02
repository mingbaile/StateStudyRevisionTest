import subprocess
import os
import sys

def main():
    input_dir = 'projects'
    output_dir = 'ASTJsonFiles'

    python_executable = sys.executable

    print(f"Generating AST files to ASTJsonFiles...")
    result = subprocess.run(
        [python_executable, 'generating_AST.py', '--input', input_dir, '--output', output_dir],
        capture_output=True, text=True, encoding='utf-8'
    )

    if result.returncode != 0:
        # print(f"Error during AST generation: {result.stderr}")
        return
    print(result.stdout)

    print("Starting the process of analyzing state variables...")
    result2 = subprocess.run(
        [python_executable, 'analyzing_state_variables.py', output_dir],
        capture_output=True, text=True, encoding='utf-8'
    )

    if result2.returncode != 0:
        print(f"Error during state variable analysis: {result2.stderr}")
        return
    print(result2.stdout)


if __name__ == "__main__":
    main()