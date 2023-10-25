#include <iostream>
#include <fstream>
#include <string>
#include <cmath>

using namespace std;

class FastqProcessor {
public:
    FastqProcessor(const string& inputFilePath, const string& outputFilePath)
        : inputFilePath(inputFilePath), outputFilePath(outputFilePath) {}

    void process_fastq_file() {
        //  Open the input file
        ifstream input_file(inputFilePath);
        if (!input_file.is_open()) {
            cerr << "Error: unable to open the input file" << inputFilePath << endl;
            return;
        }

        //  Open the output file
        ofstream output_file(outputFilePath);
        if (!output_file.is_open()) {
            cerr << "Error: unable to open the output file" << endl;
            return;
        }

        //  Add the columns names in the output file (first line)
        output_file << "read_name\tread_length\tread_avg_quality" << endl;

        //  Init the vars were the data will be stored.
        string sequence;
        string header;
        string quality;
        unsigned short int line_count = 0;
        int i = 0;
        bool all_quality_content=true;
        unsigned long int seq_len = 0;


        double tab_quality[129];
        for (int q = 0; q < 129 ; q ++) {
            tab_quality[q] = pow((double)10, -((double)q) / 10.0);
        }

        //  Read the input file line per line
        string line;
        while (getline(input_file, line)) {
            if (line[0] == '@' && all_quality_content) {  // header lines
                if (!sequence.empty()) {
                    double avg_quality = 0.0;
                    for (int i = 0; i < quality.length(); i++) {
                        avg_quality += tab_quality[(int)quality[i] - 33];
                    }
                    avg_quality /= (double)quality.length();
                    output_file << header.substr(1) << "\t" << sequence.length() << "\t" << -10 * log10(avg_quality) << endl;
                    sequence.clear();
                    quality.clear();
                }
                for (char& c : line) {
                    if (c != ' ') i++;
                    else break;
                }
                header = line.substr(0, i);
                line_count = 1;
                i = 0;
                all_quality_content = false;
            } else if (line_count == 1) {  // Sequence
                if (line == (string)"+") { 
                    line_count = 3;
                    seq_len = sequence.length();
                    continue;
                }
                sequence += line;
            } else if (line_count == 3) {  // Quality
                quality += line;
                if (quality.length() == seq_len) { 
                    all_quality_content=true;
                }
            }
        }

        //  Compute the mean Phred quality Afficher le Phred quality score moyen de la dernière séquence du fichier fastq
        if (!sequence.empty()) {
            double avg_quality = 0.0;
            for (int i = 0; i < quality.length(); i++) {
                avg_quality += tab_quality[(int)quality[i] - 33];
            }
            avg_quality /= (double)quality.length();
            output_file << header.substr(1) << "\t" << sequence.length() << "\t" << -10 * log10(avg_quality) << endl;
        }

        // Fermer les fichiers
        input_file.close();
        output_file.close();
    }

private:
    string inputFilePath;
    string outputFilePath;
};


int main(int argc, char* argv[]) {
    //  Check if the two filenames have been provided
    if (argc < 3) {
        cerr << "Missing input and/or output file path(s)" << endl;
        return 1;
    }

    string inputFilePath = argv[1]; // Input Fastq file path
    string outputFilePath = argv[2]; // Output text file pat

    FastqProcessor processor(inputFilePath, outputFilePath);
    processor.process_fastq_file();

    cout << "Fastq processing complete. Results saved in " << outputFilePath << "." << endl;

    return 0;
}


