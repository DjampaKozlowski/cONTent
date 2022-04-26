# cONTent 

## Description

cONTent parse a read library (fastq/fastq.gz) and for each read extract the read's :
- name
- length
- average quality. 

Then, save the results as a tab separated values file.

NB : This script entirely rely on Wouter De Coster's work and especially on the 'nanoget' module (see https://github.com/wdecoster/nanoget). 

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
pip install -r requirements.txt
cd cONTent/
pip install -e .
```

## Usage 

Activate the environment (if not already done)

```
conda activate content_env
```
Then launch the parsing

```
python cONTent.py [-h] -i INPUTFILEPATH -o OUTPUTFILEPATH [-t THREADS]
```
where:
- < INPUTFILEPATH > : input fastq/fastq.gz file path [mendatory]
- < OUTPUTFILEPATH > : output tsv file path [mendatory]
- < THREADS > : number of parallels workers. Is set to the maximum of available CPUs if <= 0 or if > to the maximum of available CPUs. [default : 1]. 
