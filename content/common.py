import os
import time
from multiprocessing import cpu_count
from numpy import round
import pandas as pd


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
    lst_fpath_tmp = lst_files(input_path, ".content")
    lst_fpath = []

    col_name = ["read_name", "read_length","read_avg_quality"]

    for i in lst_fpath_tmp:
        df = pd.read_csv(i, sep = "\t", nrows = 10)

        if col_name != df.columns.to_list():
            print(f"The name of the column of {i} is wrong, it must be : {', '.join(col_name)}. In this order and number")
            continue

        if not all([
            pd.api.types.is_integer_dtype(df.read_length),
            pd.api.types.is_float_dtype(df.read_avg_quality)
        ]):
            print(f"The type of the columns {i} of the read_length and read_avg_quality is wrong, it must be an int and float")
            continue
        
        lst_fpath.append(i)


    return lst_fpath

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


def number_thread(threads: int) -> int:
    return cpu_count() if threads == 0 else min(threads, cpu_count())


# Decoration : timer
def time_d(fct):
    def decorated_func(*args, **kwargs):

        start = time.time()

        fct(*args, **kwargs)

        end = time.time()

        print(f"duration : {round(end-start, 3)} s")
    
    return decorated_func