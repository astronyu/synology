[sort_moments.py]

Generates a unique filename by appending (n) to the base name of the file if a file with the same name already exists in the destination directory. 
Checks if a file with the new name exists and increments the counter until a unique name is found.

Processes a single parent folder containing yyyy-mm-dd subfolders.
Creates year/month directories in the destination directory.
Moves all files from the day folder to the corresponding month folder.

Processes multiple parent folders each containing yyyy-mm-dd subfolders.
Creates year/month directories in the destination directory.
Moves all files from the day folder to the corresponding month folder.

Prompts the user to choose whether to process a single parent folder or multiple parent folders.
Prompts the user to enter the source and destination directory paths.
Calls the appropriate function based on the user's choice.

=======================================================================================================================

[copy_or_move_with_renaming.py]

How to Use:

Save the script as copy_or_move_with_renaming.py.
Use a Python interpreter to run the script:

    python copy_or_move_with_renaming.py

Enter 1 to copy files or 2 to move files.
Provide the source and destination directory paths when asked.
This script lets you choose between copying or moving files, shows progress with an estimated time remaining, and renames duplicates automatically.
