import sys
import os

import pandas as pd
import numpy as np
import time

import content.common as cmn
import content.graphs as grph


class GenomeCoverage:
    """
    Compute genome coverage for different read length and quality values.

    Usefull information to decide what minimal reads length and quality set to
    reach a target coverage.

    1) Filter reads on a basis of minimal quality and length
    2) Divide the quality and length spaces into envely distributed intervals
    3) Compute coverage for each pair of interval


    Attributes :
    ------------
    df (pandas dataframe)   --  dataframe containing the following columns :
                                'read_length' and 'read_avg_quality'.
    genome_size (int)       --  genome size (bp).
    n (int)                 --  number of reads length space split. Increasing
                                n makes the analysis more precise but also more
                                time consuming (default : 10).
    m (int)                 --  number of reads quality space split.
    min_cov (number)        --  minimum coverage to represent (default: None)
    min_length (number)     --  minimum read size to conside to compute
                                coverage.
    min_quality (number)    --  minimum read quality to consider to compute
                                coverage.
    data (pandas dataframe) --  table storing the coverage for different read
                                length and quality trade-offs.

    Methods :
    ---------
    split_length_space()    --  Split length space into n even intervals (log
                                scale)
    split_quality_space()   --  Split quality space into m even intervals
                                (linear scale)
    compute_coverage()      --  Compute genome coverage for different length
                                and quality thresholds.
    """

    def __init__(
        self, df, genome_size, n=10, m=10, min_cov=20, min_length=1000, min_quality=12
    ):

        self.genome_size = genome_size
        self.min_quality = min_quality
        self.n = n
        self.m = m
        self.min_cov = min_cov
        self.data = df[
            (df.read_length >= min_length) & (df.read_avg_quality >= min_quality)
        ].copy()

    def split_length_space(self):
        """
        Split length space into n even intervals (log scale)
        """
        self.scl_l = np.unique(
            np.flip(
                np.geomspace(
                    start=self.data.read_length.min(),
                    stop=self.data.read_length.max(),
                    num=self.n,
                )
            ).astype(int)
        )

    def split_quality_space(self):
        """
        Split quality space into m even intervals (linear scale)
        """
        self.scl_q = np.flip(
            np.linspace(
                start=self.data.read_avg_quality.min(),
                stop=self.data.read_avg_quality.max(),
                num=self.m,
            )
        )

    def compute_coverage(self):
        """
        Compute genome coverage for different length and quality
        thresholds.
        """
        self.split_length_space()
        self.split_quality_space()

        df = pd.DataFrame({"min_length": self.scl_l}).merge(
            pd.DataFrame({"min_quality": self.scl_q}), how="cross"
        )

        df["total_length"] = np.nan

        for l in self.scl_l:
            df_out = self.data[self.data.read_length >= l]

            qmin = df_out.read_avg_quality.min()
            qmax = df_out.read_avg_quality.max()

            scl_q_tmp = self.scl_q[(self.scl_q >=  qmin) & (self.scl_q <= qmax) ]

            L = 0
            for q in scl_q_tmp:

                L = df_out[df_out.read_avg_quality >= q].read_length.sum()

                df.loc[(df.min_length == l) & (df.min_quality == q), "total_length"] = L

            df.loc[(df.min_length == l) & (df.min_quality <= qmin), "total_length"] = L

        df = df.dropna()
        df["coverage"] = df.total_length / self.genome_size

        ### Check if the actual coverage is superior to the required minimum 
        #   coverage to display
        if df.coverage.max() < self.min_cov:
            print(f"""Maximum genome coverage ({np.round(df.coverage.max(),2)} X) 
                  computed from the provided file with the specified genome 
                  size ({self.genome_size} bp)and the minimum required 
                  quality ({self.min_quality}) is inferior to the minimum 
                  coverage required ({self.min_cov})""")
            print("Please, re-run the program with a lower '-mincoverage' value")
            sys.exit()
        
        else:
            self.coverage = df[df.coverage >= self.min_cov] 

        #self.coverage = df
        #if self.min_cov:
        #    self.coverage = self.coverage[self.coverage.coverage >= self.min_cov]

@cmn.time_d
def main(args):
    """
    Execute the whole analysis.

    TODO : make intermediate functions to make the program more versatile,
    especially to be able to use the functions in a notebook for instance.
    """
    print("Starting cONTent coverage analysis")

    ### List the files pointed by  args.input
    #
    #   TODO : replace '.content' extension by a test that check the input
    #   dataframe has the right number of columns and the right columns
    #   names.
    lst_fpath = cmn.lst_content_files(args.input)
    if len(lst_fpath) == 0:
        print("No .content file found at the given adress. Program will end")
        sys.exit()

    ### Create the output directory tree
    #   NB : existing files/directories will be overwriting.
    #
    os.makedirs(args.outdir, mode=0o755, exist_ok=True)

    ### Iterate through every input '.content' file(s) and create a global
    #   dataframe.

    ### Create a global dataframe from all the libraries
    #
    df_glob = pd.concat([pd.read_csv(fpath, sep="\t") for fpath in lst_fpath])

    ### Compute coverage for different values of reads quality and length
    #
    genome_coverage = GenomeCoverage(
        df_glob,
        args.genomesize,
        n=args.n,
        m=args.m,
        min_cov=args.mincoverage,
        min_length=args.minlength,
        min_quality=args.minquality,
    )
    genome_coverage.compute_coverage()
    df_coverage = genome_coverage.coverage

    ### Create and save the optimization plot (global dataframe)
    #
    plot_coverage = grph.CoveragePlot(
        os.path.join(args.outdir, f"Coverage_{args.prefix}.pdf"),
        df_coverage,
        title=args.prefix,
    )
    plot_coverage.create_graph()
    plot_coverage.save_graph()

    ### Save the coverage dataframe
    #
    df_coverage.to_csv(
        os.path.join(args.outdir, f"Coverage_{args.prefix}.tsv"), sep="\t", index=False
    )

