# Bi 624 (Fall 2019) – Deduper Part 1

## Define the problem
Here we want to build a tool to remove all the PCR duplicates. PCR duplicates satisfy a couple criteria. First, they have the same UMI. Second, they are at the same location of a specific chromosome strand. In addition, the algorithm should identify and adjust for soft clipping.

If present, the @HD record must be the first record and specifies the SAM version (tag VN) used in this file and the sort order (SO). The optional @SQ header records give the reference sequence names (tag SN) and lengths (tag LN). There also are other header record types.


## Pseudocode
Open file and read each line at a time
	if doesn't start with @:
		if forward:
			if check_UMI:
				read cigar string(line[5]) and adjust soft clipping
				check_alignment_position

		if reverse:
			if check_UMI:
				read cigar string and adjust for soft clipping
				check_alignment_postion


## Functions
def check_UMI(string):
	```input samfile column 1, return if UMI is one of the known UMIs```
	return True,False

start a dictionary with key: RNAME_POS_UMI
def check_alignment_position(string):
	``````
	if key exists:
		toss the read
	if key doesn't exist yet:
		update dictionary with new kew
		write to the output file
#
def adjust_soft_clipping():
	```add the amount of soft clipping"
	if forward:
		subtract first number of S to the POS
	if reverse:
		add all number to POS except I
if cigar string is 2S15M5I8D8N9M starting at pos 20 forward strand,
then adjust the starting position to 18
#
if cigar string is 2S15M5I8D8N9M starting at pos 20 reverse strand
then adjust the position to 20+2+15+8+8+9