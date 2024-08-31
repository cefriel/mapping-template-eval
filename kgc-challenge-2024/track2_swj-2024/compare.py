import sys
import os
import tempfile

def sort_file(file_path):
    """Sort a file and save it as a new sorted temporary file."""
    lines = []
    with open(file_path, 'r', encoding='utf-8') as file:
        print(file_path)
        c = 0
        not_empty_lines = 0
        for line in file:
            stripped_line = line.strip()
            if stripped_line:
                lines.append(stripped_line)
                not_empty_lines += 1
            c += 1
        print(f"Filepath: {file_path}, Total lines: {c}, Not empty: {not_empty_lines}")
    
    # Sort lines
    lines.sort()

    # Create a temporary file to store sorted data
    temp_fd, temp_path = tempfile.mkstemp()
    with os.fdopen(temp_fd, 'w', encoding='utf-8') as temp_file:
        for line in lines:
            temp_file.write(f"{line}\n")
    
    return temp_path

def compare_sorted_files(file1_path, file2_path):
    """Compare two sorted files line by line."""
    equal = True
    try:
        with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:
            for line1, line2 in zip(file1, file2):
                if line1 != line2:
                    print(f"{line1},{line2}")
                    equal = False
        return equal
    finally:
        # Clean up temporary files
        os.remove(file1_path)
        os.remove(file2_path)
        print("Sorted Files Deleted!")

import os

mapping_template_path = os.getenv('MAPPING_TEMPLATE')
expected_path = os.getenv('EXPECTED')

file1 = mapping_template_path
file2 = expected_path
print("===============")
print(f"Compare {file1} and {file2}")

sorted_file1_path = sort_file(file1)
sorted_file2_path = sort_file(file2)    

print("Sorting finished")

result = compare_sorted_files(sorted_file1_path, sorted_file2_path)

if result:
    print(f"Result:", result)
else:
    print(f"Result:", result)
    sys.exit(1)