import os
import shutil
from pathlib import Path

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

def sort_photos_single(src_dir, dest_dir):
    """
    Process a single parent folder containing yyyy-mm-dd subfolders.
    """
    src_dir = Path(src_dir)
    dest_dir = Path(dest_dir)

    if not src_dir.exists():
        print(f"Source directory {src_dir} does not exist.")
        return

    for folder in src_dir.iterdir():
        if folder.is_dir():
            try:
                year, month, day = folder.name.split('-')
                new_folder_path = dest_dir / year / month
                new_folder_path.mkdir(parents=True, exist_ok=True)
                
                for file in folder.iterdir():
                    if file.is_file():
                        destination = new_folder_path / file.name
                        if destination.exists():
                            new_filename = get_unique_filename(new_folder_path, file.name)
                            destination = new_folder_path / new_filename
                        shutil.move(str(file), destination)
                        
                # Remove the original folder if it's empty
                folder.rmdir()

            except ValueError:
                print(f"Skipping folder {folder.name}: does not match yyyy-mm-dd format.")

def sort_photos_multiple(src_dir, dest_dir):
    """
    Process multiple parent folders each containing yyyy-mm-dd subfolders.
    """
    src_dir = Path(src_dir)
    dest_dir = Path(dest_dir)

    if not src_dir.exists():
        print(f"Source directory {src_dir} does not exist.")
        return

    for parent_folder in src_dir.iterdir():
        if parent_folder.is_dir():
            for folder in parent_folder.iterdir():
                if folder.is_dir():
                    try:
                        year, month, day = folder.name.split('-')
                        new_folder_path = dest_dir / year / month
                        new_folder_path.mkdir(parents=True, exist_ok=True)
                        
                        for file in folder.iterdir():
                            if file.is_file():
                                destination = new_folder_path / file.name
                                if destination.exists():
                                    new_filename = get_unique_filename(new_folder_path, file.name)
                                    destination = new_folder_path / new_filename
                                shutil.move(str(file), destination)
                                
                        # Remove the original folder if it's empty
                        folder.rmdir()

                    except ValueError:
                        print(f"Skipping folder {folder.name}: does not match yyyy-mm-dd format.")

if __name__ == "__main__":
    choice = input("Do you want to process a single parent folder (1) or multiple parent folders (2)? Enter 1 or 2: ")
    src_dir = input("Enter the source directory path: ")
    dest_dir = input("Enter the destination directory path: ")

    if choice == '1':
        sort_photos_single(src_dir, dest_dir)
    elif choice == '2':
        sort_photos_multiple(src_dir, dest_dir)
    else:
        print("Invalid choice. Please run the script again and enter 1 or 2.")
