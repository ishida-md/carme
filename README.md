# carme
lightweight kallisto RNA-seq pipeline

This small Python3 script is designed to run FastQC and kallisto analysis on many samples. The output can be readily analyzed by sleuth.

## Prerequisite

Written in Python3. Tested solely on macOS. It should run on any POSIX systems in principle.
You need to have kallisto, FastQC in your PATH.

## Usage

```carme.py [-h] [--single] [-t T] [-l FRAG_LEN] [-s FRAG_SD]  kallisto_index_path  csv_path  outdir```

run ```carme.py -h``` for more options.
