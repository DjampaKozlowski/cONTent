import sys
import os

import pandas as pd
import numpy as np

import content.common as cmn
import content.graphs as grph




def sub_sample_reads(df, frac):
    """
    Sample a fraction of the reads contained in the input dataframe. 
    
    NB : the sampling is relative to each library, i.e the absolute number of
    sampled reads vary depending on the size of the library. The proportion of
    reads from each libraries should remain unchanged in the final dataframe
    
    Parameters :
    ------------
    df (pandas dataframe)   --  df with the followin columns : 'library', 'read_avg_quality', and 'read_length'
    frac (float)            --  fraction of reads to sample
    
    Returns :
    (pandas dataframe)      --  subsample of the input dataframe
    """
    return df.groupby(by='library').sample(frac=frac).reset_index(drop=True)
    
    
def main(args):
    ### List the files pointed by  args.input
    #
    lst_fpath = cmn.lst_content_files(args.input)
    if len(lst_fpath) == 0:
        print("No .content file found at the given adress. Program will end")
        sys.exit()
    
    ### Create the output directory tree as well as a sub-dir named 'individual 
    #   where per-lib results will be stored
    #   NB : existing files/directories will be overwritten.
    #
    ind_outdir_path = os.path.join(args.outdir, 'individual')
    os.makedirs(ind_outdir_path, 
                mode=0o755, 
                exist_ok=True)
    
    ### Iterate through every input '.content' file(s) and create a global 
    #   dataframe.
    lst_df = []
    for fpath in lst_fpath:
        ## Read the .content file
        df = pd.read_csv(fpath, sep='\t')
        ## Add the origin information
        lib_name = os.path.splitext(os.path.basename(fpath))[0]
        df['library'] = lib_name
        ## Sub-sample the file
        df = sub_sample_reads(df, args.fraction)
        ## Add the df to the list for further concatenation
        lst_df.append(df)
        ## Create a plot for each lib
        ind_distrib_plot = grph.DistributionPLot(
            os.path.join(ind_outdir_path, f'ReadsDistribution_{lib_name}.pdf'),
            df,
            title=lib_name)
        ind_distrib_plot.create_graph()
        ind_distrib_plot.save_graph()
    
    ### Create a global dataframe from all the libraries
    #  
    df_glob = pd.concat(lst_df)
    
    ### Generate a global plot over all the input libraries
    #
    glob_distrib_plot = grph.DistributionPLot(
        os.path.join(args.outdir, f'ReadsDistribution_{args.prefix}.pdf'),
        df_glob,
        title=args.prefix
        )
    glob_distrib_plot.create_graph()
    glob_distrib_plot.save_graph()
   
    # python bin/cONTent.py distrib -input data -o tmp -prefix maksjfklsfdj -f 0.0001
