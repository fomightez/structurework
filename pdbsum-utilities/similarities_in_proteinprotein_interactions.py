# similarities_in_proteinprotein_interactions.py
__author__ = "Wayne Decatur" #fomightez on GitHub
__license__ = "MIT"
__version__ = "0.1.0"


# similarities_in_proteinprotein_interactions.py by Wayne Decatur
# ver 0.1.0
#
#*******************************************************************************
# 
# PURPOSE: For a pair of proteins in related structures, this script highlights 
# at the residue level where the residue-to-residue protein-protein interactions 
# are maintained for a pair of proteins and also highlights individual residues 
# in one chain that still interact with the other chain even if the partner is 
# different. In other words, in addition to highlighting residue pairings 
# maintained in both structures it also highlights residues that have shifted in
# how they interact with the other chain. 
# Note that at this time this script DOES NOT discern if the specific type of 
# residue-to-residue is different; however, using the dataframe that can be 
# made using `pdsum_prot_interactions_list_to_df.py` from the data files this 
# can be determined. (This could be added later, see 'to do'.)
# Needs to work in conjunction with the notebook 
# `Using PDBsum data to highlight changes in protein-protein interactions.ipynb` 
# that is presently in https://github.com/fomightez/pdbsum-binder . In fact, the 
# easiest way to use this is to launch sessions by clicking on the 
# `launch binder` badge at that repo. In the session that comes up, everything 
# will already be installed and available for working through the notebook 
# `Using PDBsum data to highlight changes in protein-protein interactions.ipynb` 
# that does this comparison for a demonstration set of chains in two related
# structures. Users can then change the PDB codes and chain designations to 
# analyze their own structures and protein chain interactions of interest.
# 
#
# You should probably also check out the output from the related scripts
# `differences_in_proteinprotein_interactions.py` (and coming soon: `subtle_atomiclevel_diffs_in_proteinprotein_interactions_for_shared_pairs.py`)
# 
#
#
#
# to do: 
# - Since this script DOES NOT at this time discern if the specific type of 
# residue-to-residue is different; however, using the dataframe that is used to 
# collect the interaction partners this could be determined by going through 
# each residue-residue pairing that is shared and subsetting the rows of the two 
# dataframes (one each from the related structures) that included these and 
# making a list from the type column and then seeing if the lists from each 
# structure match. If add this remove note from 'PURPOSE' and accompanying
# material describg this script, such as a README or companion notebook. <-- oh
# wait this 'type' difference could probably be added as part of the
#`subtle_atomiclevel_diffs_in_proteinprotein_interactions_for_shared_pairs.py`
# that I propose below!!!
# `Using PDBsum data to highlight changes in protein-protein interactions.ipynb`
# - perhaps make another, related script that goes through the collection of
# residue and partner interactions that are maintained by the same residues in
# both structures and see if the specifics have subtlely changed. The collection
# to use for that is the `the_shared_interactions` from the 
# `similarities_in_proteinprotein_interactions.py` script and then go back to 
# the dataframe for each structure and collect rows matching both the chain# 1
# and chain# residues in the tuples of the individual pairs in the 
# `the_shared_interactions`, mine for each structure the atoms involved in each 
# row for that pair and then see if they differ between the two structures. <--
# could call script 
# `subtle_atomiclevel_diffs_in_proteinprotein_interactions_for_shared_pairs.py`
# (also should note 'type' differences even if the involved atoms are different,
# see above! - I think both would be good to keep together since input set the
# same on both and in fact I think I spelled out much of how to do it better
# in describing 
# `subtle_atomiclevel_diffs_in_proteinprotein_interactions_for_shared_pairs.py`;
# the emphais on what is collected would just have to be expanded do do both on
# same iteration.)

import os
import sys
import glob
from shutil import copyfile
import subprocess
import pandas as pd
import numpy as np
#from halo import HaloNotebook as Halo
from IPython.utils import io





################################################################################
#######----------------------HELPER FUNCTIONS-----------------------------######
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

def res_tuple_simple(items):
    '''
    takes columns with Atom#1 residue number and chain designation along with
    Atom#2 residue number and chain designation
    and returns a tuple of residue number 1 position number first followed by 
    residue number 2 position number.
    '''
    # check for 'empty' dataframe using `np.isnan(items[0])`, based on https://stackoverflow.com/a/29528160/8508004 ; allows rest of script to run
    # gracefully if there were no interactions between the two chains examined
    # for one of the sturctures and thus 'empty' dataframe produced from PDBsum
    # data
    if np.isnan(items[0]):
        return ("0","0")
    return ("{}".format(items[0]),"{}".format(items[2]))
