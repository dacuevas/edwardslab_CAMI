#Python code for the CAMI challenge


- focus2result.py

This code converts the two column focus output into an appropriately formated output file for the CAMI challenge. There are three parameters required, the focus output file, the version of the tool being used, and the input file name.

To run it use:

```
python2.7 /home/focus2result.py /tmp/focus.out $FOCUS_TYPE $CONT_FASTQ_FILE_LISTING  > $CONT_PROFILING_FILE
```



- check_taxonomy.py

This code just checks our output to see that we are valid. To run it use:

```
python check_taxonomy.py ../../../output/results.out
```

- cami_pickle.py

This pickles the data from dcuevas and provides a mechanism to load it back in

```
python2.7 cami_pickle.py dcuevas/taxonomy_out/rank.txt dcuevas/taxonomy_out/taxonomy2_no_doubles.txt
```

Note: make sure you specify the location of the pickle in your call in focus2result.py
