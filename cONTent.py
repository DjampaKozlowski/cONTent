import sys 
import os 


from content.interface import arguments_parser
from content.utils import manage_cpus
from content.extraction import extract_infos_from_fastq



def main():
    ### Get the script arguments' values
    #
    args = arguments_parser()
    input_fpath = os.path.abspath(args.inputfilepath)
    output_fpath = os.path.abspath(args.outputfilepath)
    
    ### Check the number of available CPUs
    #
    nb_cpu = manage_cpus(args.threads)
    
    ### Parse fastq file
    #
    df = extract_infos_from_fastq(input_fpath, 
                                  nb_cpu)
    
    ### Save the results in a tab separated values file.
    #
    df.to_csv(output_fpath, 
              sep='\t',
              header=True,
              index=False)   
                                                  

if __name__ == "__main__":
    main()


    
    
    
                                   