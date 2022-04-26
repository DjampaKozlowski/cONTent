
import pandas as pd
import nanoget.extraction_functions as nef


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