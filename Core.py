__author__ = 'mikeknowles'
""" This is the core script, its mission:
Retrieve genomes
This will require the user to download rMLST data
To sort rMLST results and remove closely related sequences
then to prepare the data for strain-specific probe idenification
"""
from argparse import ArgumentParser
from Bio import SeqIO
from textwrap import fill
from collections import defaultdict
import os, glob, GeneSeekr, shutil, json, time

def retriever(genomes, output):
    if not os.path.exists(output + "Genomes"):
        os.mkdir(output + "Genomes")
    for folders in glob.glob(genomes + "/*"):
        if os.path.exists(folders + "/Best_Assemblies"):
            for fasta in glob.glob(folders + "/Best_Assemblies/*"):
                shutil.copy(fasta, output + "Genomes")

def jsonUpGoer(jsonfile, markers, genomes, outdir):
    if os.path.isfile(jsonfile):
        genedict = json.load(open(jsonfile))
    else:
        genedict = GeneSeekr.blaster(markers, genomes, outdir, "USSpip")
        json.dump(genedict, open(jsonfile, 'w'), sort_keys=True, indent=4, separators=(',', ': '))
    return genedict

def compareType(TargetrMLST, nonTargetrMLST):
    typing = defaultdict(int)
    for genome in TargetrMLST:
        for gene in sorted(TargetrMLST[genome]):
            for nontarget in nonTargetrMLST:
                if nontarget not in typing:  # if nontarget genome not in typing dictionary then add it
                    typing[nontarget] = 0



def sorter(markers, genomes, outdir, target):
    '''Strip first allele off each locus to feed into geneseekr and return dictionary
    '''
    smallMLST = outdir + "rMLST/"
    if not os.path.exists(outdir + "Genomes/"):
        retriever(genomes, outdir)
    if not os.path.exists(outdir + "tmp/"):
        os.mkdir(outdir + "tmp/")
    genomes = outdir + "Genomes/"
    start = time.time()
    jsonfile = '%sgenedict.json' %  markers
    nonTargetrMLST = jsonUpGoer(jsonfile, markers, genomes, outdir)
    end = start - time.time()
    print "Elapsed time for rMLST is %ss with %ss per genome" % (end, end/len(genomes))
    if os.path.isdir(target):  # Determine if target is a folder
        targets = glob.glob(target + "*")
        targetjson = '%sgenedict.json' % target
    elif os.path.isfile(target):
        targets = target
        targetjson = '%sgenedict.json' % outdir
    else:
        print "The variable \"--targets\" is not a folder or file "
        return
    targetrMLST = jsonUpGoer(targetjson, targets, genomes, outdir)
    nTtyp = defaultdict(dict)
    Ttyp = defaultdict(dict)
    for genome in nonTargetrMLST:
        for gene in nonTargetrMLST[genome]:








#Parser for arguments
parser = ArgumentParser(description='Find Universal Strain-Specifc Probes')
parser.add_argument('--version', action='version', version='%(prog)s v0.5')
parser.add_argument('-o', '--output', required=True, help='Specify output directory')
parser.add_argument('-i', '--input', required=True, help='Specify input genome fasta folder')
parser.add_argument('-m', '--marker', required=True, help='Specify rMLST folder')
parser.add_argument('-t', '--target', required=True, help='Specify target genome or folder')
args = vars(parser.parse_args())

sorter(args['marker'], args['input'], args['output'])