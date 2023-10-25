CXX = g++               # Compiler
CXXFLAGS = -std=c++11    # Compiler flags
TARGET = fastq_processor # Output executable name

install:
	mkdir -p content/build/
	$(CXX) $(CXXFLAGS) content/fastq_processor.cpp -o content/build/fastq_processor