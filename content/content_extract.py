import numpy as np

in_fastq = "t.cacoeciae_sup_230131.fastq"
out = "out.content"

in_fastq = open(in_fastq, "r")
out_file = open(out, "w")


tab_quality = np.power(10, (np.arange(0, 128 + 1) / -10))

all_quality_content = True
sequence = ""
quality = ""
line_count = 0

out_file.write("read_name	read_length	read_avg_quality")

for line in in_fastq:
    line = line.strip()

    if not line:
        continue

    if (line.startswith("@") and all_quality_content ):
        if sequence:
            avg_quality = np.sum( np.fromiter((tab_quality[ord(q) - 33] for q in quality), float) )
            avg_quality /= len(quality)

            out_file.write(f"{header}\t{len(sequence)}\t{-10*np.log10(avg_quality)}")

        header = line.split(" ", 1)[0][1:]
        line_count = 1
        all_quality_content = False
        sequence = ""
        quality = ""

    elif (line_count == 1):
        if (line == "+"):
            line_count = 3
            seq_len = len(sequence)
            continue
        sequence += line

    elif (line_count == 3):
        quality += line
        if len(quality) == seq_len:
            all_quality_content = True
        

if sequence:
    avg_quality = np.sum( np.fromiter((tab_quality[ord(q) - 33] for q in quality), float) )
    avg_quality /= len(quality)

    out_file.write(f"{header}\t{len(sequence)}\t{-10*np.log10(avg_quality)}")

in_fastq.close()
out_file.close()
