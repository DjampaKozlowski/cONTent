import os
import sys
import subprocess
import time
import numpy as np
from functools import partial
from multiprocessing import Pool, cpu_count

import content.common as cmn


def launch_subprocess(cmd, fp_stdout, fp_stderr):
    """
    Launch a subprocess and create logs files
    
    Parameters :
    ------------
    cmd         (str)   --  the command line 
    fp_stdout   (str)   --  standard output file path
    fp_stderr   (str)   --  standard error file path
    """
    sub_call = subprocess.Popen(cmd, shell=True,  stdout=subprocess.PIPE)
    stdout, stderr = sub_call.communicate()

    if stderr:
        with open(fp_stderr,"w") as err:
            err.write(stderr.decode("utf-8"))

    if stdout:
        with open(fp_stdout,"w") as out:
            out.write(stdout.decode("utf-8"))


def extract_infos_from_fastq(fp_input, fp_output):
    """
    Execute a C++ program as a subprocess to extract informations 
    from a .fastq file.
    
    For each reads contained in a .fastq file, extract :
        - the read name
        - the read length
        - the average read quality
    and save the results as a tab separated file.

    Parameters :
    ------------
    fp_input    (str) -- input fastq/fastq.gz file path
    fp_output   (str) -- output tab separated file path
    """
    prefix = os.path.splitext(fp_output)[0]
    fp_stdout = prefix+'.stdout'
    fp_stderr = prefix+'.stderr'
    fp_fastq_processor = os.path.join(os.path.dirname(__file__), 'build','fastq_processor')
    if os.path.exists(fp_fastq_processor):
        cmd = f"{fp_fastq_processor} {fp_input} {fp_output}"
        launch_subprocess(cmd, fp_stdout, fp_stderr)
    else:
        print(f"Can't find {fp_fastq_processor}. Please compile the program and store it in the build repository")
        sys.exit()

def workers(input_fpath: str, outdir: str):
    output_fpath = os.path.join(
        outdir, 
        os.path.splitext(os.path.basename(input_fpath))[0] + ".content"
    )

    ### Parse fastq file using the fastq_processor C++ program
    #
    extract_infos_from_fastq(input_fpath, output_fpath)
    print(input_fpath, output_fpath)


def main(args):
    print("Starting cONTent extract analysis")
    start_time = time.time()

    ### Set the input/ouput paths
    input_fpath = os.path.abspath(args.inputfilepath)
    output_dir = os.path.abspath(args.outputdirpath)

    threads = cpu_count() if args.threads == 0 else min(args.threads, cpu_count())

    lst_files = cmn.lst_files(input_fpath, ".fastq")

    ## Create the output directory if it does not exist
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir, mode=0o755, exist_ok=True)

    with Pool(processes=threads) as pool:
        pool.map(partial(workers, outdir= output_dir), lst_files)

    stop_time = time.time()
    print(f"duration : {np.round(stop_time-start_time, 3)} s")