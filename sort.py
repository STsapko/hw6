import sys
from pathlib import Path
import shutil
import os
from normalize import normalize

CATEGORIES_FILENAME = 'categories.txt'

def open_categories(CATEGORIES_FILENAME):
    with open(CATEGORIES_FILENAME) as fd:
        categories_list = fd.read().split('\n')
    return dict((line.split(': ')[0], line.split(': ')[1].replace(' ', '' ).split(','))  for line in categories_list)

CATEGORIES = open_categories(CATEGORIES_FILENAME)

def move_file(file: Path, root_dir: Path, category: str):
    normalized_file = str(normalize(file.stem)) + file.suffix
    if category == 'unknown':
        return file.replace(root_dir.joinpath(normalized_file))
    target_dir = root_dir.joinpath(category)
    if not target_dir.exists():
        target_dir.mkdir()
    return file.replace(target_dir.joinpath(normalized_file))

def get_categories(file: Path):
    extension = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if extension in exts:
            return cat
    return 'unknown'

def unpack_remove_archives(root_dir: Path):
    archive_folder_name = 'archives'
    archives_folder_path = root_dir.joinpath(archive_folder_name)
    if archives_folder_path.exists():
        for archive_path in archives_folder_path.glob('*'):
            extract_dir = archive_path.parent.joinpath(archive_path.stem)
            shutil.unpack_archive(archive_path, extract_dir)
            os.remove(archive_path)
        return 'Archives have been unpacked'
    else:
        return 'No folder with archives'

def sort_dir(root_dir: Path, current_dir: Path):
    for item in [f for f in current_dir.glob('*') if f.name not in CATEGORIES.keys()]:
        if not item.is_dir():
            category = get_categories(item)
            new_path = move_file(item, root_dir, category)
            print(new_path)
        else:
            sort_dir(root_dir, item)
            item.rmdir()
    
def return_results_info(root_path):
    known_extensions = []
    for dir in [item for item in root_path.glob('*') if item.is_dir()]:
        print(f"category: {dir.stem}")
        for file in dir.glob('*.*'):
            print(file.name)
            known_extensions.append(file.suffix)
        print('\n')

    unknown_extensions = set([file.suffix for file in root_path.glob('*.*')])   
    print(f"known_extensions: \n{', '.join(set(known_extensions))}", '\n')
    print(f"unknown_extensions: \n{', '.join(unknown_extensions)}")

def main():
    try:
        path = Path(sys.argv[1])
        # return 'All ok'
    except IndexError:
        return f'No path to folder. Take as parameter'
    if not path.exists():
        return "Sorry, correct folder not exists"
    sort_dir(path, path)
    return_results_info(path)
    unpack_remove_archives(path)
    return 'All ok'

if __name__ == "__main__":
    main()