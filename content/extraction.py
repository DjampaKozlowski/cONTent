import os
import pandas as pd


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
    return pd.DataFrame.from_records(
        nef.stream_fastq_full(fpath, threads),
        columns=["read_name", "read_length", "read_avg_quality", "other"],
    ).drop(columns="other")


def main(args):
    ### Set the input/ouput paths
    #
    input_fpath = os.path.abspath(args.inputfilepath)
    output_dir = os.path.abspath(args.outputdirpath)


    ### Parse fastq file
    #
    df = extract_infos_from_fastq(input_fpath, nb_cpu)

    ### Create the output directory tree as well as a sub-dir named 'individual
    #   where per-lib results will be stored
    #   NB : existing files/directories will be overwriting.
    #
    os.makedirs(output_dir, mode=0o755, exist_ok=True)

    ### Save the results in a tab separated values file.
    #
    output_fpath = os.path.join(
        output_dir, os.path.splitext(os.path.basename(input_fpath))[0] + ".content"
    )

    print(output_fpath)
    df.to_csv(output_fpath, sep="\t", header=True, index=False)
