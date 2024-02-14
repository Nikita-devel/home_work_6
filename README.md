# File Sorter

## Project Description

This Python project is designed to organize files within a specified directory based on their file extensions, creating corresponding categories for efficient file management. Each file undergoes transliteration from Cyrillic to Latin characters, ensuring standardized naming conventions, and is then placed in its designated category. The project also identifies archive files, unpacks them, and handles renaming conflicts. Additionally, it provides insights into the directory structure and detected file extensions. The implementation includes functions for transliteration, category determination, and file movement/renaming.

## Key Features

- Efficient file categorization based on predefined extension categories.
- Transliteration of file names from Cyrillic to Latin characters for standardized naming.
- Recognition and unpacking of archive files, including conflict resolution for renamed files.
- Output of directory structure and detected file extensions for informative insights.

## Usage

1. Ensure Python is installed on your system.
2. Run the script with the desired directory path as a command-line argument to initiate the file sorting process.

   ```bash
   python sorter.py /path/to/directory
   
Note: Make sure to provide a valid directory path as the command-line argument.
