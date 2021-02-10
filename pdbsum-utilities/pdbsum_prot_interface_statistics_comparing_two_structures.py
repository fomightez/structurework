#!/usr/bin/env python
# pdbsum_prot_interface_statistics_comparing_two_structures.py
__author__ = "Wayne Decatur" #fomightez on GitHub
__license__ = "MIT"
__version__ = "0.1.0"


# pdbsum_prot_interface_statistics_comparing_two_structures.py by Wayne Decatur
# ver 0.1
#
#*******************************************************************************
# Verified compatible with both Python 2.7 and Python 3.8; written initially in 
# Python 3. 
#
#
# PURPOSE: Takes two PDB codes and gets the corresponding protein-protein 
# interface statistics from PDBsum for each and converts the two  
# tables for two structures into a single easy-to-compare Pandas dataframe. 
# Saves that dataframe and saves a file of that dataframe for use elsewhere. 
# Optionally, it can also return that dataframe for use inside a Jupyter 
# notebook.
#
# Keep in mind this only compares portions in the structure for which there was 
# experimental data. Explore the 'Missing Residues' of any chains of interest.
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
# Developed by adapting backbone of `pdbsum_prot_interface_statistics_to_df` to 
# handle interface statistics for two structures.
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
# python pdbsum_prot_interface_statistics_comparing_two_structures.py PDB_CODE PDB_CODE
#-----------------------------------
# Issue `pdbsum_prot_interface_statistics_comparing_two_structures.py -h` for details.
# 
# More examples from running from the command line are at the links below: 
# https://git.io/Jtfon
#
#
#
# To use this after importing/pasting or loading into a cell in a Jupyter 
# notebook, specify at least the data file (or data as a string) in the 
# call to the main function similar to below:
# df = pdbsum_prot_interface_statistics_comparing_two_structures("6kiv")
# df
#
#
# A more in-depth series of examples of using this script within a notebook 
# without need to save file intermediates is found at:
# https://git.io/Jtfon
#
# 
#
'''
CURRENT ACTUAL CODE FOR RUNNING/TESTING IN A NOTEBOOK WHEN IMPORTED/LOADED OR 
PASTED IN ANOTHER CELL:
from pdbsum_prot_interface_statistics_comparing_two_structures import pdbsum_prot_interface_statistics_comparing_two_structures
df = pdbsum_prot_interface_statistics_comparing_two_structures("6kiv","6kiz")
df
'''
#
#*******************************************************************************
#





#*******************************************************************************
##################################
#  USER ADJUSTABLE VALUES        #

##################################
#

## Settings and options for output dataframe-as-file 
df_save_as_name = 'int_stats_comparison_pickled_df.pkl' #name for pickled 
#dataframe file

#
#*******************************************************************************
#**********************END USER ADJUSTABLE VARIABLES****************************













#*******************************************************************************
#*******************************************************************************
###DO NOT EDIT BELOW HERE - ENTER VALUES ABOVE###

import sys
import os
import pandas as pd
import numpy as np


###---------------------------HELPER FUNCTIONS-------------------------------###
from contextlib import contextmanager,redirect_stderr,redirect_stdout
from os import devnull

@contextmanager
def suppress_stdout_stderr():
    """
    A context manager that redirects stdout and stderr to devnull.
    From https://stackoverflow.com/a/52442331/8508004
    """
    with open(devnull, 'w') as fnull:
        with redirect_stderr(fnull) as err, redirect_stdout(fnull) as out:
            yield (err, out)

def _(row):
    '''
    takes the row and .... PLACEHOLDER FOR NOW
    '''
    return _



