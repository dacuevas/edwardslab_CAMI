#!/bin/bash

#######################################################################
#                                                                     #
#          FOCUS main.sh                                              #
#                                                                     #
#######################################################################

#
# A wrapper around focus for the CAMI challenge. 
# This wrapper takes the input files listed in the environment variables
# and runs FOCUS on each file.
# 
# There are three possible input files you can choose. Each has a 
# list of files that you must process, one per line.
#
# - a read-based profiler would take CONT_FASTQ_FILE_LISTING as input
# - a read-based profiler aware of paired-end reads would take CONT_PAIRED_FASTQ_FILE_LISTING as input
# - a config-based profiler would read CONT_CONTIGS_FILE_LISTING
# 
# The output must be provided in $CONT_PROFILING_FILE

# should we change IFS to make sure there are no spaces in the filename.  I doubt that they will be that dastardly!


FOCUS_TYPE="cfk7b"


echo "Cleaning up"
rm -rf /tmp/fasta /tmp/fastq /tmp/DNA.fasta /tmp/focus.out

# work in the /tmp directory as this is deleted at the end
cd /tmp
mkdir -p fasta fastq

# process each file in the fastq listing
echo "Extracting all fastq files"

for FILE in $(sed '/^$/d' $CONT_FASTQ_FILE_LISTING);
do 
	# convert the fastq file to fasta 
	FID=$RANDOM
	gunzip -c $FILE > fastq/$FID.fastq
	/home/fastq2fasta /tmp/fastq/$FID.fastq /tmp/fasta/$FID.fasta
done

echo "Concatenating all fasta files into a single file"
cat /tmp/fasta/*.fasta > /tmp/DNA.fasta
	
echo "Profiling"
python /home/focus_cami.py -q DNA.fasta -m 0.001 -c b -k 7  > /tmp/focus.out

echo "Generating CAMI report"
python2.7 /home/focus2result.py /tmp/focus.out $FOCUS_TYPE $CONT_FASTQ_FILE_LISTING  > $CONT_PROFILING_FILE


