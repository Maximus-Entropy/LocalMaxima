import argparse
import sys
import LocalMaxima.structure.structure3D as strct

def register_parser(subparsers):
    parser = subparsers.add_parser('gaps', usage=usage(), description=description())
    add_arguments(parser)

def add_arguments(parser):
    parser.add_argument("--structure", metavar="FILE", help="PDB or CIF Structure File.", required=True)
    parser.add_argument("--sequence", default='\0', metavar="FILE", help="Sequence FASTA File. This file is considered only when a PDB structure file is used.", required=False)
    parser.add_argument('--num', type=int, action="store", default=60, help="This option takes an integer value for the width of the alignment displays. Default is 60.")
    parser.set_defaults(func=run)

def run(options):
    structure = strct.structure(options.structure)
    if (structure.file_sufix.lower() == 'pdb') or (structure.file_sufix.lower() == 'cif'):
        if options.sequence != '\0':
            print("Number of columns:"+str(options.num))
            structure.sequence_path = options.sequence
            structure.add_sequence('fasta')
        structure.gap_report(options.num)
    else:
        print("ERROR: Unrecognized structure file format.")
        print("       Program will exit without results.")
        sys.exit(1)

def description():
    return """This command detects gaps in the crystal structure of a protein. 
    The search requires at least a structure PDB or CIF file. When only a CIF 
    or PDB file is provided, gaps are checked by tracking monotonically increa-
    sing residue numbers from 1 to the last residue in the structure; this 
    search has the potential to not report missing residues in the C-terminal 
    of the structure as gaps because the last amino acid in the structure is 
    assumed to be the last one in the sequence, which is not always the case.
                                                             
    Gaps in crystalographic structures can be detected with certainty when a 
    FASTA file is provided in the arguments, then an alignment is done between 
    the amino acid sequence from those present in the structure with the ones 
    in the FASTA file. 

    NOTE: Sequence information is found in headers of CIF and PDB files. The 
    PDB's header information is not considered reliable and the user will have 
    to enter a Fasta sequence file to reliably find gaps in the structure. A 
    CIF sequence information found in the header is considered more reliable, 
    but Biopython still fails to recognized subtle features that are different 
    between two crystal structures's headers and cause problems. Yet, providing
    sequence informatio in the form of a FASTA file by the user makes the 
    program more reliable, less confusing, and avoids bugs caused by CIF and 
    PDB formating inconsistencies. TODO: If there is a match between a fasta
    file number of entries and a structure, get chains of structure and align
    to thos in the fasta file with the same chain identifier.
    """

def usage():
    return '\nstrctr gaps --structure 1BRS.pdb --sequence 1BRS.fasta.txt'

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description=description())
    add_arguments(arg_parser)
    args = arg_parser.parse_args()
    args.func(args)
