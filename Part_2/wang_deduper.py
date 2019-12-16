#!/usr/bin/env python3
import re
import argparse


parser = argparse.ArgumentParser(description="Get rid of PCR duplicats")
parser.add_argument("-f", type=str, help="input file, absolute file path", required=True)
parser.add_argument("-p", help = "for paired end file",action='store_true')
parser.add_argument("-u", type=str, default = None, help = "filter out unknow umi")



args = parser.parse_args()

inputfile = args.f
umifile = args.u
f = open("output_file.sam", 'w')
# inputfile = '/projects/bgmp/shared/deduper/Dataset3.sam'

if args.u != None:
	with open(args.u) as file:
		UMIS = [line.strip() for line in file]
else:
	UMIS = []



def check_UMI(UMI):
    '''check if UMI in file is one of the known UMIs'''
    if UMI in UMIS:
        return True
    elif args.u == None:
    	return True
    return False


def check_not_duplicate(string):
    '''check duplicate in the same chromosome, return False for dup and True for new read'''
    if string not in dupdict:
        return True
    return False


def adjust_position(CIGAR, POS):
    '''if forward:subtract first number of S to the POS
    if reverse:add all number to POS except I + left S'''
    if (flag & 16) != 16:
    	strand='f'
        leftclip = re.compile(r'^\d+S').findall(CIGAR)
        if len(leftclip) > 0:
            POS = POS - int(leftclip[0][0])
    elif (flag & 16) == 16:
    	strand='r'
        num = 0
        seqlen = re.compile(r'\d+(?=[MDNP=X])').findall(CIGAR)
        for i in range(len(seqlen)):
            num += int(seqlen[i])
        POS = POS + num
        rightclip = re.compile(r'\d+S$').findall(CIGAR)
        if len(rightclip) > 0:
            POS = POS + int(rightclip[0][0])
    return POS,strand


rname = 0
dupdict = {}
n = 0
with open(inputfile) as fh:
    for line in fh:
        n += 1
        line = line.split('\t')
        if "@" == line[0][0]:
            f.write('\t'.join(line))
        else:
            umi = line[0].split(':')[-1]
            if check_UMI(umi):
                if rname != line[2]:
                    f.write('\t'.join(line))
                    dupdict = {}
                    rname = line[2]
                else:
                    pos = int(line[3])
                    rname = line[2]
                    cigar = line[5]
                    flag = int(line[1])
                    newpos,strand = adjust_position(cigar, pos)
                    if check_not_duplicate(str(newpos) + '_' + str(umi) +'_' +str(strand)):
                        dupdict.update({str(newpos) + '_' + str(umi)+ '_' +str(strand): 1})
                        f.write('\t'.join(line))
        if n % 100000 == 0:
            print(n)


f.close()
