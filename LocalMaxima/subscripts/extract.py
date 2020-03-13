import argparse
import sys
import LocalMaxima.structure.structure3D as strct

def register_parser(subparsers):
    parser = subparsers.add_parser('extract', usage=usage(), 
                                   description=description())
    add_arguments(parser)

def add_arguments(parser):
    parser.add_argument("--structure", metavar="FILE", help="Input File.", 
                        required=True)
    parser.add_argument("--expression", type=str,help="""A Structural expresion that 
                        must be a subset of --structure. If the structural 
                        expression includes elements not found in the --structure, 
                        the program will not run. The structural expression 
                        must be in \" quotation marks.""", required=True)
    parser.add_argument("--output", metavar="FILE", type=str, default="OUT_2_TERMINAL",
                        help="""Path filename for output structure file in PDB format. If
                        no --output is provided, structure will be output to the
                        standard output in the shell prompt.""",required=False)
    parser.set_defaults(func=run)

def run(options):
    structure = strct.structure(options.structure)
    if (structure.file_sufix.lower() == 'pdb') or (structure.file_sufix.lower() == 'cif'):
        structure.get_se_output(options.expression, options.output)
    else:
        print("ERROR: Unrecognized structure file format.")
        print("       Program will exit without results.")
        sys.exit(1)
def description():
    return """It extracts models or chain groups in the structure into separate 
           PDB files. The --models and --chains flags will not run if both are 
           present in the command line; separate by models and the run the 
           hrscript again to separate a model into chains."""

def usage():
    return '\npdb_cif.py extract --input 1BRS.pdb --se c[A,D]\n' \
           'pdb_cif.py extract --input 1BRS.pdb --se c[A,D] --out 1BRS_1_AD.pdb'

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description=description())
    add_arguments(arg_parser)
    args = arg_parser.parse_args()
    args.func(args)
