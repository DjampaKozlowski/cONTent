import argparse

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
