import os

def count_files_and_size(folder):
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    total_files = len(files)
    total_size = sum(os.path.getsize(os.path.join(folder, f)) for f in files)
    return total_files, total_size