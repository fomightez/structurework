#!/usr/bin/env python
# pdb_code_to_prot_prot_interactions_via_PDBsum.py
__author__ = "Wayne Decatur" #fomightez on GitHub
__license__ = "MIT"
__version__ = "0.1.0"


# pdb_code_to_prot_prot_interactions_via_PDBsum.py by Wayne Decatur
# ver 0.1
#
#*******************************************************************************
# Verified compatible with both Python 2.7 and Python 3.8; written initially in 
# Python 3. 
#
#
# PURPOSE: Takes a PDB code and returns a list of the interacting protein pairs 
# chain designation for that structure. The pairs are returned as a list of 
# tuples.
#
# This script is meant to be a utility script for working with PDBsum and 
# Python, see a demonstration of use in
# https://github.com/fomightez/pdbsum-binder
# It will be part of a larger set of tools meant to facilitate highlighting
# differences & similarities in protein-protein interactions of the same protein
# pairs in different, related complexes.
# 
#
#
# Written to run from command line or imported into/pasted/loaded inside a 
# Jupyter notebook cell. When doing in Jupyter (or IPython, I believe) you can 
# skip the file save intermediate, see https://git.io/Jtfon for these advanced 
# examples.
#
#
#
# 
#
#
#
#
#
#
# Dependencies beyond the mostly standard libraries/modules:
#
#
#
# VERSION HISTORY:
# v.0.1. basic working version

#
# To do:
# - make sure works with Python 2.7 <- sometimes I was lazy during development 
# used f-strings, & those need to be replaced with string formatting using 
# `.format()` because Python 2.7 never had f-strings, unless I add the use of 
# future_fstrings package, see https://stackoverflow.com/a/46182112/8508004
#
#
#
#
# TO RUN:
# Examples,
# Enter on the command line of your terminal, the line
#-----------------------------------
# python pdb_code_to_prot_prot_interactions_via_PDBsum.py PDB_CODE
#-----------------------------------
# Issue `pdb_code_to_prot_prot_interactions_via_PDBsum.py -h` for details.
# 
# More examples from running from the command line are at the links below: 
# https://git.io/Jtfon
#
#
#
# To use this after importing/pasting or loading into a cell in a Jupyter 
# notebook, specify at least the data file (or data as a string) in the 
# call to the main function similar to below:
# from pdb_code_to_prot_prot_interactions_via_PDBsum import pdb_code_to_prot_prot_interactions_via_PDBsum
# li = pdb_code_to_prot_prot_interactions_via_PDBsum("6kiv")
# li
#
#
# 
#
'''
CURRENT ACTUAL CODE FOR RUNNING/TESTING IN A NOTEBOOK WHEN IMPORTED/LOADED OR 
PASTED IN ANOTHER CELL:
df = pdb_code_to_prot_prot_interactions_via_PDBsum.("data.txt")
df
'''
#
# For testing, use these PDBsum data in addition to ones I was using at the time 
# because these cover more of a range of complexity:
#from 6KIZ Cryo-EM structure of human MLL1-NCP complex, binding mode2
#http://www.ebi.ac.uk/thornton-srv/databases/cgi-bin/pdbsum/GetIface.pl?pdb=6kiz&chain1=C&chain2=G
#http://www.ebi.ac.uk/thornton-srv/databases/cgi-bin/pdbsum/GetIface.pl?pdb=6kiz&chain1=B&chain2=N
#http://www.ebi.ac.uk/thornton-srv/databases/cgi-bin/pdbsum/GetIface.pl?pdb=6kiz&chain1=C&chain2=E
#http://www.ebi.ac.uk/thornton-srv/databases/cgi-bin/pdbsum/GetIface.pl?pdb=6kiz&chain1=A&chain2=B
#
#*******************************************************************************
#





#*******************************************************************************
##################################
#  USER ADJUSTABLE VALUES        #

##################################
#

## Settings and options for naming page_source to save 
output_file_name_prefix = "page_source" #at present this gets deleted & so I use
# datetime stamp to make unique so limited chance it deletes wrong thing

#
#*******************************************************************************
#**********************END USER ADJUSTABLE VARIABLES****************************













#*******************************************************************************
#*******************************************************************************
###DO NOT EDIT BELOW HERE - ENTER VALUES ABOVE###

import sys
import os
from sh import curl
import datetime
now = datetime.datetime.now()
output_file_name = "{}{}.htm".format(
    output_file_name_prefix,now.strftime('%b%d%Y%H%M'))


###---------------------------HELPER FUNCTIONS---------------------------------###

def get_n_save_protprot_page_source(pdb_code):
    '''
    Take a PDB code identifier and gets the Prot-prot page from PDBsum for that
    structure and saves the html as a text file. 

    Returns the file name of the text file produced.

    for example, 
    from 
    http://www.ebi.ac.uk/thornton-srv/databases/cgi-bin/pdbsum/GetPage.pl?pdbcode=6kiv&template=interfaces.html ,which is the 'Prot-prot' 
    page for 6kiv, it will get the source html and save it
    '''
    from sh import curl
    main_url = (
        "http://www.ebi.ac.uk/thornton-srv/databases/cgi-bin/pdbsum/GetPage.pl")
    curl("-L","-o","{}".format(output_file_name),
        "--data","pdbcode={}&template=interfaces.html".format(pdb_code),
        "{}".format(main_url))
    return output_file_name


