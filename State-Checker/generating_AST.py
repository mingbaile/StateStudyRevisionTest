import os
import subprocess
import argparse

def get_sol_files(dir_path):
    sol_files = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.sol'):
                sol_files.append(os.path.join(root, file))
    return sol_files

def parse_solidity_with_node(sol_file, input_dir, output_dir):
    result = subprocess.run(
        ['node', 'parse_solidity.js', sol_file, input_dir, output_dir],
        capture_output=True, text=True, encoding='utf-8'
    )

    if result.returncode == 0:
        # print(f"AST for {sol_file} saved successfully.")
        return True
    else:
        # print(f"Error processing {sol_file}: {result.stderr}")
        return False

def process_sol_files(testdir, output_dir):
    sol_files = get_sol_files(testdir)

    failed_files = []

    for sol_file in sol_files:
        if not parse_solidity_with_node(sol_file, testdir, output_dir):
            failed_files.append(sol_file)

    if failed_files:
        print(f"Failed to process the following files: {failed_files}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process Solidity files to generate AST.')
    parser.add_argument('--input', required=True, help='Input directory path containing Solidity files')
    parser.add_argument('--output', required=True, help='Output directory path to save AST files')

    args = parser.parse_args()

    process_sol_files(args.input, args.output)