def handle_pickling_the_dataframe(df, pickle_df,df_save_as_name):
    '''
    Was at end but moved to a function because will be used when 'empty' data
    provided where no interaction occurs.
    '''
    if pickle_df == False:
        sys.stderr.write("\n\nA dataframe of the data "
        "was not stored for use\nelsewhere "
        "because `no_pickling` was specified.")
    else:
        df.to_pickle(df_save_as_name )
        # Let user know
        sys.stderr.write("\n\nA dataframe of the data "
        "has been saved as a file\nin a manner where other "
        "Python programs can access it (pickled form).\n"
        "RESULTING DATAFRAME is stored as ==> '{}'".format(df_save_as_name ))

def arrange_returning_the_dataframe_and_info(
    df,pdb_code_id,return_df,return_pdb_code):
    '''
    Was at end but moved to a function because will be used when 'empty' data
    provided where no interaction occurs.
    '''
    if return_df and return_pdb_code:
        sys.stderr.write("\n\nReturning both the PDB code identifier and a "
            "dataframe with the information as well.")
        return pdb_code_id,df
    elif return_df:
        sys.stderr.write("\n\nReturning a dataframe with the information "
                "as well.")
        return df


###--------------------------END OF HELPER FUNCTIONS-------------------------###
###--------------------------END OF HELPER FUNCTIONS-------------------------###

#*******************************************************************************
###------------------------'main' function of script--------------------------##

