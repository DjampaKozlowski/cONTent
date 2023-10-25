CXX = g++               # Compiler
CXXFLAGS = -std=c++11    # Compiler flags


install:
	echo "Installing python requirements & installing the content module"
	pip install -r requirements.txt
	pip install -e .
	echo "Building the fastq parser"
	mkdir -p content/build/
	$(CXX) $(CXXFLAGS) content/fastq_processor.cpp -o content/build/fastq_processor