def res_tuple(items):
    '''
    takes columns with Atom#1 residue number and chain designation along with
    Atom#2 residue number and chain designation
    and returns a tuple of residue#1 information first followed by 
    residue#2 information.
    Uses Jmol/Jsmol convention where `161:B` means residue #161 of chain B.
    '''
    # check for 'empty' dataframe using `np.isnan(items[0])`, based on https://stackoverflow.com/a/29528160/8508004 ; allows rest of script to run
    # gracefully if there were no interactions between the two chains examined
    # for one of the sturctures and thus 'empty' dataframe produced from PDBsum
    # data
    if np.isnan(items[0]):
        return ("0:NA","0:NA")
    return ("{}:{}".format(items[0],items[1]),"{}:{}".format(items[2],items[3]))

def write_string_to_file(s, fn):
    '''
    Takes a string, `s`, and a name for a file & writes the string to the file.
    '''
    with open(fn, 'w') as output_file:
        output_file.write(s)

def out2_stderr_n_log(s,log_file_text):
    '''
    Takes a string as input and sends it to the stderr as well as to a building
    string that will everntually get saved as a Log file.
    Also needs the Log file to be sent in because gets assigned within the
    function in order to add to it. Returns the modified `log_file_text`.
    '''
    sys.stderr.write(s)
    log_file_text += s
    return log_file_text


import time
from IPython.display import display, Javascript
import hashlib
def save_notebook(file_path):
    '''
    Function to save a notebook from 
    https://stackoverflow.com/a/57814673/8508004

    IMPORTANTLY, this won't work in the JupyterLab interface for notebooks!
    See https://github.com/jupyterlab/jupyterlab/issues/7627
    '''
    start_md5 = hashlib.md5(open(file_path,'rb').read()).hexdigest()
    display(Javascript('IPython.notebook.save_checkpoint();'))
    current_md5 = start_md5
    while start_md5 == current_md5:
        time.sleep(1)
        current_md5 = hashlib.md5(open(file_path,'rb').read()).hexdigest()



def chunk_string(string, chunk_size):
    """Return a list of n-sized chunks from string of letters."""
    return [string[i:i+chunk_size] for i in range(0, len(string),chunk_size)] 


def strip_off_first_line(fn,set_name,character_to_mark_set_name_end):
    '''
    This takes a name of a file & then uses the shell to remove the first line.
    In order to leave the input file intact, a new multi-sequence FASTA file
    is made and that is used in place of the one where the label was the first
    line. The set sample name extracted gets added to the file name.
    Removing first line based on 
    https://unix.stackexchange.com/questions/96226/delete-first-line-of-a-file
    '''
    name_for_f_without_first_line = (
        f"{set_name}{character_to_mark_set_name_end}set.fa")
    #!tail -n +2 {fn} >{name_for_f_without_first_line} 
    os.system(f"tail -n +2 {fn} >{name_for_f_without_first_line}")
    return name_for_f_without_first_line


def percent_GCcalc(items):
    '''
    takes a list of three and calculates percentage of sum of first
    two itemswithin total (second item)

    Taken from 
    `GSD Adding_percentGC_to_nt_counts_for_mito_genomes_from_1011_collection.ipynb`
    '''
    return (items[0] + items[1])/items[2]


#######------------------END OF HELPER FUNCTIONS--------------------------######
################################################################################



#### SOME SETTINGS FOR THE MAIN PART OF THE SCRIPT
# Anything go here?







################################################################################
#######------------------------MAIN SECTION-------------------------------######

#spinner = Halo(text='Processing...', spinner='dots',color = 'magenta')
#spinner.start()

