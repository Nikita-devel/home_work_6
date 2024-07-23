import os
import shutil
import zipfile
import tarfile
import re
import uuid
from pathlib import Path

# Транслітерація кирилиці на латиницю
TRANS = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d",
    "е": "e", "є": "ie", "ж": "zh", "з": "z", "и": "y",
    "і": "i", "ї": "i", "й": "i", "к": "k", "л": "l",
    "м": "m", "н": "n", "о": "o", "п": "p", "р": "r",
    "с": "s", "т": "t", "у": "u", "ф": "f", "х": "kh",
    "ц": "ts", "ч": "ch", "ш": "sh", "щ": "shch", "ю": "iu",
    "я": "ia"
}

def normalize(name: str) -> str:
    transliterated = ''.join(TRANS.get(ch.lower(), ch) for ch in name)
    normalized = re.sub(r'[^a-zA-Z0-9]', '_', transliterated)
    return normalized

# Категорії файлів
FILE_TYPES = {
    'text': ['.txt', '.doc', '.docx', '.pdf', '.odt', '.rtf', '.md', '.tex', '.wps'],
    'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.tiff', '.psd', '.ai', '.ico'],
    'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', '.aiff'],
    'video': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.vob'],
    'archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.iso'],
    'databases': ['.sql', '.mdb', '.accdb', '.sqlite', '.db', '.dbf', '.myd', '.frm'],
    'software': ['.exe', '.msi', '.apk', '.dmg', '.iso', '.bin', '.jar', '.deb', '.rpm'],
    'scripts': ['.py', '.js', '.html', '.css', '.php', '.java', '.cpp', '.cs', '.rb', '.sh', '.pl'],
    'system': ['.dll', '.sys', '.ini', '.log', '.bat', '.cfg', '.reg', '.efi']
}

def categorize_file(file_name: str) -> str:
    ext = os.path.splitext(file_name)[1].lower()
    for category, extensions in FILE_TYPES.items():
        if ext in extensions:
            return category
    return 'other'

def handle_archive(file_path: str, target_dir: str):
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == '.zip':
            with zipfile.ZipFile(file_path, 'r') as archive:
                archive.extractall(target_dir)
        elif ext in ['.tar', '.gz', '.bz2', '.xz']:
            with tarfile.open(file_path, 'r:*') as archive:
                archive.extractall(target_dir)
        os.remove(file_path)
    except (zipfile.BadZipFile, tarfile.TarError):
        print(f"Failed to unpack the archive: {file_path}")

def ensure_unique_path(path: str) -> str:
    if not os.path.exists(path):
        return path
    
    base, ext = os.path.splitext(path)
    unique_path = f"{base}_{uuid.uuid4().hex}{ext}"
    return ensure_unique_path(unique_path)

def process_folder(folder_path: str):
    sorted_files = {
        'text': [],
        'images': [],
        'audio': [],
        'video': [],
        'archives': [],
        'databases': [],
        'software': [],
        'scripts': [],
        'system': [],
        'other': []
    }
    known_extensions = set()
    unknown_extensions = set()

    # Створюємо папки для кожної категорії
    for category in sorted_files.keys():
        category_dir = os.path.join(folder_path, category)
        os.makedirs(category_dir, exist_ok=True)

    for root, dirs, files in os.walk(folder_path, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            category = categorize_file(file)
            sorted_files[category].append(file_path)

            ext = os.path.splitext(file)[1].lower()
            if category == 'other':
                unknown_extensions.add(ext)
            else:
                known_extensions.add(ext)

            new_name = normalize(os.path.splitext(file)[0]) + ext
            new_path = os.path.join(folder_path, category, new_name)
            new_path = ensure_unique_path(new_path)
            shutil.move(file_path, new_path)

            if category == 'archives':
                target_dir = os.path.join(folder_path, 'archives', os.path.splitext(file)[0])
                os.makedirs(target_dir, exist_ok=True)
                handle_archive(new_path, target_dir)

    remove_empty_dirs(folder_path)

    print("\nSorting completed. Results:")
    for category, files in sorted_files.items():
        print(f"{category.capitalize()}:")
        for file in files:
            print(f"  - {file}")

    print("\nKnown extensions:")
    for ext in known_extensions:
        print(f"  - {ext}")

    print("\nUnknown extensions:")
    for ext in unknown_extensions:
        print(f"  - {ext}")

def remove_empty_dirs(folder_path: str):
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            try:
                os.rmdir(dir_path)
                print(f"Removed empty directory: {dir_path}")
            except OSError:
                pass

def main():
    while True:
        folder_path = input("Enter the path to the folder to sort (or type 'exit' to quit): ").strip()
        if folder_path.lower() == 'exit':
            print("Exiting the program.")
            break
        
        if not os.path.isdir(folder_path):
            print(f"The path '{folder_path}' is not a valid directory. Please try again.")
            continue

        process_folder(folder_path)

if __name__ == "__main__":
    main()
