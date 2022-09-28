# cONTent 

## Description
cONTent is a tool-box allowing the analysis of ONT long-reads length and quality.

cONTent is composed of 3 sub-programs:
- extract : parse a read library and extract each reads' id, length and average phred quality. Then results are saved as tab-separated file with a '.content' extension. This tool is based on the nanoget package (https://github.com/wdecoster/nanoget) developped by Wouter De Coster.
- distribution : subsample read-librar(y/ies) and plot reads' quality as a function of the reads' length. Also compute basic statistics for these two measurments. NB : if several libraries are provided, individual plot and statistics will be generated for each library in addition to a global plot and table.  
- coverage : compute genome coverage using different length and quality cut-offs. Display the results as a heatmap. This program might be usefull to set minimal reads length and quality cut-off to reach a target genome coverage.

Programs usages and ouputs are extensively described below. 

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

## cONTent.py usage 

Activate the environment (if not already done)

```
conda activate content_env
```

### extract


Launch cONTent.py extract doing :

```
python cONTent.py [-h] -i INPUTFILEPATH -o OUTPUTFILEPATH [-t THREADS]
```
where:
- < INPUTFILEPATH > : input fastq/fastq.gz file path [mendatory]
- < OUTPUTFILEPATH > : output tsv file path [mendatory]
- < THREADS > : number of parallels workers. Is set to the maximum of available CPUs if <= 0 or if > to the maximum of available CPUs. [default : 1]. 

### distrib

Launch cONTent.py disctrib doing :


###  coverage

Launch cONTent.py coverage doing :


NB : The output table only display rows for which the coverage obtained with these values of minimal reads' length and quality satisfies the required coverage.