def pdbsum_prot_interface_statistics_comparing_two_structures(pdb_code1, 
    pdb_code2, return_df = True, pickle_df=True):
    '''
    Main function of script. 
    PDBsum protein-protein Interface statistics tables for two structures to 
    an easy-to-compare Pandas dataframe.
    Optionally also returns a dataframe of the data. 
    Optionally can also return the PDB code found inside the parse data as well.
    Meant for use in a Jupyter notebook.

    Adapted from the main function in `blast_to_df.py`
    '''
    # GET NECESSARY COMPANION SCRIPTS AND IMPORT FUNCTIONS:
    #--------------------------------------------------------------------------#
    file_needed = "pdbsum_prot_interface_statistics_to_df.py"
    if not os.path.isfile(file_needed):
        sys.stderr.write("\nObtaining script containing a function to use to "
            "parse the interaction statistics from PDBsum "
            "...\n")
      # based on http://amoffat.github.io/sh/
        from sh import curl
        curl("-OL",
            "https://raw.githubusercontent.com/fomightez/structurework/master"
            "/pdbsum-utilities/"+file_needed)
        # verify that worked & ask for it to be done manually if fails
        if not os.path.isfile(file_needed):
            github_link = ("https://github.com/fomightez/structurework/tree"
                "/master/pdbsum-utilities")
            sys.stderr.write("\n'+file_needed+' not found. "
                "Please add it to your current working\ndirectory from {}"
                ".\n**EXITING !!**.\n".format(github_link))
            sys.exit(1)
    from pdbsum_prot_interface_statistics_to_df import pdbsum_prot_interface_statistics_to_df

    # MAKE DATAFRAMES FOR BOTH STRUCTURES:
    #--------------------------------------------------------------------------#
    sys.stderr.write("\nParsing interaction statistics from PDBsum ...\n")
    with suppress_stdout_stderr():
        structure1_df = pdbsum_prot_interface_statistics_to_df(pdb_code1, 
            pickle_df=False)
        sys.stderr.write("\n")
        structure2_df = pdbsum_prot_interface_statistics_to_df(pdb_code2, 
            pickle_df=False)
    dfs = [structure1_df, structure2_df]

    # Prepare dataframes for combining by moving chains to index
    for indx,the_df in enumerate(dfs):
        dfs[indx] = the_df.set_index('Chains')

    # COMBINE INTO SINGLE DATAFRAME THE INFORMATION FOR BOTH STRUCTURES:
    #--------------------------------------------------------------------------#
    # Based on https://stackoverflow.com/q/45307296/8508004 & 
    # https://stackoverflow.com/a/45307471/8508004 to combine dataframes of 
    # interface statistics with same column names and add in PDB code, placing 
    # the columns with same name next to each but with the groups (PDB id codes) 
    # below. Interweaves/interleaves(?) each column from each dataframe.
    df = pd.concat(
        [dfs[0],dfs[1]],axis=1,keys=[pdb_code1,pdb_code2]).swaplevel(
        0,1,axis=1).sort_index(axis=1)# based on 
    # https://stackoverflow.com/a/45307471/8508004
    # fix order of columns because seems to get changed around and would prefer
    # like PDBsum table
    order_at_pdbsum = (['No. of interface residues', 'Interface area (Å2)', 
        'No. of salt bridges', 'No. of disulphide bonds',
        'No. of hydrogen bonds', 'No. of non-bonded contacts'])
    df = df.reindex(order_at_pdbsum, axis=1, level=0) #based on
    # https://stackoverflow.com/a/52046294/8508004
    # feedback
    sys.stderr.write("Interface statistics for provided structures read and "
        "converted to a single dataframe...")

    sys.stderr.write("\nKeep in mind this only compares portions in the "
        "structure "
        "for which there was experimental data.\nYou'll want to explore the "
        "'Missing Residues' of any chains of interest.")


    # Reporting and Saving
    #---------------------------------------------------------------------------
    #print(df)#originally for debugging during development,added..
    # Document the full set of data collected in the terminal or 
    # Jupyter notebook display in some manner. 
    # Using `df.to_string()` because more universal than `print(df)` 
    # or Jupyter's `display(df)`.
    #sys.stderr.write("\nFor documenting purposes, the following lists the "
    #    "parsed data:\n")
    #with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #    display(df)
    #sys.stderr.write(df.to_string())

    # Handle pickling the dataframe
    handle_pickling_the_dataframe(df, pickle_df,df_save_as_name)

    
    # Return dataframe and pdb code(options)
    #---------------------------------------------------------------------------
    if return_df:
        sys.stderr.write("\n\nReturning a dataframe with the information "
            "as well.")
        return df
    

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
    if df_save_as_name == 'no_pickling':
        kwargs['pickle_df'] = False
    kwargs['return_df'] = False #probably don't want dataframe returned if 
    # calling script from command line
    pdbsum_prot_interface_statistics_comparing_two_structures(
        pdb_code1,pdb_code2,**kwargs)
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
    parser = argparse.ArgumentParser(prog='pdbsum_prot_interface_statistics_comparing_two_structures.py',
        description="pdbsum_prot_interface_statistics_comparing_two_structures.py \
        Takes two PDB codes and gets the corresponding protein-protein \
        interface statistics from PDBsum for each and converts the two tables \
        for two structures into a single easy-to-compare Pandas dataframe. \
        Optionally, it can \
        also return that dataframe for use inside a Jupyter notebook. \
        Meant to be a utility script for working \
        with PDBsum and Python.\
        **** Script by Wayne Decatur   \
        (fomightez @ github) ***")
    parser.add_argument("pdb_code1", help="Identifier code of a structure at \
        PDB.",
        metavar="PDB_CODE")
    parser.add_argument("pdb_code2", help="Identifier code of another structure \
        at PDB.",
        metavar="PDB_CODE")
    parser.add_argument('-dfo', '--df_output', action='store', type=str, 
    default= df_save_as_name, help="OPTIONAL: Set file name for saving pickled \
    dataframe. If none provided, '{}' will be used. To force no dataframe to \
    be saved, enter `-dfo no_pickling` without quotes as output file \
    (ATYPICAL).".format(df_save_as_name))



    #I would also like trigger help to display if no arguments provided because 
    # need at least one for url
    if len(sys.argv)==1:    #from http://stackoverflow.com/questions/4042452/display-help-message-with-python-argparse-when-script-is-called-without-any-argu
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    pdb_code1 = args.pdb_code1
    pdb_code2 = args.pdb_code2
    df_save_as_name = args.df_output


    main()

#*******************************************************************************
###-***********************END MAIN PORTION OF SCRIPT***********************-###
#*******************************************************************************
