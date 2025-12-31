# A python program to print the content of a directpry using the os module

import os

# Specify the directory path
directory_path = "/xampp"  # Current directory, or use "/path/to/directory"

# Check if the directory exists
if os.path.exists(directory_path) and os.path.isdir(directory_path):
    print(f"Contents of '{directory_path}':\n")
    
    # Get all files and folders in the directory
    contents = os.listdir(directory_path)
    
    # Print each item
    for item in contents:
        full_path = os.path.join(directory_path, item)
        
        # Check if it's a file or directory
        if os.path.isfile(full_path):
            print(f"📄 {item}")
        elif os.path.isdir(full_path):
            print(f"📁 {item}")
else:
    print(f"Directory '{directory_path}' does not exist.")