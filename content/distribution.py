import sys
import os
import time

from multiprocessing import Pool
from functools import partial

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
    return df.groupby(by="library").sample(frac=frac).reset_index(drop=True)

def basic_stats(df, outdir, prefix):
    df[["read_length", "read_avg_quality"]].describe().to_csv(
        os.path.join(outdir, f"ReadsDistribution_basic_stats_{prefix}.tsv")
        , sep="\t")


def workers(fpath, fraction, ind_outdir_path):
    df = pd.read_csv(fpath, sep="\t")

    ## Check that the file is not empty, else, raise a warning 
    if len(df)>1:
        ## Add the origin information
        lib_name = os.path.splitext(os.path.basename(fpath))[0]
        df["library"] = lib_name

        ## Sub-sample the file
        df = sub_sample_reads(df, fraction)

        ## Create a plot for each lib
        ind_distrib_plot = grph.DistributionPLot(
            os.path.join(ind_outdir_path, f"ReadsDistribution_{lib_name}.pdf"),
            df,
            title=lib_name,
        )
        ind_distrib_plot.create_graph()
        ind_distrib_plot.save_graph()

        ## Save basic stats about reads' length and quality (individual)
        basic_stats(df, ind_outdir_path, lib_name)

        return df
        
    else:
        print(f"{fpath} is an empty file.")
        return None





@cmn.time_d
def main(args):
    """
    Execute the whole analysis.

    TODO : make intermediate functions to make the program more versatile,
    especially to be able to use the functions in a notebook for instance.
    """
    print("Starting cONTent distribution analysis")

    ### List the files pointed by  args.input
    #
    ## TODO : modify the lst_content_files function so it ckeck for columns
    ## rather than just files extensions
    lst_fpath = cmn.lst_content_files(args.input)
    nb_input_file = len(lst_fpath)
    if nb_input_file == 0:
        print("No .content file found at the given adress. Program will end")
        sys.exit()
    elif nb_input_file > 1:
        ### Create the output directory tree as well as a sub-dir named 'individual
        #   where per-lib results will be stored
        #   NB : existing files/directories will be overwriting.
        #
        ind_outdir_path = os.path.join(args.outdir, "individual")
        os.makedirs(ind_outdir_path, mode=0o755, exist_ok=True)

    ### Iterate through every input '.content' file(s) and create a global
    #   dataframe.
    lst_df = []

    threads = cmn.number_thread(args.threads)

    if nb_input_file > 1:
        with Pool(threads) as pool:
            lst_df = pool.map(
                partial(workers, fraction = args.fraction, ind_outdir_path = ind_outdir_path), 
                lst_fpath
            )

        # if an element of the list is null 
        lst_df = [i for i in lst_df if isinstance(i, pd.DataFrame)]

        ### Create a global dataframe from all the libraries (or from the only one
        #   if only one library is provided)
        if len(lst_df) > 0:
            df_glob = pd.concat(lst_df).reset_index(drop=True)
        else:
            print("All the files containing nothing", file = sys.stderr)
            exit(1)
    else: 
        fpath = lst_fpath[0]
        df_glob = pd.read_csv(fpath, sep = "\t")

        lib_name = os.path.splitext(os.path.basename(fpath))[0]
        df_glob["library"] = lib_name

        if len(df_glob)>1:
            df_glob = sub_sample_reads(df_glob, args.fraction)
    
    

    ### Generate a global plot over all the input libraries
    #
    if len(df_glob)>1:
        glob_distrib_plot = grph.DistributionPLot(
            os.path.join(args.outdir, f"ReadsDistribution_{args.prefix}.pdf"),
            df_glob,
            title=args.prefix,
        )
        glob_distrib_plot.create_graph()
        glob_distrib_plot.save_graph()
        ### Save basic stats about reads' length and quality (global)
        #
        basic_stats(df_glob, args.outdir, args.prefix)

    else:
        print("No information provided in the input file(s). The program will stop")
