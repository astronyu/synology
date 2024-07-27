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

def sort_photos(src_dir, dest_dir):
    """
    Sort photos by moving files from yyyy-mm-dd subfolders into yyyy/mm subfolders.
    """
    src_dir = Path(src_dir)
    dest_dir = Path(dest_dir)

    if not src_dir.exists():
        print(f"Source directory {src_dir} does not exist.")
        return

    if not dest_dir.exists():
        dest_dir.mkdir(parents=True)

    # Collect all files from yyyy-mm-dd subfolders
    files = list(src_dir.rglob('*'))
    total_files = len(files)
    start_time = time.time()

    for i, item in enumerate(files):
        if item.is_file():
            # Extract date parts from the file's relative path
            relative_path = item.relative_to(src_dir)
            year, month, _ = relative_path.parts[:3]
            destination = dest_dir / year / month / relative_path.name

            # Create destination directories if they don't exist
            destination.parent.mkdir(parents=True, exist_ok=True)

            # Move the file
            if destination.exists():
                new_filename = get_unique_filename(destination.parent, destination.name)
                destination = destination.parent / new_filename
            shutil.move(str(item), destination)

        # Update progress bar
        print_progress_bar(i + 1, total_files, prefix='Sorting files:', suffix='Complete', length=50, start_time=start_time)

    print_progress_bar(total_files, total_files, prefix='Sorting files:', suffix='Complete', length=50, start_time=start_time)

if __name__ == "__main__":
    src_dir = input("Enter the source directory path: ")
    dest_dir = input("Enter the destination directory path: ")

    sort_photos(src_dir, dest_dir)
