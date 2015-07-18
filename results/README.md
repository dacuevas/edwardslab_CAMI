#Results for the FOCUS predictions

We have run focus with a couple of different parameters, and so we generated eight different output files. Here are the output files and their fingerprints from camiClient.jar

To generate these fingerprints we run with this code:

```
for i in output_files/cami_low/*;
do
	fp=$(echo $i | sed -e 's/\.out/.fp/');
	echo "$i -> $fp";
	java -jar camiClient.jar -pf $i taxdb/ | grep -v ^read > $fp;
done
```

We ignore any line beginning with read because the camiClient prints every line it processes to stdout (should have been to stderr). This allows us to grab just the fingerprint for those files.


## 1st CAMI Challenge Dataset 1 CAMI_low

---|---|---|---|
Results file | *k*-mer size | database | fingerprint |
---|---|---|---|
[cfk7b](cami_low/cfk7b.out)  | 7 | bacteria genomes | 6A53F8DF380EC16261216B6B9187BF29141 |
[cfk7d](cami_low/cfk7d.out)  | 7 | draft genomes | 9CC2A4F7773E3F90A743B0E1970188B3141 |
[cfk7bd](cami_low/cfk7bd.out) | 7 | bacteria and draft genomes | C6FE24C88B746306270653C1A522845D141 |
[cfk8b](cami_low/cfk8b.out)  | 8 | bacteria genomes | 8A7F34A2DE6E1AB1895F2C1D7E4E48C6141 |
[cfk8d](cami_low/cfk8d.out)  | 8 | draft genomes | 27B9414DAC1BBA25F18AF7C31650D3F0141 |
[cfk8bd](cami_low/cfk8bd.out) | 8 | bacteria and draft genomes | 82AF2F94221D56DFF1CBE2FE0321FFF1141 |


## 1st CAMI Challenge Dataset 2 CAMI_medium

---|---|---|---|
Results file | *k*-mer size | database | fingerprint |
---|---|---|---|
[cfk7b](cami_mid/cfk7b.out)  | 7 | bacteria genomes | 
[cfk7d](cami_mid/cfk7d.out)  | 7 | draft genomes | 
[cfk7bd](cami_mid/cfk7bd.out) | 7 | bacteria and draft genomes | 
[cfk8b](cami_mid/cfk8b.out)  | 8 | bacteria genomes | 47214307251FBF5B673E11D5D2CECB48141
[cfk8d](cami_mid/cfk8d.out)  | 8 | draft genomes | 06F903274E774941DCF50BAD469232D7141
[cfk8bd](cami_mid/cfk8bd.out) | 8 | bacteria and draft genomes | 4E2F00871FA9895D9B8539D05FAF8795141


## 1st CAMI Challenge Dataset 3 CAMI_high


---|---|---|---|
Results file | *k*-mer size | database | fingerprint |
---|---|---|---|
[cfk7b](cami_high/cfk7b.out)  | 7 | bacteria genomes | 
[cfk7d](cami_high/cfk7d.out)  | 7 | draft genomes | 
[cfk7bd](cami_high/cfk7bd.out) | 7 | bacteria and draft genomes | 
[cfk8b](cami_high/cfk8b.out)  | 8 | bacteria genomes | 75EFB1F8FB3EE13BF4DC5E8F47458E1C141
[cfk8d](cami_high/cfk8d.out)  | 8 | draft genomes | E89C02471D36FB399E814645C0B86894141
[cfk8bd](cami_high/cfk8bd.out) | 8 | bacteria and draft genomes | 2064FEEB59AAFFC379D6D2C6DFB08640141






