import os
import sys
import content.utils as utls 



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
    lst_paths = []
    if os.path.isdir(input_path):
        lst_paths = utls.lst_files_in_dir(input_path, 
                                            '.content')
    elif os.path.isfile(input_path) and input_path.endswith('.content'):
        lst_paths = [os.path.abspath(input_path)]
        
    return lst_paths