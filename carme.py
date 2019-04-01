#!/usr/bin/env python3

pipe_ver = "0.0.1"

import csv
import argparse
from argparse import RawTextHelpFormatter
import subprocess
import os
from datetime import datetime

def parse_args():
    parser = argparse.ArgumentParser(description =
    '''carme -lightweight kallisto pipeline-
    Prerequisite: Python3, FastQC, kallisto in $PATH.
    You need a csv file with the header containing "sample", "r1", "r2". 
    You can easily generate CSVs by executing the following command and editing
    the resulting text on Excel. 
    > find $PWD -name "*.fastq"  -type f > targets.txt''',
    formatter_class=RawTextHelpFormatter)
    parser.add_argument('kallisto_index_path', help = 'absolute path to kallisto index file')
    parser.add_argument('csv_path', help = 'absolute path to csv file')
    parser.add_argument('outdir', help = 'absolute path to output dir')
    parser.add_argument('--single', help = 'required if your fastq is single endded', action = 'store_true')
    parser.add_argument('-t', help = 'number of parallel threads (default: 4)', type = int, default = 4)
    parser.add_argument('-l', '--fragment-length', dest = 'frag_len', type = int, default = 200)
    parser.add_argument('-s', '--sd', type = int, dest = 'frag_sd', default = 30)
    args = parser.parse_args()
    
    return (args.kallisto_index_path, args.csv_path, args.outdir,
            args.single, str(args.t), str(args.frag_len), str(args.frag_sd))

def capture_bash(cmd):
    b = subprocess.check_output(cmd)
    x = b.decode('utf-8')
    return(x)

def write_log(outdir):
    log_file = open(outdir + "/pipeline_report_" + datetime.now().strftime('%Y-%m-%d %H.%M.%S') + ".log", 'w')
    print(outdir)
    
    fastqc = capture_bash(['fastqc', '-v'])
    kallisto = capture_bash(['kallisto', 'version'])
    
    log_file.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
    log_file.write("carme lightweight kallisto pipeline version " + pipe_ver + "\n")
    log_file.write(fastqc)
    log_file.write(kallisto)
    log_file.close()

def is_bom(filename):
    first_line = open(filename, encoding = 'utf-8').readline()
    return(first_line[0] == '\ufeff')

def run_kallisto_single(kallisto_idx, read1, sample_dir, n_thread, frag_len, frag_sd):
    kallisto_command = ["kallisto", "quant", "--single", "-l", frag_len, "-s",  frag_sd,
                        "-t", n_thread, "-b", "100", "-i", kallisto_idx, "-o", sample_dir, read1]
    subprocess.run(kallisto_command)

def run_kallisto_double(kallisto_idx, read1, read2, sample_dir, n_thread):
    kallisto_command = ["kallisto", "quant", "-t", n_thread, "-b", "100", "-i", kallisto_idx, "-o", sample_dir, read1, read2]
    subprocess.run(kallisto_command)

def main():
    kallisto_idx, csv_path, outdir, is_single, n_thread, frag_len, frag_sd = parse_args()
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": kallisto pipeline: starting the run")
    write_log(outdir)
    
    if not os.path.isdir(outdir): os.mkdir(outdir) # check output directory

    encoding = 'utf-8-sig' if is_bom(csv_path) else None # take care of Excel CSV with BOM
    csvfile =  open(csv_path, "r", encoding = encoding)

    f = csv.DictReader(csvfile, delimiter = ',')
    for row in f:
        sample_name = row['sample']
        sample_dir = outdir + "/" + sample_name
        if not os.path.isdir(sample_dir): os.mkdir(sample_dir)
        read1 = row['r1']
        read2 = None if is_single else row['r2']
        
        print("Performing QC: " + sample_name)
        fastqc_command = ["fastqc", read1, "-o", sample_dir]
        subprocess.run(fastqc_command)

        print("Performing kallisto analysis: " + sample_name)
        if is_single:
            run_kallisto_single(kallisto_idx, read1, sample_dir, n_thread, frag_len, frag_sd)
        else:
            run_kallisto_double(kallisto_idx, read1, read2, sample_dir, n_thread)
    csvfile.close()
    
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": kallisto pipeline: run ended")

if __name__ == "__main__":
    main()