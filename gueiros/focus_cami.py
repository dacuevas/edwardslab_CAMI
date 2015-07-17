# FOCUS version CAMI
from numpy import array,linspace,zeros,eye,concatenate,sum as SUM,linalg
from scipy.optimize import nnls
import os,sys,random

##############################
#  Program Defaults parameters#
##############################
parameters={"-k":"7","-q":"","-d":"","dir":"","-c":"b"}
# [-q] metagenome sequence files in FASTA format
# [-k] k-mer choice
# [-d] data to insert into the Database
# [-c] cami database [b for complete bacterial; d for drafts; bd for both]

usage="FOCUS: An Alignment-Free Model To Identify Organisms In Metagenomes Using Non-Negative Least Squares\n\nUSAGE\n\npython focus.py -q query_sequence.fna [-k] [-c]\n   -q Specify input file.\n      Required: Input files should be in FASTA format\n   -k Specify k-mer frequency used on the profile (default: 7)\n       7 and 8 frequencies are available.\n      All the output files have this project name as prefix.\n   -m [-c] cami database [b for complete bacterial; d for drafts; bd for both]\n      more information README"


#######################################################
#Read and save the parameters given by the user       #
#######################################################
def setParameters():
    if "/" in sys.argv[0]:
        parameters["dir"]="/".join(sys.argv[0].split("/")[:-1])+"/"
    userParameters=sys.argv[1:]
    for i in range(0,len(userParameters),2):
        try:
            parameters[userParameters[i]]=userParameters[i+1]
        except:
            if userParameters[i] in parameters:
                print "Please inform a value for "+userParameters[i]
            else:
                print userParameters[i]+" is not a valid parameter"
                
                    
setParameters()#store user parameters

if parameters["-c"]=="b":
    parameters["-c"]="_bacterial"
elif parameters["-c"]=="d":
    parameters["-c"]="_draft"
elif parameters["-c"]=="bd":
    parameters["-c"]="_bacterial_and_draft"



#returns the path for a given program name
def which(program):
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

#jellyfish version
jf=os.popen("jellyfish count --version").read().split(".")[0]

if "-h" in sys.argv[1:]:
    print usage

elif len(jf)==0:
    print "Jellyfish not installed. Please download it at http://www.cbcb.umd.edu/software/jellyfish"    
    
#check if the query exists or if it is adding genome to the db
elif os.path.isfile(parameters["-q"])!=True:
    print "Please use -q and select a valid query!"

#check if jellyfish is installed
elif which("jellyfish")==None:
    print "Jellyfish is not installed!!!\nhttp://www.cbcb.umd.edu/software/jellyfish/"

else:
    try:
        #Stores the tabular file
        tabular=[]
        ######################################################
        #Normalises the k-mer usage by the total length      #
        ######################################################
        def normalise(result):
            return result/(SUM(result)*1.)

        #######################################################
        #Run jellyfish and counts the k-mer for the user input#
        #######################################################
        def kmer():
            random.seed()#random seed in case someone runs it on a cluster
            randomID=str(int(random.random()*100000))
            
            #runs jellyfish to count the k-mer for the input data
            if jf=="1":
                os.system("jellyfish count -m "+parameters["-k"]+" -o "+randomID+"_kmer_counting -s 100000 -t 32 -C "+parameters["-q"])
                merge=int(os.popen("ls | grep "+randomID+"_kmer_counting_ | wc -l").read())
                #checks if we need to merge the files or not
                if merge>1:
                    os.system("jellyfish merge "+randomID+"_kmer_counting* -o kmer_counting")
                    os.system("jellyfish dump "+randomID+"_kmer_counting -c > "+randomID+"_query")
                else:
                    os.system("jellyfish dump "+randomID+"_kmer_counting_0 -c > "+randomID+"_query")
            else:
                os.system("jellyfish count -m "+parameters["-k"]+" -o "+randomID+"_kmer_counting -s 100M -t 32 -C --disk "+parameters["-q"])
                os.system("jellyfish dump "+randomID+"_kmer_counting -c > "+randomID+"_query")

            #loads the mers that we need in the order that we need
            ##########################################################
            referenceDB={}
            usage=file(parameters["dir"]+"db/k"+parameters["-k"]+parameters["-c"]).readline().replace("\r\n","");usage=usage.split("\t")[8:]
            ##########################################################
            #Stores the mers counted by jellyfish
            mer={}
            k=open(randomID+"_query")
            for line in k:
                line=line.split()
                mer[line[0]]=int(line[1])
            k.close()
            os.system("rm "+randomID+"_query "+randomID+"_kmer_counting*")#delete jellyfish's output
            metagenomeUsage=[]
            #Read the query input mers in the order that we need
            for i in usage:
                if i in mer:
                    metagenomeUsage.append(int(mer[i]))
                else:
                    metagenomeUsage.append(0)  
            data=normalise(metagenomeUsage)#normalise the input usage
            
            return data
        #######################################################
        #Loads the Database selected by the user              #
        #######################################################
        def loadDB():


            
            db=open(parameters["dir"]+"db/k"+parameters["-k"]+parameters["-c"])
            db.readline()
            h={}
            for line in db:
                line=line.split("\t")
                h["\t".join(line[:8])]=normalise(array(line[8:], dtype='i'))#array([int(x) for x in line[8:]])
            db.close()
            
            organisms=h.keys()
            h=array(h.values())
            return h.T,organisms
        ##############################################################
        # Get the results, prints to the user and plot on the figures#
        ##############################################################
        def GetResults(level,organisms,weights):
            results={}
            #add in the hash the values related to the parameter 'level'
            for i in range(len(organisms)):
                tax=organisms[i].split("\t")[level]
                if tax not in results:
                    results[tax]=weights[i]
                else:
                    results[tax]+=weights[i]
            #creates and sorts a list of tuples with (ID,abundance)
            results=[(float(results[i])*100,i) for i in results]
            results.sort(reverse=True)
            if level==0:
                level="TaxonID"

            #prints the results in a readable format
            tabular.append(level+"\nRank\tPredicted Organism\tEstimated Abundance (%)\n")            

            c=1
            labels=[];fracs=[]
            for i in results:
                if i[0]>0:
                    print i[1],"\t",i[0]
                    tabular.append(str(c)+"\t"+str(i[1])+"\t"+str(i[0])+"\n")
                    c+=1
                    labels.append(i[1])
                    fracs.append(round(i[0],2))
            return [labels,fracs,level]
            
        #######################################################
        #Starts to run FOCUS
        #######################################################
        def main():
            if parameters["-k"] not in ["7","8"]:
                print usage
                print "Problem(s):"
                print "-"*50
                print "-k parameter has to be 7, or 8"
                print "-"*50
                
            else:
                data=kmer()

                db,organisms=loadDB()

                #find the best set of organisms that reconstruct the user metagenome using NNLS
                weights=normalise(nnls(db,data)[0])

                c=6
                for i in [0]:
                    labels,fracs,level=GetResults(i,organisms,weights)

                    c+=1

                #Writes tabular output!
                o=open(parameters["-q"]+"__output.txt","w+")
                o.write("Query: "+parameters["-q"]+"\n")
                o.write("K-mer size: "+parameters["-k"]+"\n\n")
                for result in tabular:
                    o.write(result)
                o.close()
                    
        main() 
    except:
        print usage
