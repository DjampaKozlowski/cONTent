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



def interface_content_QL():
    """
    Description :
    -------------
    Parse script arguments to get the following information:


    Returns :
    ---------
     *  -- object, parser object
    """
    parser = argparse.ArgumentParser(description="""Parse one or several 
                                     .content file(s) and compute a graph
                                     representing the distribution of read phred 
                                     quality and read length of a representative
                                     subset of reads.""")
    parser.add_argument("-i", 
                        "--input", 
                        help="""file (.content) or directory input path. 
                        If a directory is specified, all the .content files will
                        be pooled together [mendatory]""", 
                        type=str,
                        required=True)
    parser.add_argument("-o", 
                        "--outputdir", 
                        help="output directory path  [mendatory]", 
                        type=str,
                        required=True)
    
    parser.add_argument("-f", 
                        "--fraction", 
                        help="""fraction of the input data to represent. If the 
                        input is composed of multiple libraries, the subsampling
                        will be done per library. That way, each library will 
                        have the same weight on the representation. The more 
                        important is the fraction, the more heavy the 
                        computation will be. (default : 0.0001)""", 
                        type=float,
                        default=0.0001)    
    parser.add_argument("--prefix",
                        help="""prefix to include in graph title and output
                        files names. Prefix must be space free. If no prefix is 
                        specified and the input is a single file, the file 
                        basename will be used. If no prefix is specified and 
                        the input is a directory, the prefix will be set to 
                        'pooled_libraries'.""")
    return parser.parse_args()
    
    
def interface_content_opti():
    """
    Description :
    -------------
    Parse script arguments to get the following information:


    Returns :
    ---------
     *  -- object, parser object
    """
    parser = argparse.ArgumentParser(description="""Parse one or several 
                                     .content file(s) and compute a graph
                                     representing the distribution of read phred 
                                     quality and read length of a representative
                                     subset of reads.""")
    parser.add_argument("-i", 
                        "--input", 
                        help="""file (.content) or directory input path. 
                        If a directory is specified, all the .content files will
                        be pooled together [mendatory]""", 
                        type=str,
                        required=True)
    parser.add_argument("-o", 
                        "--outputdir", 
                        help="output directory path  [mendatory]", 
                        type=str,
                        required=True)
    
    parser.add_argument("-f", 
                        "--fraction", 
                        help="""fraction of the input data to represent. If the 
                        input is composed of multiple libraries, the subsampling
                        will be done per library. That way, each library will 
                        have the same weight on the representation. The more 
                        important is the fraction, the more heavy the 
                        computation will be. (default : 0.0001)""", 
                        type=float,
                        default=0.0001)    
    parser.add_argument("--prefix",
                        help="""prefix to include in graph title and output
                        files names. Prefix must be space free. If no prefix is 
                        specified and the input is a single file, the file 
                        basename will be used. If no prefix is specified and 
                        the input is a directory, the prefix will be set to 
                        'pooled_libraries'.""")
    return parser.parse_args()




def argument_parser_graphs():
    """
    Description :
    -------------
    Parse script arguments to get the following information:


    Returns :
    ---------
     *  -- object, parser object
    """
    parser = argparse.ArgumentParser(description="insert description")
    parser.add_argument("-i", 
                        "--input", 
                        help="""file (.content) or directory input path. 
                        If a directory is specified, all the .content files will
                        be pooled together [mendatory]""", 
                        type=str,
                        required=True)
    parser.add_argument("-o", 
                        "--outputdir", 
                        help="output directory path  [mendatory]", 
                        type=str,
                        required=True)
    
    
    
    parser.add_argument("--prefix",
                        help="""prefix to include in graph title and output
                        files names. Prefix must be space free. If no prefix is 
                        specified and the input is a single file, the file 
                        basename will be used. If no prefix is specified and 
                        the input is a directory, the prefix will be set to 
                        'pooled_libraries'.""")
    return parser.parse_args()
    