###--------------------------END OF HELPER FUNCTIONS---------------------------###
###--------------------------END OF HELPER FUNCTIONS---------------------------###


#*******************************************************************************
###------------------------'main' function of script---------------------------##

#def get_interacting_protein_pairs(pdb_code):  <--called this in development
def pdb_code_to_prot_prot_interactions_via_PDBsum(pdb_code):
    '''
    Takes a PDB code and returns a list of the interacting protein pairs chain
    designation for that structure.
    The pairs are returned as a list of tuples.

    for example, 
    from 
    http://www.ebi.ac.uk/thornton-srv/databases/cgi-bin/pdbsum/GetPage.pl?pdbcode=6kiv&template=interfaces.html ,which is the 'Prot-prot' 
    page for 6kiv, it will return the full list of interacting pairs of proteins
    chain designations as a list of pairs.
    '''
    page_source_fn = get_n_save_protprot_page_source(pdb_code)
    with open(page_source_fn, 'r') as input_file:
        raw_txt=input_file.read()
    interface_summary_section = raw_txt.split(
        'Interface summary</a></B>')[1].split("<TD WIDTH=94% VALIGN=top>")[0]
    collected_lines = []
    for line in interface_summary_section.split("<B><a href"):
        if '.jpg"></a></B>' in line:
            collected_lines.append(line.split('.jpg"></a></B>')[0])
    # mine the tuples from `collected_lines`
    pair_tuples = [] # list of the tuples with the pair elements as members
    str_in_front_of_chainDesignation = (
        "/thornton-srv/databases/pdbsum/templates/gif/chain")
    for line in collected_lines:
        first_and_after = line.split(str_in_front_of_chainDesignation,1)[1]
        first_designation = first_and_after.split('.jpg">}{',1)[0]
        second_designation= first_and_after.split(
            str_in_front_of_chainDesignation,1)[1]
        pair_tuples.append((first_designation,second_designation))
    return pair_tuples
    os.remove("page_source_fn")

    

###--------------------------END OF MAIN FUNCTION----------------------------###
###--------------------------END OF MAIN FUNCTION----------------------------###










#*******************************************************************************
###------------------------'main' section of script---------------------------##
def main():
    """ Main entry point of the script """
    # placing actual main action in a 'helper'script so can call that easily 
    # with a distinguishing name in Jupyter notebooks, where `main()` may get
    # assigned multiple times depending how many scripts imported/pasted in.
    kwargs = {}
    '''
    if df_save_as_name == 'no_pickling':
        kwargs['pickle_df'] = False
    kwargs['return_df'] = False #probably don't want dataframe returned if 
    # calling script from command line
    '''
    interaction_tuples = pdb_code_to_prot_prot_interactions_via_PDBsum(
        pdb_code,**kwargs)
    print(interaction_tuples) # print results if calling script from command line
    # using https://www.saltycrane.com/blog/2008/01/how-to-use-args-and-kwargs-in-python/#calling-a-function
    # to build keyword arguments to pass to the function above
    # (see https://stackoverflow.com/a/28986876/8508004 and
    # https://stackoverflow.com/a/1496355/8508004 
    # (maybe https://stackoverflow.com/a/7437238/8508004 might help too) for 
    # related help). Makes it easy to add more later.





if __name__ == "__main__" and '__file__' in globals():
    """ This is executed when run from the command line """
    # Code with just `if __name__ == "__main__":` alone will be run if pasted
    # into a notebook. The addition of ` and '__file__' in globals()` is based
    # on https://stackoverflow.com/a/22923872/8508004
    # See also https://stackoverflow.com/a/22424821/8508004 for an option to 
    # provide arguments when prototyping a full script in the notebook.
    ###-----------------for parsing command line arguments-------------------###
    import argparse
    parser = argparse.ArgumentParser(prog='pdb_code_to_prot_prot_interactions_via_PDBsum.py',
        description="pdb_code_to_prot_prot_interactions_via_PDBsum.py \
        Takes a PDB code and returns a list of the interacting protein pairs \
        chain designation for that structure. The pairs are returned as a list \
        of tuples. \
        Meant to be a utility script for working \
        with PDBsum and Python.\
        **** Script by Wayne Decatur   \
        (fomightez @ github) ***")
    parser.add_argument("pdb_code", help="PDB code identifier for structure \
        of interest.\
        ", metavar="PDB_CODE")




    #I would also like trigger help to display if no arguments provided because 
    # need at least one for url
    if len(sys.argv)==1:    #from http://stackoverflow.com/questions/4042452/display-help-message-with-python-argparse-when-script-is-called-without-any-argu
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    pdb_code = args.pdb_code



    main()

#*******************************************************************************
###-***********************END MAIN PORTION OF SCRIPT***********************-###
#*******************************************************************************
