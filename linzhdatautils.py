import linzhutils as lu
from tqdm import tqdm
import os
import shutil
import random


def confirm_directory_empty(dst):
    if not lu.is_folder_empty(dst) or os.path.exists(dst):
        confirm = input(
            f"WARNING: {dst} is not empty or exists. Do you want to proceed? (y/n) "
        )
        if confirm.lower() != 'y':
            print("Aborting operation.")
            return False
    return True


def split_data(src, dst, ratio, seed=42):
    """
    Split data from a source directory into a destination directory based on a given ratio.
    """
    if not confirm_directory_empty(dst):
        return

    lu.ensure_directory_exists(dst)
    file_list = lu.get_file_list(src)
    random.seed(seed)
    move_list = random.sample(file_list, int(len(file_list) * ratio))
    for i in tqdm(move_list):
        shutil.move(os.path.join(src, i), os.path.join(dst, i))


def split_multi_data(src_list, dst_list, ratio=0.7, seed=42):
    """
    Split data in multiple folders, e.g. images and masks, with a given ratio.
    """
    assert len(src_list) == len(dst_list)

    # Check if all dst directories are empty or don't exist; otherwise, ask for user confirmation
    if not all(confirm_directory_empty(dst) for dst in dst_list):
        return

    # Check if all src directories have the same number of files
    file_counts = [len(lu.get_file_list(src)) for src in src_list]
    if len(set(file_counts)) != 1:
        print(
            "Error: The source directories do not have the same number of files."
        )
        return

    random.seed(seed)
    file_list = lu.get_file_list(src_list[0])
    move_list = random.sample(file_list, int(len(file_list) * (1 - ratio)))
    for j in range(len(dst_list)):
        lu.ensure_directory_exists(dst_list[j])
        for i in range(len(move_list)):
            file_name = move_list[i]
            shutil.move(os.path.join(src_list[j], file_name),
                        os.path.join(dst_list[j], file_name))
