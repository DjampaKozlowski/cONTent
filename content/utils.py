import os
import multiprocessing

def manage_cpus(nb_wanted_cpus):
    """
    Check the number of available CPUs, compare it with the number of CPUs
    wanted and return the number of CPUs to use.
    If the number of CPU wanted is > to the number of available CPU or <= 0, the 
    max number of available CPU is returned. Else, the required number of CPU 
    is returned.
    
    Parameters:
    -----------
        nb_wanted_cpus (int)    :   the number of CPU wanted. If == 0, will return
                                    all the CPU available.
                                    (default : 0)
    Returns:
    --------
        (int)                   :   the number of CPU to use.
    """

    nb_available_cpus = multiprocessing.cpu_count()
    if (nb_wanted_cpus <= 0) or (nb_wanted_cpus > nb_available_cpus):
        nb_cpu_to_use = nb_available_cpus
    else:
        nb_cpu_to_use = nb_wanted_cpus
    return nb_cpu_to_use


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
    lst_fpath = []
    if ext:
        for f in os.scandir(dpath):
            if f.is_file():
                if f.name.endswith(ext):
                    lst_fpath.append(f.path)        
    else:
        for f in os.scandir(dpath):
            if f.is_file():
                lst_fpath.append(f.path)
    return lst_fpath


