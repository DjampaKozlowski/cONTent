# cONTent 

## Description
cONTent is a tool-box allowing the analysis of ONT long-reads length and quality.

cONTent is composed of 3 sub-programs:
- extract : parse a read library and extract each reads' id, length and average phred quality. Then results are saved as tab-separated file with a '.content' extension. This tool is based on the nanoget package (https://github.com/wdecoster/nanoget) developped by Wouter De Coster. The extracted
information are per read identifier, length, and mean quality (phred score).
- distribution : subsample read-librar(y/ies) and plot reads' quality as a function of the reads' length. Also compute basic statistics for these two measurments. NB : if several libraries are provided, individual plot and statistics will be generated for each library in addition to a global plot and table.  
- coverage : compute genome coverage using different length and quality cut-offs. Display the results as a heatmap. This program might be usefull to set minimal reads length and quality cut-off to reach a target genome coverage. NB : The output table only display rows for which the coverage obtained with these values of minimal reads' length and quality satisfies the required coverage.

Programs usages and ouputs are extensively described the 'Usage' section below. 

## Installation 

Clone the repository in the desired location
```
git clone git@github.com:DjampaKozlowski/cONTent.git
```

Then, exectute the following lines. These lines will :
- create a python 3.10.4 conda environment named 'content_env'
- activate the 'content_env'
- install the required dependencies and set the enviroment as follow : biopython==1.79, certifi==2021.10.8, nanoget==1.16.1, numpy==1.22.3, pandas==1.4.2, pysam==0.19.0, python-dateutil==2.8.2, pytz==2022.1, six==1.16.0 .
- install the package.

```
conda create -n content_env -y python=3.10.4
conda activate content_env
cd cONTent/
pip install -r requirements.txt
pip install -e .
```

## Usage 

Activate the environment (if not already done)

```
conda activate content_env
```

NB : parameters between brackets are optional parameters with default values.

### extract

Launch cONTent.py extract doing :

```
python cONTent.py extract [-h] -i INPUTFILEPATH -o OUTPUTFILEPATH [-t THREADS]
```
where:
- < INPUTFILEPATH > : input fastq/fastq.gz file path [mendatory]
- < OUTPUTFILEPATH > : output tsv file path [mendatory]
- < THREADS > : number of parallels workers. Is set to the maximum of available CPUs if <= 0 or if > to the maximum of available CPUs. [default : 1]. 

cONTent.py coverage can be parallelized both by :
- using multiple cores
- launching several runs, one for each reads library


### distrib

Launch cONTent.py distrib doing :

```
python cONTent.py distrib [-h] -input INPUTPATH -outdir OUTPUTPATH -prefix PREFIX [-fraction FRACTION]
```
- < INPUTPATH > : Input directory/file path. If the path point to a directory, all the '.content' files will be analysed (individually and together). [mendatory]
- < OUTPUTPATH > : Output directory path. Nb: if the ouput directory does not exist, it will be created along with its parent directories. If only a directory name is provided, the directory will be created in the execution directory. In any case,if the directory exist, it will be overwritten as well as the files it might contain (if files with the same name exist). [mendatory]
- < PREFIX > : Prefix used to name output files but also as plots' title (for global analysis). Spaces will be replaced with '_' in the files names [mendatory]. 
- < FRACTION > : fraction of reads to subsample per analysed library (distribution plot only). The biggest is the fraction, the longer the analysis will take. (default : 0.01)

###  coverage

Launch cONTent.py coverage doing :

```
python cONTent.py coverage [-h] -input INPUTPATH -outdir OUTPUTPATH -prefix PREFIX -genomesize GENOMESIZE [-n N] [-m M] [-mincoverage MINCOV]
```
- < INPUTPATH > : Input directory/file path. If the path point to a directory, all the '.content' files will be analysed (individually and together). [mendatory]
- < OUTPUTPATH > : Output directory path. Nb: if the ouput directory does not exist, it will be created along with its parent directories. If only a directory name is provided, the directory will be created in the execution directory. In any case,if the directory exist, it will be overwritten as well as the files it might contain (if files with the same name exist). [mendatory]
- < PREFIX > : Prefix used to name output files but also as plots' title (for global analysis). Spaces will be replaced with '_' in the files names [mendatory]. 
- < GENOMESIZE > : Genome size (bp). Necessary to compute genome coverage
- < N > : Number of interval to create in reads length space (optimization plot only; used to compute coverage). Increasing n makes the coverage length/quality trade-off analysis more precise but also more time consuming. (default : 100).
- < M > : Number of interval to create in reads quality space (optimization plot only; used to compute coverage)  Increasing n makes the coverage length/quality trade-offanalysis more precise but also more time consuming. (default : 100).
- < MINCOV > : Minimal coverage to represent (optimization plot only). (default : 50).





