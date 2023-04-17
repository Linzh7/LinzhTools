import os
from pathlib import Path
import shutil
from tqdm import tqdm


def is_folder_empty(folder_path):
    """Check if a folder is empty."""
    return len(os.listdir(folder_path)) == 0


def ensure_directory_exists(path):
    """Create a directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)


def move_pair_files(src1, src2, dst1, dst2=None):
    """
    Move files from src1 and src2 to dst1 and dst2 respectively, if they have the same file name (excluding extension).
    """
    if dst2 is None:
        dst2 = dst1
    file_list1 = get_file_list(src1)
    file_list2 = get_file_list(src2)
    file_list1.sort()
    file_list2.sort()
    i = 0
    j = 0
    while i < len(file_list1) or j < len(file_list2):
        name1 = file_list1[i].split('.')[0]
        name2 = file_list2[j].split('.')[0]
        if name1 == name2:
            shutil.move(os.path.join(src1, file_list1[i]),
                        os.path.join(dst1, file_list1[i]))
            shutil.move(os.path.join(src2, file_list2[j]),
                        os.path.join(dst2, file_list2[j]))
            i += 1
            j += 1
        elif name1 < name2:
            i += 1
        else:
            j += 1


def remove_files(path, pattern):
    """Remove files that match a given pattern."""
    file_list = Path(path).rglob(pattern)
    for i in tqdm(file_list):
        print(f'[UtilsToolkit] Removing {i}...')
        os.remove(i)


def move_files_to(src, dst, file_name_pattern):
    """
    Move files from src to dst directory that match the given file name pattern.
    """
    if not is_folder_empty(dst):
        confirm = input(
            f"WARNING: {dst} is not empty. Do you want to proceed? (y/n) ")
        if confirm.lower() != 'y':
            print("Aborting move operation")
            return
    ensure_directory_exists(dst)
    file_list = get_files_from_pattern(src, file_name_pattern)
    file_count = len(list(file_list))
    if file_count == 0:
        print(
            f"No files found in {src} that match pattern {file_name_pattern}")
        return
    print(
        f"Found {file_count} files in {src} that match pattern {file_name_pattern}"
    )
    for i in tqdm(list(file_list)):
        file_name = str(i).split('/')[-1]
        shutil.move(i, os.path.join(dst, file_name))


def get_files_from_pattern(path, pattern):
    """Get a list of files that match a given pattern."""
    return Path(path).rglob(pattern)


def print_not_instance(ls, type):
    """Print elements of a list that are not instances of a given type."""
    for i in ls:
        if not isinstance(i, type):
            try:
                type(i)
            except Exception as e:
                print(f"Error: {e}")


def rename_files(folder_path, add_name):
    """Rename all files in a folder by adding a prefix."""
    file_list = get_file_list(folder_path)
    for file_name in tqdm(file_list):
        os.rename(os.path.join(folder_path, file_name),
                  os.path.join(folder_path, f"{add_name}{file_name}"))


def get_file_list(path):
    """Get a list of files in a directory, excluding hidden files."""
    return [
        f.name for f in Path(path).iterdir()
        if f.is_file() and not f.name.startswith('.')
    ]


def get_all_file_list(path):
    """Get a list of all files, including those in subdirectories."""
    return [str(f) for f in Path(path).rglob('*') if f.is_file()]


def get_folder_list(path):
    """Get a list of folders in a directory."""
    return [f.name for f in Path(path).iterdir() if f.is_dir()]


# def get_file_content(file_path):
#     """Read and return the content of a file."""
#     with open(file_path, 'rb') as fp:
#         return fp.read()
