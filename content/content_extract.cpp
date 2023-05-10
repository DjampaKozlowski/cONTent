#include <iostream>
#include <fstream>
#include <string>
#include <cmath>
#include <filesystem>

namespace fs = std::filesystem;
using namespace std;

string get_filename_without_extension(const string& filepath) {
    // Trouver la dernière occurrence d'un séparateur de chemin
    size_t last_slash_pos = filepath.find_last_of("\\/");
    if (last_slash_pos == string::npos) {
        last_slash_pos = 0;
    } else {
        last_slash_pos++;
    }

    // Extraire le nom de fichier à partir du chemin
    string filename = filepath.substr(last_slash_pos);

    // Trouver la dernière occurrence d'un point dans le nom de fichier
    size_t last_dot_pos = filename.find_last_of(".");
    if (last_dot_pos == string::npos) {
        // Le nom de fichier ne contient pas d'extension
        return filename;
    } else {
        // Extraire le nom de fichier sans l'extension
        return filename.substr(0, last_dot_pos);
    }
}

bool create_directories_if_not_exists(const std::string& dirpath) {
    if (fs::exists(dirpath)) {
        // Le répertoire existe déjà
        return true;
    } else {
        // Le répertoire n'existe pas, on essaie de le créer
        if (fs::create_directories(dirpath)) {
            // std::cout << "Le répertoire " << dirpath << " a été créé avec succès.\n";
            return true;
        } else {
            std::cerr << "Erreur : impossible de créer le répertoire " << dirpath << ".\n";
            return false;
        }
    }
}



int main(int argc, char* argv[]) {
    // Vérifier si l'utilisateur a fourni un nom de fichier
    if (argc < 2) {
        cerr << "Usage: " << argv[0] << " filename" << endl;
        return 1;
    }

    // Ouvrir le fichier
    ifstream input_file(argv[1]);
    if (!input_file.is_open()) {
        cerr << "Erreur: impossible d'ouvrir le fichier " << argv[1] << endl;
        return 1;
    }

    string fileout = get_filename_without_extension((string)argv[1]);

    if (argc >= 3 ) {
        string output_dir = argv[2];
        create_directories_if_not_exists(output_dir);

        fileout = output_dir + "/" + fileout;
    }

    // Ouvrir le fichier de sorte
    ofstream output_file( fileout + (string)".content");
    if (!output_file.is_open()) {
        cerr << "Erreur: impossible d'ouvrir le fichier de sortie" << endl;
        return 1;
    }

    // Header
    output_file << "read_name	read_length	read_avg_quality" << endl;

    // Variables pour stocker les données
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

    // Lire le fichier ligne par ligne
    string line;
    while (getline(input_file, line)) {
        if (line[0] == '@' && all_quality_content) {  // Ligne d'en-tête
            if (!sequence.empty()) {
                double avg_quality = 0.0;
                for (int i = 0; i < quality.length(); i++) {
                    avg_quality += tab_quality[(int)quality[i] - 33];
                }
                avg_quality /= (double)quality.length();
                output_file << header.substr(1) << "\t" << sequence.length() << "\t" << -10 * log10(avg_quality) << endl;
                // cout << sequence.length() << "\t" << quality.length() << endl;
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
        } else if (line_count == 1) {  // Séquence
            if (line == (string)"+") { 
                line_count = 3;
                seq_len = sequence.length();
                continue;
            }
            sequence += line;
        } else if (line_count == 3) {  // Quality
            quality += line;
            if (quality.length() == seq_len) { 
                // cout << sequence.length() << endl;
                all_quality_content=true;
            }
        }
        // line_count++;
    }

    // Afficher le Phred quality score moyen de la dernière séquence du fichier fastq
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

    return 0;
}
