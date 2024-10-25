import os
from pylint import epylint as lint

def analyze_code(file_path):
    (pylint_stdout, pylint_stderr) = lint.py_run(file_path, return_std=True)
    print(pylint_stdout.getvalue())
    print(pylint_stderr.getvalue())

if __name__ == "__main__":
    #eg:analyze a Python file
    analyze_code("path/to/my/code.py") #need to work on this
