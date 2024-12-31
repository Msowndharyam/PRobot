import os
# from pylint import epylint as lint
import subprocess

def analyze_code(file_path):
    """
    Runs pylint on the specified file and prints the output.
    """
    try:
        #run pylint as a subprocess
        result = subprocess.run(
            ["pylint", file_path],
            capture_output=True,
            text=True,
        )
        #print pylint output
        print("Pylint Output:")
        print(result.stdout)
        print("Pylint Errors:")
        print(result.stderr)
    except FileNotFoundError:
        print("Pylint is not installed or not found in the environment.")
        
if __name__ == "__main__":
    analyze_code("analysis/example.py")#need to work on this
