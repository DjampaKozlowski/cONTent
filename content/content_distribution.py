import sys 
import os
import pandas as pd


import content.utils as utl 
import content.graphs as grf
import content.interface as itf


# input_fpath=os.path.abspath('/Users/dkozlowski/Documents/work/scripts/cONTent/data/guppy_sup/incognita')
# output_dir=os.path.abspath('/Users/dkozlowski/Documents/work/scripts/cONTent/tmp/')
# individual=True
# fraction=0.0001
# prefix='incognita_sup'
# prefix = prefix.strip('_')
# n = 100
# m = 100
# min_cov = 50
# genome_size=183000000

### Get the script arguments. 
#
args = itf.arguments_parser_graph()

### List the  file(s) pointed by the input path 
#
if os.path.isdir(args.input):
    lst_infiles = utl.lst_files_in_dir(args.input, '.content')
elif os.path.isfile(args.input) and args.input.endswith('.content'):
    lst_infiles = [os.path.abspath(args.input)]
else:
    print("Input path do not point to any '.content' file. Program execution will end.")
    sys.exit()
    
### Create the output directory tree as well as a sub-dir named 'individual 
#   where per-lib results will be stored
#   NB : existing files/directories will be overwritten.
#
os.makedirs(os.path.join(args.outdir, 'individual'), 
            mode=0o755, exist_ok=True)

# ### Iterate through every '.content' file from the input directory
# #
# lst_df = []
# for fpath in lst_infiles:
#     df = pd.read_csv(fpath, sep='\t')
#     lib_name = os.path.splitext(os.path.basename(fpath))[0]
#     df['library'] = lib_name
#     lst_df.append(df)
#     grf.PlotDistrib(
#         os.path.join(os.path.join(output_dir, 'individual'), lib_name+'.pdf'),
#         df,
#         frac=fraction,
#         title=lib_name
#         )
    
# ### Create a global dataframe from all the libraries
# #  
# df_glob = pd.concat(lst_df)

# ### Create and save the distribution plot (global dataframe)
# #
# grf.PlotDistrib(
#     os.path.join(output_dir, f'Reads_length_and_quality_distribution_{prefix}.pdf'),
#     df_glob,
#     frac=fraction,
#     title=prefix
#     )

# ### Create and save the optimization plot (global dataframe)
# #
# grf.PlotCoverageTradeoff(
#     os.path.join(output_dir, f'Coverage_opti{prefix}.pdf'),
#     df_glob,
#     genome_size,
#     title=prefix,
#     n=n, 
#     m=m, 
#     min_cov=min_cov
#     )
    


