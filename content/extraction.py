import os
import sys
import subprocess


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
    with open(fp_stdout,"w") as out, open(fp_stderr,"w") as err:
        out.write(str(stdout))
        err.write(str(stderr))

def extract_infos_from_fastq(fp_input, fp_output):
    """
    Execute a C++ program as a subprocess to extract informations 
    from a .fastq file.
    
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
    fp_input    (str) -- input fastq/fastq.gz file path
    fp_output   (str) -- output tab separated file path
    """
    prefix = os.path.splitext(fp_output)[0]
    fp_stdout = prefix+'.stdout'
    fp_stderr = prefix+'.stderr'
    if os.path.exists('build/fastq_processor'):
        cmd = f"build/fastq_processor {fp_input} {fp_output}"
        launch_subprocess(cmd, fp_stdout, fp_stderr)
    else:
        print("Can't find build/fastq_processor. Please compile the program and store it in the build repository")
        sys.exit()


def main(args):
    ### Set the input/ouput paths
    #
    input_fpath = os.path.abspath(args.inputfilepath)
    output_dir = os.path.abspath(args.outputdirpath)
    
    ## Create the output directory if it does not exist
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir, mode=0o755, exist_ok=True)
        
    output_fpath = os.path.join(output_dir, 
                                os.path.splitext(os.path.basename(input_fpath))[0] + ".content"
                                )


    ### Parse fastq file using the fastq_processor C++ program
    #
    extract_infos_from_fastq(input_fpath, output_fpath)
