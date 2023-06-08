import os
import sys
import shutil

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


def main():
    sorted_path = sys.argv[1]

    files = os.listdir(sorted_path)

    ext_set = set()
    unknown_ext_set = set()

    for file in files:
        if os.path.isfile(os.path.join(sorted_path, file)):
            ext = file.split('.')[-1]
            if ext in str(CATEGORIES.values()):
                ext_set.add(ext)
            else:
                unknown_ext_set.add(ext)

            normalized_name = transliterate(file)
            os.rename(os.path.join(sorted_path, file), os.path.join(sorted_path, normalized_name))

    for category in CATEGORIES:
        if category not in os.listdir(sorted_path):
            os.mkdir(os.path.join(sorted_path, category))

    for file in os.listdir(sorted_path):
        if os.path.isfile(os.path.join(sorted_path, file)):
            ext = file.split('.')[-1]
            category = get_category(ext)
            target_folder = os.path.join(sorted_path, category)
            
            if category == 'ARCHIVE':
                shutil.unpack_archive(os.path.join(sorted_path, file), target_folder)
                os.remove(os.path.join(sorted_path, file))
            else:
                shutil.move(os.path.join(sorted_path, file), target_folder)

    # Remove empty directories
    for root_folder, dirs, _ in os.walk(sorted_path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root_folder, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)

    for folder in os.listdir(sorted_path):
        folder_path = os.path.join(sorted_path, folder)
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


if __name__ == "__main__":
    main()
