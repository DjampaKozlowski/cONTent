import sys 
import os 
import pandas as pd


import content.utils as utl 
import content.graphs as grf


input_fpath=os.path.abspath('/Users/dkozlowski/Documents/work/scripts/cONTent/data/guppy_sup/incognita')
output_dir=os.path.abspath('/Users/dkozlowski/Documents/work/scripts/cONTent/tmp/')
individual=True
fraction=0.0001
prefix='incognita_sup'
prefix = prefix.strip('_')




### List the  files in the input directory 
#
lst_infiles = utl.lst_files_in_dir(input_fpath, '.tsv')
print(lst_infiles)

### Create a directory named 'per_lib' which will contain 
#   an instance of the reads quality/length distribution plos
#   for each library
#
#   NB : existing files/directories will be overwritten.
#
os.makedirs(os.path.join(output_dir, 'individual'), 
            mode=0o755, exist_ok=True)

### Iterate through every '.content' file from the input directory
#
lst_df = []
for fpath in lst_infiles:
    df = pd.read_csv(fpath, sep='\t')
    lib_name = os.path.splitext(os.path.basename(fpath))[0]
    df['library'] = lib_name
    lst_df.append(df)
    # ## Create individual QC graph (reads length vs quality)
    # ind_reads_qc = grf.QualAndLenDistrib(df)
    # ind_reads_qc.subsample(fraction)
    # ind_reads_qc.create_graph(title=lib_name)
    # ind_reads_qc.save_graph(os.path.join(os.path.join(output_dir, 'individual'), 
    #                                         lib_name+'.pdf'))      
        
df_glob = pd.concat(lst_df)
# ## Create a global QC graph (reads length vs quality)
# reads_qc = grf.QualAndLenDistrib(df_glob)
# reads_qc.subsample(fraction)
# reads_qc.create_graph(title=prefix)
# reads_qc.save_graph(os.path.join(output_dir, f'Reads_length_and_quality_distribution_{prefix}.pdf'))

grf.QualAndLengthTradeoff(df_glob, 
                          183000000, 
                          os.path.join(output_dir, f'Coverage_opti{prefix}.pdf'),
                          prefix, n=100, m=100, min_cov=50)
    


