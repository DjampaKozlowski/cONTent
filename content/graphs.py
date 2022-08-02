import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import sys
sns.set_style("white")


class GraphsReadsQualityAndLength:

    def __init__(self, df):
        self.df = df.copy()
        
    def create_distrib_graph(self):
        
        print('tutu')
        
        
    def create_opti_graph(self):
        print('tata')
        
 
    def subsample(self, frac=0.0001):
        self.data = self.data.groupby(by='library')\
            .sample(frac=frac)\
                .reset_index(drop=True)
                
    def save_graph(self, fpath):
        plt.savefig(fpath, bbox_inches='tight')
        
        
    def plot_quality_and_length_distrib(self):
        print('titou')
        
        
    def split_length_space(self):
        if self.min_length < self.df.read_length.max():
            self.scl_l = np.flip(np.geomspace(start=self.min_length,
                                              stop=self.df.read_length.max(),
                                              num=self.n))
        else:
            print("Requested min. read length >= actual maximum read length. Program will stop")
            sys.exit()
        
    def split_quality_space(self):
        if self.min_quality < self.df.read_length.max():
            self.scl_q= np.flip(np.linspace(start=self.min_quality,
                                            stop=self.df.read_avg_quality.max(),
                                            num=self.m))
        else:
            print("Requested min. read quality >= actual maximum read quality. Program will stop")
            sys.exit()   






class QualAndLenDistrib:
    
    def __init__(self, df):
        self.data = df
        
    def subsample(self, frac=0.0001):
        self.data = self.data.groupby(by='library')\
            .sample(frac=frac)\
                .reset_index(drop=True)
                
    def create_graph(self, title=None, fig_height=12, width_ratio=5):
        self.graph = sns.JointGrid(height=fig_height,ratio=width_ratio)
        sns.histplot(data=self.data, 
                    x='read_length', 
                    y='read_avg_quality',
                    ax=self.graph.ax_joint,
                    log_scale=(True, False))
        sns.boxplot(data=self.data, x='read_length',ax=self.graph.ax_marg_x, color='white')
        sns.boxplot(data=self.data, y='read_avg_quality',ax=self.graph.ax_marg_y, color='white')
        self.graph.refline(x=self.data.read_length.median(), 
                y=self.data.read_avg_quality.median())
        self.graph.ax_joint.set_xlabel("length (bp) [log-scale]", fontsize=15, y=-0.2)
        self.graph.ax_joint.set_ylabel("quality (phred)", fontsize=15, x=-0.2)
        if title:    
            plt.suptitle(str(title), fontsize=20, y=1.05)
            
    def save_graph(self, fpath):
        plt.savefig(fpath, bbox_inches='tight')
        

        
        
class QualAndLengthTradeoff:
    
    def __init__(self, df, genome_size, fpath, title=None, n=10, m=10, min_cov=None, 
                 min_length=1000, min_quality=12, figsize=(12,10)):
        self.df = df[(df.read_length >= min_length) & (df.read_avg_quality >= min_quality)].copy()
        print(self.df.describe())
        self.genome_size = genome_size
        self.fpath = fpath
        self.min_cov = min_cov
        self.min_length = min_length
        self.min_quality = min_quality
        self.n=n
        self.m=m 
        self.title = title
        self.figsize = figsize
        self.split_length_space()
        self.split_quality_space()
        self.compute_coverage()
        self.create_graph()
        self.save_graph()
        
        
        
    def split_length_space(self):
        if self.min_length < self.df.read_length.max():
            self.scl_l = np.flip(np.geomspace(start=self.min_length,
                                              stop=self.df.read_length.max(),
                                              num=self.n))
        else:
            print("Requested min. read length >= actual maximum read length. Program will stop")
            sys.exit()
        
    def split_quality_space(self):
        if self.min_quality < self.df.read_length.max():
            self.scl_q= np.flip(np.linspace(start=self.min_quality,
                                            stop=self.df.read_avg_quality.max(),
                                            num=self.m))
        else:
            print("Requested min. read quality >= actual maximum read quality. Program will stop")
            sys.exit()        
        
        
                
    def compute_coverage(self):
        """
        Compute genome coverage in function of different length and quality 
        thresholds. Split the length and quality space evenly according to n 
        (number of bins for reads length) and m (number of bins for reads quality) 
        parameters. 
        
        Parameters : 
        -----------
        df (pandas dataframe) -- a dataframe with the following 
        columns : 'read_length' and 'read_avg_quality'
        genome_size (int) -- the genome size (bp)
        n (int) -- number of reads length bins. Data space will be evenly cut 
        (log scale)
        m (int) -- number of reads quality bins.Data space will be evenly cut.
        
        """

        lst_dct = []
        for q in self.scl_q:
            for l in self.scl_l:
                L = self.df[(self.df.read_length >= l) & (self.df.read_avg_quality >= q)].read_length.sum()
                C = L/self.genome_size
                lst_dct.append(
                    {'min_length':l,
                    'min_quality':q,
                    'total_length':L,
                    'coverage':C}
                    )
        self.data = pd.DataFrame(lst_dct)
        if self.min_cov:
            self.data = self.data[self.data.coverage >= self.min_cov]
        
        
        
        
    def create_graph(self):
        """
        Create a heatmap from coverage values at different quality and length 
        cut-off. Min. quality is represented on the y axis and length on the x axis.
        
        Parameters : 
        ------------
        df (pandas dataframe) -- coverage dataframe. A dataframe whith the 3 
        following columns :  'coverage', 'min_length', 'min_quality'.
        title (str) -- figure title
        figsize (tuple) -- figure width and height
        min_cov (number) -- minimum coverage to represent
        min_length (number) -- minimum length to represent
        min_quality (number) -- minimum quality to represent. 
        """
        plt.figure(figsize=self.figsize)
        ax1 = sns.heatmap(
            self.data[['min_quality', 'min_length', 'coverage']].round(1)\
                .pivot(index='min_quality', columns='min_length', values='coverage'),
                    cbar_kws = dict(location="bottom"))
        ax1.figure.axes[-1].set_xlabel('Coverage (X)', size=15)

        if self.title:
            plt.title(self.title, fontsize=20)
        plt.xlabel("min. length (bp)", fontsize=15)
        plt.ylabel("min. quality (phred)", fontsize=15)
        plt.xticks(rotation=90);
            
    def save_graph(self):
        plt.savefig(self.fpath)
