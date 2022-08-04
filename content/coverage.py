import sys
import os

import pandas as pd
import numpy as np
sns.set_style("white")

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

    def __init__(self, df, genome_size, n=10, m=10, min_cov=None, 
                 min_length=1000, min_quality=12):
        
        self.genome_size = genome_size
        self.min_quality = min_quality
        self.n=n
        self.m=m 
        self.min_cov=min_cov
        self.data = df[(df.read_length >= min_length)\
            & (df.read_avg_quality >= min_quality)].copy()

    def split_length_space(self):
            """
            Split length space into n even intervals (log scale)
            """
            self.scl_l = np.flip(np.geomspace(start=self.data.read_length.min(),
                                                stop=self.data.read_length.max(),
                                                num=self.n))
            
    def split_quality_space(self):
        """
        Split quality space into m even intervals (linear scale)
        """
        self.scl_q= np.flip(np.linspace(start=self.data.read_avg_quality.min(),
                                            stop=self.data.read_avg_quality.max(),
                                            num=self.m))    

    def compute_coverage(self):
        """
        Compute genome coverage for different length and quality 
        thresholds. 
        """
        self.split_length_space()
        self.split_quality_space()
        lst_dct = []
        for q in self.scl_q:
            for l in self.scl_l:
                L = self.data[(self.data.read_length >= l) & (self.data.read_avg_quality >= q)].read_length.sum()
                C = L/self.genome_size
                lst_dct.append(
                    {'min_length':l,
                    'min_quality':q,
                    'total_length':L,
                    'coverage':C}
                    )
        self.coverage = pd.DataFrame(lst_dct)
        if self.min_cov:
            self.coverage = self.coverage[self.coverage.coverage >= self.min_cov]



def main(args):
    ### List the files pointed by  args.input
    #
    lst_fpath = cmn.lst_content_files(args.input)
    if len(lst_fpath) == 0:
        print("No .content file found at the given adress. Program will end")
        sys.exit()
    
    ### Create the output directory tree 
    #   NB : existing files/directories will be overwritten.
    #
    os.makedirs(args.outdir, 
                mode=0o755, 
                exist_ok=True)
    
    ### Iterate through every input '.content' file(s) and create a global 
    #   dataframe.
    lst_df = []
    for fpath in lst_fpath:
        df = pd.read_csv(fpath, sep='\t')
        lst_df.append(df)
    
    ### Create a global dataframe from all the libraries
    #  
    df_glob = pd.concat(lst_df)
    
    ### Compute coverage for different values of reads quality and length
    #
    genome_coverage = GenomeCoverage(
        df_glob,
        args.genomesize,
        n=args.n, 
        m=args.m, 
        min_cov=args.mincoverage
        )
    genome_coverage.compute_coverage()
    df_coverage = genome_coverage.coverage
    
    ### Create and save the optimization plot (global dataframe)
    #
    plot_coverage = grph.CoveragePlot(
        os.path.join(args.outdir, f'Coverage_{args.prefix}.pdf'),
        df_coverage,
        title=args.prefix,
        )
    plot_coverage.create_graph()
    plot_coverage.save_graph()
    
    ### Save the coverage dataframe
    #
    df_coverage.to_csv(
        os.path.join(args.outdir, f'Coverage_{args.prefix}.tsv'),
        sep='\t',
        index=False
    )    
    