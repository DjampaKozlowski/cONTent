import argparse
from multiprocessing import cpu_count


PROG_DESCRIPTION = """
cONTent is a tool-box allowing the analysis of ONT long-reads length and quality.

cONTent tool-box contains 3 sub-programs:
- extract
- distribution 
- coverage

Execute `python cONTent.py < extract | distribution | coverage > -h` for more information or
`content < extract | distribution | coverage > -h` for more information
"""


def arguments_parser():

    parser = argparse.ArgumentParser(prog="content.py", description=PROG_DESCRIPTION)
    subparsers = parser.add_subparsers(dest="sub_prog")

    scan_p = subparsers.add_parser(
        "extract",
        description="""Parse read library (/!\ SHOULD BE A FASTQ FILE AND NOT A FASTQ.GZ) and for each 
        read extract the read's name, length, and average quality. Save the 
        results as a tab separated file with the following name :
        '<input_file_name>.content'. Can be an directory""",
    )

    scan_p.add_argument(
        "-i",
        "--inputfilepath",
        help="input fastq file path or directory where there are fastq",
        type=str,
        required=True,
    )
    scan_p.add_argument(
        "-o",
        "--outputdirpath",
        help="""output directory path. Nb: if the ouput 
                        directory does not exist, it will be created along with
                        its parent directories. If only a directory name is 
                        provided, the directory will be created in the execution
                        directory. In any case,if the directory exist, it will 
                        be overwritten as well as the files it might contain.""",
        type=str,
        required=True,
    )

    scan_p.add_argument(
        "-t", 
        "--threads", 
        help= f"Number of threads allowed (default all cpus)",
        type=int,
        default = cpu_count()
    )

    dist_p = subparsers.add_parser(
        "distrib",
        description="""Parse .content file(s) and create for each file a
        representation of the reads length and quality distribution. If several 
        files are provided, also compute a global figure.""",
    )
    dist_p.add_argument(
        "-input",
        help="""Input directory/file path. If the path point to 
                        a directory, all the '.content' files will be analysed 
                        (individually and together).""",
        type=str,
        required=True,
    )
    dist_p.add_argument(
        "-outdir",
        help="""Output directory path. Nb: if the ouput 
                        directory does not exist, it will be created along with
                        its parent directories. If only a directory name is 
                        provided, the directory will be created in the execution
                        directory. In any case,if the directory exist, it will 
                        be overwritten as well as the files it might contain.
                        """,
        type=str,
        required=True,
    )
    dist_p.add_argument(
        "-prefix",
        help="""Prefix used to name output files but also as  
                        plots' title (for global analysis). Spaces will be 
                        replaced with '_' in the files names""",
        type=str,
        required=True,
    )
    dist_p.add_argument(
        "-fraction",
        help="""fraction of reads to subsample per analysed 
                        library (distribution plot only). The more important 
                        is the fraction, the most time consuming the analysis 
                        will be. (default : 0.01)""",
        type=float,
        default=0.01,
    )

    dist_p.add_argument(
        "-t", 
        "--threads", 
        help= f"Number of threads allowed (default all cpus)",
        type=int,
        default = cpu_count()
    )


    cov_p = subparsers.add_parser(
        "coverage",
        description="""Parse .content files and create a representation of 
        genome coverage for different thresholds of reads length and quality. 
        This information can be used to set minimal reads length and quality 
        to reach a target genome coverage.""",
    )

    cov_p.add_argument(
        "-input",
        help="""Input directory/file path. If the path point to 
                        a directory, all the '.content' files will be analysed 
                        (individually and together).""",
        type=str,
        required=True,
    )
    cov_p.add_argument(
        "-outdir",
        help="""Output directory path. Nb: if the ouput 
                        directory does not exist, it will be created along with
                        its parent directories. If only a directory name is 
                        provided, the direcotry will be created in the execution
                        directory. In any case,if the directory exist, it will 
                        be overwritten as well as the files it might contain.
                        """,
        type=str,
        required=True,
    )
    cov_p.add_argument(
        "-prefix",
        help="""Prefix used to name output files but also as  
                        plots' title (for global analysis). Spaces will be 
                        replaced with '_' in the files names""",
        type=str,
        required=True,
    )
    cov_p.add_argument(
        "-genomesize",
        help="""genome size (bp). Necessary to compute genome
                        coverage""",
        type=int,
        required=True,
    )

    cov_p.add_argument(
        "-n",
        help="""Number of interval to create in reads length 
                        space (optimization plot only; used to compute coverage)
                        Increasing n makes the coverage length/quality trade-off
                        analysis more precise but also more time consuming.  
                        (default : 100)""",
        type=int,
        default=100,
    )
    cov_p.add_argument(
        "-m",
        help="""Number of interval to create in reads quality 
                        space (optimization plot only; used to compute coverage)
                        Increasing n makes the coverage length/quality trade-off
                        analysis more precise but also more time consuming.  
                        (default : 100)""",
        type=int,
        default=100,
    )
    cov_p.add_argument(
        "-mincoverage",
        help="""Minimal coverage to represent (optimization plot 
                        only) (default : 20)""",
        type=int,
        default=20,
    )
    cov_p.add_argument(
        "-minquality",
        help="""Minimal quality to represent (optimization plot 
                        only) (default : 12)
        """,
        type=int,
        default=12,
    )
    cov_p.add_argument(
        "-minlength",
        help="""Minimal length of sequences to represent (optimization plot 
                        only) (default : 1000)
        """,
        type=int,
        default=1000,
    )

    return parser.parse_args()
