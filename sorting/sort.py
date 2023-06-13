import os
import sys
import shutil
import uuid

CATEGORIES = {
    'IMAGE': ['jpeg', 'png', 'jpg', 'svg'],
    'VIDEO': ['avt', 'mp4', 'mov', 'mkv'],
    'DOCS': ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx', 'rtf'],
    'MUSIC': ['mp3', 'ogg', 'wav', 'amr'],
    'ARCHIVE': ['zip', 'gz', 'tar', '7z'],
    'OTHER': []
}
IGNORE = ['.DS_Store']

TRANSLATE_DICT = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
    'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
    'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
    'ю': 'u', 'я': 'ya', 'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'YO',
    'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
    'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H',
    'Ц': 'C', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SCH', 'Ъ': '', 'Ы': 'y', 'Ь': '', 'Э': 'E',
    'Ю': 'U', 'Я': 'YA', 'ґ': '', 'ї': '', 'є': '', 'Ґ': 'g', 'Ї': 'i',
    'Є': 'e', '1': '1', '2': '2', '3': '3'
}


def transliterate(word):
    return ''.join(TRANSLATE_DICT.get(c, c) for c in word)


def get_category(ext):
    for category, extensions in CATEGORIES.items():
        if ext in extensions and ext not in IGNORE:
            return category
    return 'OTHER'


def sort_files_in_directory(directory):
    ext_set = set()
    unknown_ext_set = set()

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                ext = file.split('.')[-1]
                if ext in [item for sublist in CATEGORIES.values() for item in sublist]:
                    ext_set.add(ext)
                else:
                    unknown_ext_set.add(ext)

                normalized_name = transliterate(file)
                os.rename(file_path, os.path.join(root, normalized_name))

    for category in CATEGORIES:
        category_folder = os.path.join(directory, category)
        if category not in os.listdir(directory):
            os.mkdir(category_folder)

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                ext = file.split('.')[-1]
                category = get_category(ext)
                target_folder = os.path.join(directory, category)

                if category == 'ARCHIVE':
                    shutil.unpack_archive(file_path, target_folder)
                    os.remove(file_path)
                else:
                    if os.path.exists(os.path.join(target_folder, file)):
                        base_name = os.path.splitext(file)[0]
                        unique_name = base_name + '_' + str(uuid.uuid4())[:8] + os.path.splitext(file)[1]
                        shutil.move(file_path, os.path.join(target_folder, unique_name))
                    else:
                        shutil.move(file_path, target_folder)

    # Remove empty directories
    for root_folder, dirs, _ in os.walk(directory, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root_folder, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)

    for folder in os.listdir(directory):
        folder_path = os.path.join(directory, folder)
        print('{:>50} - {:<50} '.format('Folder', folder))
        print('{:^100}'.format('-' * 99))
        for file in os.listdir(folder_path):
            print('{:^5} {:<95} '.format('', file))
        print('\n')
        print('{:^100}'.format('-' * 99))

    print('{:^100}'.format('*' * 100))
    print(f"Founded file's with known extension: {ext_set}")
    print(f"Founded file's with unknown extension: {unknown_ext_set}")
    print('{:^100}'.format('*' * 100))


def main():
    if len(sys.argv) < 2:
        print("Please provide a directory path as an argument.")
        return

    sorted_path = sys.argv[1]

    if not os.path.exists(sorted_path) or not os.path.isdir(sorted_path):
        print("Invalid directory path.")
        return

    sort_files_in_directory(sorted_path)


if __name__ == "__main__":
    main()
