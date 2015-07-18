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
# - a read-based profiler would take CONT_FASTQ_FILE_LISTING as input. In this file, we're using DATASET for this variable
# - a read-based profiler aware of paired-end reads would take CONT_PAIRED_FASTQ_FILE_LISTING as input
# - a config-based profiler would read CONT_CONTIGS_FILE_LISTING
# 
# The output must be provided in $CONT_PROFILING_FILE

# should we change IFS to make sure there are no spaces in the filename.  I doubt that they will be that dastardly!



# focuses is a text file with one focus run per line. i.e. it has these 6 lines:
# cfk7b
# cfk7d
# cfk7bd
# cfk8b
# cfk8d
# cfk8bd


FOCUS_TYPE=$(head -n $SGE_TASK_ID focuses | tail -n 1)
echo "Running $FOCUS_TYPE"

IDIR="/home3/redwards/Cami_Challenge/input_data/cami_low/input"
ODIR="/home3/redwards/Cami_Challenge/input_data/cami_low/output"
export DATASET="CAMI-LOW"

export PATH=$PATH:/usr/local/jellyfish/bin/

# just move to scratch space to write the temporary files for Jellyfish
cd /scratch/redwards/
echo "Profiling"
export PYTHONPATH=:/usr/local/opencv/lib/python2.6/site-packages/:/home3/redwards/bioinformatics/Modules/:/usr/local/opencv/lib/python2.6/site-packages/:/home3/redwards/bioinformatics/Modules/:/home3/redwards/Cami_Challenge/edwardslab_CAMI/redwards/python

case "$FOCUS_TYPE" in 
	cfk7b)
		echo "cfk7b : -c b -k 7"
		python2.7 /home3/redwards/Cami_Challenge/FOCUS_CAMI/focus_cami.py -q $IDIR/CAMI.fa -m 0.001 -c b -k 7  > $ODIR/$FOCUS_TYPE.focus
		;;
	cfk7d)
		echo "cfk7d : -c d -k 7"
		python2.7 /home3/redwards/Cami_Challenge/FOCUS_CAMI/focus_cami.py -q $IDIR/CAMI.fa -m 0.001 -c d -k 7  > $ODIR/$FOCUS_TYPE.focus
		;;
	cfk7bd)
		echo "cfk7bd : -c bd -k 7"
		python2.7 /home3/redwards/Cami_Challenge/FOCUS_CAMI/focus_cami.py -q $IDIR/CAMI.fa -m 0.001 -c bd -k 7  > $ODIR/$FOCUS_TYPE.focus
		;;
	cfk8b)
		echo "cfk8b : -c b -k 8"
		python2.7 /home3/redwards/Cami_Challenge/FOCUS_CAMI/focus_cami.py -q $IDIR/CAMI.fa -m 0.001 -c b -k 8  > $ODIR/$FOCUS_TYPE.focus
		;;
	cfk8d)
		echo "cfk8d : -c d -k 8"
		python2.7 /home3/redwards/Cami_Challenge/FOCUS_CAMI/focus_cami.py -q $IDIR/CAMI.fa -m 0.001 -c d -k 8  > $ODIR/$FOCUS_TYPE.focus
		;;
	cfk8bd)
		echo "cfk8bd : -c bd -k 8"
		python2.7 /home3/redwards/Cami_Challenge/FOCUS_CAMI/focus_cami.py -q $IDIR/CAMI.fa -m 0.001 -c bd -k 8  > $ODIR/$FOCUS_TYPE.focus
		;;
	*)
		echo "DONT UNDERSTAND: $FOCUS_TYPE"
		exit 5
		;;
	esac


echo "Generating CAMI report"
python2.7 /home3/redwards/Cami_Challenge/edwardslab_CAMI/redwards/python/focus2result.py $ODIR/$FOCUS_TYPE.focus $FOCUS_TYPE $DATASET > $ODIR/$FOCUS_TYPE.out


