import os
import shutil
from pathlib import Path
import time

def get_unique_filename(directory, filename):
    """
    Generate a unique filename by appending (n) where n is the smallest integer that results in a unique filename.
    """
    base, extension = os.path.splitext(filename)
    counter = 1
    new_filename = f"{base}({counter}){extension}"
    while (directory / new_filename).exists():
        counter += 1
        new_filename = f"{base}({counter}){extension}"
    return new_filename

def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█', start_time=None):
    """
    Call in a loop to create terminal progress bar
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)

    # Calculate time taken and estimated time remaining
    if start_time:
        elapsed_time = time.time() - start_time
        avg_time_per_iteration = elapsed_time / iteration if iteration > 0 else 0
        estimated_total_time = avg_time_per_iteration * total
        estimated_time_remaining = estimated_total_time - elapsed_time

        time_suffix = f" | Elapsed: {time.strftime('%H:%M:%S', time.gmtime(elapsed_time))} | Remaining: {time.strftime('%H:%M:%S', time.gmtime(estimated_time_remaining))}"
    else:
        time_suffix = ""

    print(f'\r{prefix} |{bar}| {percent}% {suffix}{time_suffix}', end='\r')
    if iteration == total: 
        print()

def copy_or_move_with_renaming(src_dir, dest_dir, operation):
    """
    Copy or move a folder with contents to a network drive while retaining any duplicates renamed with numbers.
    """
    src_dir = Path(src_dir)
    dest_dir = Path(dest_dir)

    if not src_dir.exists():
        print(f"Source directory {src_dir} does not exist.")
        return

    if not dest_dir.exists():
        dest_dir.mkdir(parents=True)

    files = list(src_dir.rglob('*'))
    total_files = len(files)
    start_time = time.time()
    for i, item in enumerate(files):
        print_progress_bar(i, total_files, prefix=f'{operation.capitalize()}ing files:', suffix='Complete', length=50, start_time=start_time)
        if item.is_file():
            relative_path = item.relative_to(src_dir)
            destination = dest_dir / relative_path

            if destination.exists():
                new_filename = get_unique_filename(destination.parent, destination.name)
                destination = destination.parent / new_filename

            destination.parent.mkdir(parents=True, exist_ok=True)
            if operation == 'copy':
                shutil.copy2(item, destination)
            elif operation == 'move':
                shutil.move(str(item), destination)
    print_progress_bar(total_files, total_files, prefix=f'{operation.capitalize()}ing files:', suffix='Complete', length=50, start_time=start_time)

if __name__ == "__main__":
    print("Select the operation:")
    print("1. Copy")
    print("2. Move")
    operation_choice = input("Enter 1 or 2: ").strip()

    if operation_choice == '1':
        operation = 'copy'
    elif operation_choice == '2':
        operation = 'move'
    else:
        print("Invalid choice. Please run the script again and enter 1 or 2.")
        exit()

    src_dir = input("Enter the source directory path: ")
    dest_dir = input("Enter the destination directory path: ")

    copy_or_move_with_renaming(src_dir, dest_dir, operation)
