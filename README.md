# The Edwards' lab CAMI submission

##2015 first CAMI challenge

The [CAMI (Critical Assessment of Metagenomic Interpretation)](http://www.cami-challenge.org/) challenge started in 2014, with data submission in July 2015. In the intital round there are three challenges, [assembly](https://github.com/CAMI-challenge/contest_information/blob/master/file_formats/CAMI_A_specification.mkd), [binning](https://github.com/CAMI-challenge/contest_information/blob/master/file_formats/CAMI_B_specification.mkd), and [profiling](https://github.com/CAMI-challenge/contest_information/blob/master/file_formats/CAMI_TP_specification.mkd).

We don't have an assembler, but we have tools for [binning](http://edwards.sdsu.edu/crAss/) and [profiling](http://edwards.sdsu.edu/FOCUS/). After some discsussion we decided to enter the profiling tool to start with, and if time allowed (it didn't) we'd enter the binning tools.

Next time, we hope there is a challenge for [functional annotation](http://edwards.sdsu.edu/rtmg/) as we have some new ideas on that!

Our approach was to enter FOCUS, but adapt it to the [databases](https://data.cami-challenge.org/) that CAMI provided. In the end, there are two different data sets: complete bacteria from RefSeq and a combination of complete and draft bacteria. (There is some redundancy between the two data sets.) This allows us to test something we've been pondering for a while: how does the presence of draft genomes affect our predictions of the species present in the sample.

The standard [focus](http://edwards.sdsu.edu/FOCUS/) that you can download has three *k*-mer data sets that we provide: 7-mers, 8-mers, and 9-mers. We decided that the CAMI challenge would also allow us to test the effect of different size *k*-mers on the predictions. We have some preliminary evidence that 7- and 8-mers are better than 9-mers, and since time was short (we procrastinated too much), we decided to focus on those two.

Our general approach was to use focus, but to adapt the output from the normal output where we list everything to a revised output where we only include the taxonomy ID and the percent abundance of the sample. We then wrote a post-procesisng script that allowed us to take that output and add the taxonomic information as required by the CAMI challenge. This is the essence of computer science: take a large problem and break it down into smaller pieces, solve those pieces, and put it all together. 

Our pipeline started out as the following steps:

1. Uncompress the fastq file and convert it to fasta format
2. Run the modified [focus_cami.py](gueiros/focus_cami.py) to predict the organisms present in this data
3. Run a post-processing script [focus2results.py](redwards/python/focus2result.py) to convert the output into CAMI format.

Initially we built [docker](https://hub.docker.com/u/linsalrob/) implementations of our pipeline. There were a couple of things that were slow, in particular the fastq to fasta converter was pretty slow, so we [rewrote that in C++](redwards/cpp/fastq2fasta.cpp) (note: if you use this, it ignores the quality scores!), and tested the timing. The C++ code is ~50x faster than equivilent PERL code, however it was very slow if we use a UNIX pipe to pipe the input rather than just using a file. Our current approach is therefore to uncompress the file and then convert it to fasta.

Our [docker](https://hub.docker.com/u/linsalrob/) implementations work as described, and are easy to get going. You only need two directories, an input and output directory. Put the compressed fastq file(s) in the input directory, and create a file that lists all of those fastq files, one per line. I call that `fastq.list` (though if you use a different name, change it here).

You can implement the docker code like this:

```
docker run \
-v "$PWD/input:/dckr/mnt/input:ro" \
-v "$PWD/output:/dckr/mnt/output:rw" \
-e "DCKR_THREADS=16" \
-e "CONT_FASTQ_FILE_LISTING=/dckr/mnt/input/fastq.list" \
-e "CONT_PAIRED_FASTQ_FILE_LISTING=/dckr/mnt/input/paired_fastq.list" \
-e "CONT_PROFILING_FILE=/dckr/mnt/output/results.out" \
--rm \
linsalrob/cfk7b \
default
```

This will run the 7-mer complete bacterial data set against your fastq file(s) listed in `fastq.list` (note: it is expected that they are compressed with gzip).


We [downloaded](https://data.cami-challenge.org/) the three CAMI test data sets (low, medium, and high complexity), and wanted to run these using our pipeline. However, time was against us. We had two strikes against us, first, we procrastinated too long. We don't often procrastinate and I'd tell you why, but that's a story for another day. Second, we didn't really read all the instructions and/or didn't understand them. Thinking that the dockers would suffice, we put all our energy into making robust fast dockers rather than actually analyzing the data. Oops. So we decided to analyze the data using our cluster (thanks NSF grant [CNS-1305112](http://www.nsf.gov/awardsearch/showAward?AWD_ID=1305112)). Here's how to quickly annotate 100+ GB of metagenome data in a few minutes, eight times, and generate fingerprints. Yeah, that's how quickly we can do this!

1. Uncompress the data. 

Since we are going to analyze the data multiple times, we only need to uncompress it and convert it to fasta format once. Start with the uncompressing: [parallel gzip](http://zlib.net/pigz/) is your friend.  This will uncompress a bunch of files (warning, do this on a machine with a reasonable number of cores and decent IO).

```
 for i in *; do pigz -d $i & echo $i; done
```

2. Convert to fasta

This uses our [C++](redwards/cpp/fastq2fasta.cpp) code, but you can do it with PERL, SeqTK, or anyhow you want

```
for i in *.fq;
do
	o=$(echo $i | sed -e 's/.fq/.fa/');
	edwardslab_CAMI/redwards/cpp/fastq2fasta $i $o & echo $i;
done
```


3. Analyze using [focus](gueiros/focus_cami.py) and [focus2result.py](redwards/python/focus2result.py)

For this we use the cluster, and so we wrote a [submission script](redwards/bash/cami.sh).

This code reads a file to figure out which type of focus it should run (based on a parameter passed to it), and then calls the appropriate command line. The command lines are of the variety:

```
python2.7 /home3/redwards/Cami_Challenge/FOCUS_CAMI/focus_cami.py -q $IDIR/CAMI.fa -m 0.001 -c b -k 7  > $ODIR/$FOCUS_TYPE.focus
```

Where `$INDIR` is the file that contains the fasta input file (CAMI.fa), and `$ODIR` is the output directory to write the results. We then make a file with the suffix focus which is just tab separated text containing [taxid, percent].

4. Finally, we convert that focus file to an output file that we can submit to CAMI:

```
python2.7 /home3/redwards/Cami_Challenge/edwardslab_CAMI/redwards/python/focus2result.py $ODIR/$FOCUS_TYPE.focus $FOCUS_TYPE $DATASET > $ODIR/$FOCUS_TYPE.out
```

Straightforward, eh? For the high complexity data set this takes about 15 minutes (OK, I am estimating since I didn't time it).


#RESULTS

We generate the fingerprint for the results file and upload that to the CAMI site as described on their website.

[All of our results are also posted online](results/)


