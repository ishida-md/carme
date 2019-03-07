# carme
very lightweight kallisto RNA-seq pipeline

This short Python3 script is designed to run FastQC and kallisto analysis on many samples.

## Prerequisite

Written in Python3. Tested solely on macOS. In principle, it should run on any POSIX systems.
You need to have kallisto, FastQC in your PATH.

## Usage

carme.py [-h] [--single] [-t T] [-l FRAG_LEN] [-s FRAG_SD] kallisto_index_path csv_path outdir

run ```carme.py -h``` for more options.
