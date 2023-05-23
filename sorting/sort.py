import os
import shutil
import sys

def normalize(filename):
    translit_table = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g', 'д': 'd', 'е': 'e', 'є': 'ie',
        'ж': 'zh', 'з': 'z', 'и': 'y', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k', 'л': 'l',
        'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ю': 'iu',
        'я': 'ia',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'H', 'Ґ': 'G', 'Д': 'D', 'Е': 'E', 'Є': 'Ye',
        'Ж': 'Zh', 'З': 'Z', 'И': 'Y', 'І': 'I', 'Ї': 'Yi', 'Й': 'Y', 'К': 'K', 'Л': 'L',
        'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
        'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch', 'Ю': 'Yu',
        'Я': 'Ya'
    }

    result = ''
    for char in filename:
        if char.isalnum():
            result += char
        elif char in translit_table:
            result += translit_table[char]
        else:
            result += '_'
    return result

def process_folder(folder_path):
    known_extensions = {
        'images': ('JPEG', 'PNG', 'JPG', 'SVG'),
        'video': ('AVI', 'MP4', 'MOV', 'MKV'),
        'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
        'audio': ('MP3', 'OGG', 'WAV', 'AMR'),
        'archives': ('ZIP', 'GZ', 'TAR')
    }
    unknown_extensions = set()

    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_extension = filename.split('.')[-1].upper()

            if file_extension in known_extensions['images']:
                destination = 'images'
            elif file_extension in known_extensions['video']:
                destination = 'video'
            elif file_extension in known_extensions['documents']:
                destination = 'documents'
            elif file_extension in known_extensions['audio']:
                destination = 'audio'
            elif file_extension in known_extensions['archives']:
                destination = 'archives'
                unpacked_folder = os.path.splitext(file_path)[0]
                shutil.unpack_archive(file_path, unpacked_folder)
                process_folder(unpacked_folder)
            else:
                destination = 'unknown'
                unknown_extensions.add(file_extension)

            if destination != 'unknown':
                destination_folder = os.path.join(folder_path, destination)
                os.makedirs(destination_folder, exist_ok=True)
                new_filename = normalize(filename)
                new_file_path = os.path.join(destination_folder, new_filename)
                shutil.move(file_path, new_file_path)

    return known_extensions, unknown_extensions

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide the folder path as an argument.")
    else:
        folder_path = sys.argv[1]
        known_extensions, unknown_extensions = process_folder(folder_path)

        print("Known extensions:")
        for category, extensions in known_extensions.items():
            print(f"{category}: {', '.join(extensions)}")

        print("\nUnknown extensions:")
        print(', '.join(unknown_extensions))
# test