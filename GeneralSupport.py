def getFileNameRoot(file_name):
    if "." in file_name:
        file_name_root = file_name.split(".")[0]
    else:
        file_name_root = file_name
    return file_name_root

def bohrToAngstrom(n):
    return float(n) * 0.5291772086
