import sys 
import os 


import content.interface as itf
import content.utils as utl
import content.extraction as xtr




def main():
    ### Get the script arguments' values
    #
    args = itf.arguments_parser()
    input_fpath = os.path.abspath(args.inputfilepath)
    output_fpath = os.path.abspath(args.outputfilepath)

    ### Check the number of available CPUs
    #
    nb_cpu = utl.manage_cpus(args.threads)
    
    ### Parse fastq file
    #
    df = xtr.extract_infos_from_fastq(input_fpath, 
                                  nb_cpu)
    
    ### Save the results in a tab separated values file.
    #
    
    # add proper extension 
    
    df.to_csv(output_fpath, 
              sep='\t',
              header=True,
              index=False)   
                                                  

if __name__ == "__main__":
    main()


    
    
    
                                   