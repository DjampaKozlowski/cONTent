import os

def lst_files_in_dir(dpath, ext=None):
    """
    List files in a directory and return a list of file paths.
    Optional : a file extension can be specified. If so, only files with such
    extension will be outputed. NB : Extension is case sensitive.
    Parameters :
    ------------
    dpath (str) -- directory path
    Returns :
    ---------
    (list) -- list of files paths.
    """
    # lst_fpath = []
    if ext:
        lst_fpath = [
            os.path.abspath(f.path)
            for f in os.scandir(dpath)
            if f.is_file() and f.name.endswith(ext)
        ]

    else:
        lst_fpath = [os.path.abspath(f.path) for f in os.scandir(dpath) if f.is_file()]

    return lst_fpath



def lst_content_files(input_path):
    """
    List '.content' files.

    If the path point to a directory, will list all the .content files in it.
    Elif the path point to a file, only return a 1 element list.
    Else, return an empty list

    Parameters :
    ------------
    input_path (str) -- a file/directory path

    Returns :
    ---------
    (list) -- a list of file paths. If no '.content' file found, return an
    empty list
    """
    return lst_files(input_path, ".content")

def lst_files(input_path, ext):
    """
    List files with extentions.

    If the path point to a directory, will list all the .content files in it.
    Elif the path point to a file, only return a 1 element list.
    Else, return an empty list

    Parameters :
    ------------
    input_path (str) -- a file/directory path
    ext (str) -- an extention

    Returns :
    ---------
    (list) -- a list of file paths. If no '.content' file found, return an
    empty list
    """
    lst_paths = []
    if os.path.isdir(input_path):
        lst_paths = lst_files_in_dir(input_path, ext)
    elif os.path.isfile(input_path) and input_path.endswith(ext):
        lst_paths = [os.path.abspath(input_path)]

    return lst_paths