# GET NECESSARY COMPANION SCRIPTS AND IMPORT FUNCTIONS:
#------------------------------------------------------------------------------#
file_needed = "pdbsum_prot_interactions_list_to_df.py"
if not os.path.isfile(file_needed):
    sys.stderr.write("\nObtaining script containing a function to use to parse "
        "the data files from PDBsum "
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
from pdbsum_prot_interactions_list_to_df import pdbsum_prot_interactions_list_to_df

# MAKE DATAFRAMES FOR BOTH STRUCTURES:
#------------------------------------------------------------------------------#
sys.stderr.write("\nParsing data files from PDBsum ...\n")
with suppress_stdout_stderr():
    structure1_pdb_code, structure1_df = pdbsum_prot_interactions_list_to_df(
        structure1_data_name, pickle_df=False, return_pdb_code=True)
    sys.stderr.write("\n")
    structure2_pdb_code, structure2_df = pdbsum_prot_interactions_list_to_df(
        structure2_data_name, pickle_df=False, return_pdb_code=True)
dfs = [structure1_df, structure2_df]

# ADD A COLUMN TO DATAFRAME THAT IS TUPLE OF BOTH RESIDUES
#------------------------------------------------------------------------------#
# To make things easy going forward include the chain designation in the tuple
# as well using Jmol convention since is familiar to me. So residue 161 of 
# chain B interacting with residue 3371 of chain K would be the following tuple:
# (161:B,3371:K)
sys.stderr.write("\nCollecting similarities for chain vs chain interactions "
    "in the two structures ...\n")
dfs_with_extra_column = []
for df in dfs:
    df['partner_residues'] = df[['Atom1 Res no.','Atom1 Chain',
        'Atom2 Res no.','Atom2 Chain']].apply(res_tuple_simple, axis=1)
    df['partner_residues_w_chain'] = df[['Atom1 Res no.','Atom1 Chain',
        'Atom2 Res no.','Atom2 Chain']].apply(res_tuple, axis=1)
    dfs_with_extra_column.append(df)
dfs = dfs_with_extra_column # replace the list of dataframes with the dataframes 
# with the new tuple column(s)

# COLLECT THE TUPLES AS A LIST
#------------------------------------------------------------------------------#
# keep the list in a list where first one is from structure #1 and second is 
# from structure #2.
tuples_list = []
for df in dfs:
    tuples_list.append(df['partner_residues_w_chain'].tolist())

# TOSS OUT REPEATS BY MAKING THE LIST A SET 
#------------------------------------------------------------------------------#
# keep the list in a list where first one is from structure #1 and second is 
# from structure #2.
unique_tuples_sets = []
for the_list in tuples_list:
    unique_tuples_sets.append(set(the_list))
tuples_list = [list(x) for x in unique_tuples_sets] # Do I need it converted 
# back to a list?

# IDENTIFY THE SAME PAIRS IN BOTH STRUCTURES USING SET MATH (INTERSECTION)
#------------------------------------------------------------------------------#
# The intersection of the two tuples list are the residue interactions that
# are shared between the two structues.
the_shared_interactions = (
    unique_tuples_sets[0].intersection(unique_tuples_sets[1]))

# IDENTIFY THE RESIDUES THAT NO LONGER HAVE THE SAME PARTNERS 
#------------------------------------------------------------------------------#
# Identify the residues for each chain in that are similar in that they still 
# contribute to the interaction with the other chain, yet no longer have the 
# same partners.
# When reporting on these HERE just highlight they are still involved in the 
# interaction and don't report here the new partner, save that for the 
# 'differences' script.
chain1_shifted_res = []
chain2_shifted_res = []

# Exclude the intersection members by focusing on difference for each. NEVERMIND
diff_tuples_structure1 = unique_tuples_sets[0].difference(unique_tuples_sets[1]) #should be 
# the tuples list for structure 1 without those in the_shared_interactions; 
# DECIDED TO BE MORE THOROUGH AND NOT USE THIS IN THE LOOP.
diff_tuples_structure2 = unique_tuples_sets[1].difference(unique_tuples_sets[0]) #should be 
# the tuples list for structure 2 without those in the_shared_interactions; 
# DECIDED TO BE MORE THOROUGH AND NOT USE THIS DETEMRINING THOSE THAT POSESS 
# SOME NEW PARTNERS.

# I don't think I need it; however...
# REmmber "to find the values that exist in only one set, we use 
# .symmetric_difference(). Think of this as the union minus the intersection." , 
# or all those that don't occur in both structures, the example here
# see 
# https://medium.com/better-programming/a-visual-guide-to-set-comparisons-in-python-6ab7edb9ec41

# Now loop on all the tuples and check the residues for first chain which are 
# always on left half of the tuple. Collect all interaction partners & see if 
# the sets (want `set` because don't care if the same residue is in interaction 
# 3 or 5 times) for each structure changes. WHEN DOING EACH CHECK WANT TO LOOP 
# OVER ALL THE RESIDUES 
# INVOLED FOR THE PARTICULAR CHAIN, REGARDLESS OF WHAT STRUCTURE IT OCCURS IN
# BECAUSE WANT TO CHECK FOR SHIFTS IN CHAIN INTERACTIONS FOR ALL RESIDUES OF THAT
# PARTICULAR CHAIN SEEN TO INTERACT WITH THE OTHER CHAIN, THAT'S FOR THE 
# INITIAL `for t in` THESE TWO LOOPS START OUT WITH. For interating on each 
# structure (inner, sub looping), I could get away with not including those in
# the_shared_interactions, i.e., diff_tuples_structure1  & 
# diff_tuples_structure2 I define above; however, it won't save that much effort
# and in regards to fully seeing what partners shifted later it would be more 
# informative to include all so I can collect all the partners at the same time.
# Make a dictionary for each structure and each chain (so four total) and 
# use the residue number of each as key. So the list of the four 
# dictionaries `partners_dicts` will be - Structure#1, chain#1; 
# Structure#2, chain#1; Structure#1, chain#2; Structure#2, chain#2
partners_dicts =[]
structure1_partners_dict={}
structure2_partners_dict={}
for t in unique_tuples_sets[0].union(unique_tuples_sets[1]):
    residue = int(t[0].split(":")[0] )# will get chain 1 residue & so combined
    #  with above for loop, will iterate on all residues in chain 1 involved in 
    # interactions in both structure 1 and 2
    residue_partner = int(t[1].split(":")[0])
    structure1_partners_for_residue = []
    for i in unique_tuples_sets[0]:
        left_side_of_tuple = int(i[0].split(":")[0])
        right_side_of_tuple = int(i[1].split(":")[0])
        if left_side_of_tuple == residue:
            structure1_partners_for_residue.append(right_side_of_tuple)
    # add the list of partners, as a set, for the residue in structure#1 if not 
    # empty set; it may be an empty set because iterating on all residues in 
    # chain#1 that interact and some may not interact in structure#1
    if set(structure1_partners_for_residue): 
        structure1_partners_dict[residue] = set(structure1_partners_for_residue)
    structure2_partners_for_residue = []
    for i in unique_tuples_sets[1]:
        left_side_of_tuple = int(i[0].split(":")[0])
        right_side_of_tuple = int(i[1].split(":")[0])
        if left_side_of_tuple == residue:
            structure2_partners_for_residue.append(right_side_of_tuple)
    if set(structure2_partners_for_residue):
        structure2_partners_dict[residue] = set(structure2_partners_for_residue)
    if set(structure1_partners_for_residue) != set(structure2_partners_for_residue):
        # don't bother adding if already there, & ALSO DON'T ADD IF EITHER SET
        # IS EMPTY AS THAT MEANS IT ONLY CONTRIBUTES TO INTERACTION WITH THE 
        # OTHER CHAIN IN ONE STRUCTURE, isn't shifted. By the way, those that
        # only contribure to interaction with the other chain in one structure 
        # will get identified in the 'differences' script.
        if residue not in chain1_shifted_res and (
            set(structure1_partners_for_residue) and set(
            structure2_partners_for_residue)):
            chain1_shifted_res.append(residue)
partners_dicts.append(structure1_partners_dict)
partners_dicts.append(structure2_partners_dict)
# now loop on all tuples & check the residues for other chain which are always 
# on right half of the tuple
structure1_partners_dict={}
structure2_partners_dict={}
for t in unique_tuples_sets[0].union(unique_tuples_sets[1]):
    residue = int(t[1].split(":")[0]) # will get chain 2 residue & so combined 
    # with above for loop, will iterate on all residues in chain 2 involved in 
    # interactions in both structure 1 and 2
    residue_partner = int(t[0].split(":")[0])
    structure1_partners_for_residue = []
    for i in unique_tuples_sets[0]:
        right_side_of_tuple = int(i[1].split(":")[0])
        left_side_of_tuple = int(i[0].split(":")[0])
        if right_side_of_tuple == residue:
            structure1_partners_for_residue.append(left_side_of_tuple)
    if set(structure1_partners_for_residue):
        structure1_partners_dict[residue] = set(structure1_partners_for_residue)
    structure2_partners_for_residue = []
    for i in unique_tuples_sets[1]:
        right_side_of_tuple = int(i[1].split(":")[0])
        left_side_of_tuple = int(i[0].split(":")[0])
        if right_side_of_tuple == residue:
            structure2_partners_for_residue.append(left_side_of_tuple)
    if set(structure2_partners_for_residue):
        structure2_partners_dict[residue] = set(structure2_partners_for_residue)
    if set(structure1_partners_for_residue) != set(structure2_partners_for_residue):
        if residue not in chain2_shifted_res and (
            set(structure1_partners_for_residue) and set(
            structure2_partners_for_residue)):
            chain2_shifted_res.append(residue)
partners_dicts.append(structure1_partners_dict)
partners_dicts.append(structure2_partners_dict)
# Note that for `chain1_shifted_res` and `chain2_shifted_res`, don't need to be
# concerned with whether anything in 'Missing residues' category because by
# definition they cannot possible classified interacting with both structures if 
# not resolved in both.


# Notes for 'differences' script:
# following gives the residues of chain#1 that contribute to one structure not the other
set(partners_dicts[0].keys()).symmetric_difference(set(partners_dicts[1].keys()))
# following gives the residues of chain#2 that contribute to one structure not the other
set(partners_dicts[2].keys()).symmetric_difference(set(partners_dicts[3].keys()))
# following gives the residues of chain#1 that contribute to structure#1 but not structure #2
chain1_res_only_contributing_to_structure1 = (
    set(partners_dicts[0].keys()).difference(set(partners_dicts[1].keys())))
# following gives the residues of chain#1 that contribute to structure#2 but not structure #1
chain1_res_only_contributing_to_structure2 = (
    set(partners_dicts[1].keys()).difference(set(partners_dicts[0].keys())))
# following gives the residues of chain#2 that contribute to structure#1 but not structure #2
chain2_res_only_contributing_to_structure1 = (
    set(partners_dicts[2].keys()).difference(set(partners_dicts[3].keys())))
# following gives the residues of chain#2 that contribute to structure#2 but not structure #1
chain2_res_only_contributing_to_structure2 = (
    set(partners_dicts[3].keys()).difference(set(partners_dicts[2].keys())))

# SUMMARY REPORT
#------------------------------------------------------------------------------#
sys.stderr.write("\nDetermination of SIMILARITIES Completed.\n\n"
    "************************RESULTS************************")
sys.stderr.write("\nThe following interacting pairs of residues occur in "
    "both structures:")
for i in the_shared_interactions:
    sys.stderr.write("\n("+str(i[0])+", "+str(i[1])+")")

chain1_designation_rep = list(unique_tuples_sets[0])[0][0].split(":")[1]
chain2_designation_rep = list(unique_tuples_sets[0])[0][1].split(":")[1]
# The 'first' chain in structure #1 and structure #2 can have different 
# designations and still be the same proteins & so in those cases I'm going to
# have the 'first' chain represented by structure1 designation separated by a 
# forward slash from structure2 sdesignation, like `R/C`. Same for 'second' 
#chain.
if chain1_designation_rep != list(unique_tuples_sets[1])[0][0].split(":")[1]:
    chain1_designation_rep += "/{}".format(
        list(unique_tuples_sets[1])[0][0].split(":")[1])
if chain2_designation_rep != list(unique_tuples_sets[1])[0][1].split(":")[1]:
    chain2_designation_rep += "/{}".format(
        list(unique_tuples_sets[1])[0][1].split(":")[1])
sys.stderr.write("\n\nThe following residues of chain "+chain1_designation_rep+
    " contribute to interactions with\nchain "+chain2_designation_rep+
    " in both structures " +structure1_pdb_code+" & "+structure2_pdb_code+","
    " yet have differing sets of partners:")
for i in chain1_shifted_res:
    sys.stderr.write("\n"+str(i))

sys.stderr.write("\n\nThe following residues of chain "+chain2_designation_rep+
    " contribute to interactions with\nchain "+chain1_designation_rep+
    " in both structures " +structure1_pdb_code+" & "+structure2_pdb_code+","
    " yet have differing sets of partners:")
for i in chain2_shifted_res:
    sys.stderr.write("\n"+str(i))
sys.stderr.write("\nThe differing sets of partners are detailed by running the"
    " 'difference' script.")




#######------------------END OF MAIN SECTION------------------------------######
################################################################################
