import sys 
import os 
import argparse
import multiprocessing
import argparse
import pandas as pd

import nanoget.extraction_functions as nef



def arguments_parser():
    """
    Description :
    -------------
    Parse script arguments to get the following information:
            - input file path
            - output file path
            - number of CPUs
    Returns :
    ---------
     *  -- object, parser object
    """
    parser = argparse.ArgumentParser(description="Parse reads a read library \
        (fastq/fastq.gz) and for each read \
        extract the read's name, length, and average quality. \
        Save the results as a tab separated values file.")
    parser.add_argument("-i", 
                        "--inputfilepath", 
                        help="input fastq/fastq.gz file path [mendatory]", 
                        type=str,
                        required=True)
    parser.add_argument("-o", 
                        "--outputfilepath", 
                        help="output file path  [mendatory]", 
                        type=str,
                        required=True)
    parser.add_argument("-t", 
                        "--threads", 
                        help="Number of parallel jobs. If a negative number is \
                            provided or if the provided number exceed the \
                            number of available CPUs, the number of threads is \
                            set to the maximum number of available CPUs \
                            [default=1]", 
                        type=int,
                        default=1)
    return parser.parse_args()


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





def extract_infos_from_fastq(fpath, threads):
    """
    For each reads contained in a .fastq / .fastq.gz file, extract :
        - the read name
        - the read length
        - the average read quality
    This function uses stream_fastq_full function 
    from nanoget.extraction_functions (https://github.com/wdecoster/nanoget)
    See nanoget.utils.ave_qual function for more information about the quality
    score computation. 
    
    Parameters :
    ------------
    fpath (str) -- input fastq/fastq.gz file path
    threads (int) -- the number of parallels threads
    """
    return pd.DataFrame\
        .from_records(nef.stream_fastq_full(fpath, threads),
                                     columns=['read_name', 
                                              'read_length', 
                                              'read_avg_quality', 
                                              'other'])\
                                                  .drop(columns='other')
                                                  

if __name__ == "__main__":

    ### Get the script arguments' values
    #
    args = arguments_parser()
    input_fpath = os.path.abspath(args.inputfilepath)
    output_fpath = os.path.abspath(args.outputfilepath)
    
    ### Check the number of available CPUs
    #
    nb_cpu = manage_cpus(args.threads)
    
    ### Parse fastq file
    #
    df = extract_infos_from_fastq(input_fpath, 
                                  nb_cpu)
    
    ### Save the results in a tab separated values file.
    #
    df.to_csv(output_fpath, 
              sep='\t',
              header=True,
              index=False)
    
    
    
                                   