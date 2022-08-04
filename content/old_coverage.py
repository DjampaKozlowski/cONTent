import numpy as np
import pandas as pd

def compute_cov_fct_of_qual_and_len(df, genome_size, n=10, m=10):
    """
    Compute genome coverage in function of different length and quality 
    thresholds. Split the length and quality space evenly according to n 
    (number of bins for reads length) and m (number of bins for reads quality) 
    parameters. 
    
    Parameters : 
    -----------
    df (pandas dataframe) -- a dataframe with the following 
    columns : 'read_length' and 'read_avg_quality'
    genome_size (int) -- the genome size (bp)
    n (int) -- number of reads length bins. Data space will be evenly cut 
    (log scale)
    m (int) -- number of reads quality bins.Data space will be evenly cut.
    
    Returns : 
    ---------
    (pandas dataframe) -- a pandas dataframe of 4 columns and n*m rows. The 
    columns are 'min_length', 'min_quality', 'total_length', 'coverage'.
    
    """
    scl_l = np.flip(
        np.geomspace(start=df.read_length.min(),
                    stop=df.read_length.max(),
                    num=n
                    )
        )
    scl_q= np.flip(
        np.linspace(start=df.read_avg_quality.min(),
                    stop=df.read_avg_quality.max(),
                    num=m
                    )
        )

    lst_dct = []
    for q in scl_q:
        for l in scl_l:
            L = df[(df.read_length >= l) & (df.read_avg_quality >= q)].read_length.sum()
            C = L/genome_size
            lst_dct.append(
                {'min_length':l,
                 'min_quality':q,
                 'total_length':L,
                 'coverage':C}
                )
    return pd.DataFrame(lst_dct)