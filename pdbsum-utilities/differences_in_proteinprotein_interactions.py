# differences_in_proteinprotein_interactions.py
__author__ = "Wayne Decatur" #fomightez on GitHub
__license__ = "MIT"
__version__ = "0.1.0"


# differences_in_proteinprotein_interactions.py by Wayne Decatur
# ver 0.1.0
#
#*******************************************************************************
# 
# PURPOSE: For a pair of proteins in related structures, this script highlights 
# at the residue level where the residue-to-residue protein-protein interactions 
# differ for a pair of proteins. Among the results are the details of shifts of
# partners paired that occur for a residue in the two structures. 
# Note that this script is only concerned with differences that result in 
# differences at the level of the residue. If specific atom to atom chage or 
# are lost while the same residues still interact in some way, those SUBTLE 
# CHANGES WILL NOT BE HIGHLIGHTED here. (To add this I think it would probably
# be best to do in another related script,see 'to do' for possibility later.)
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
# You should probably also check out the output from the related script 
# `similarities_in_proteinprotein_interactions.py` (and coming soon: `subtle_atomiclevel_diffs_in_proteinprotein_interactions_for_shared_pairs.py`)
#
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
file_needed = "similarities_in_proteinprotein_interactions.py"
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

# MAKE DATAFRAMES FOR BOTH STRUCTURES AND GENERATE THE PYTHON OBJECTS NEEDED:
#------------------------------------------------------------------------------#
#`similarities_in_proteinprotein_interactions.py` does much of what is needed 
# (and more) so silently run that script and then continue on effort to compile
# information needed for report from this script
# see https://gist.github.com/fomightez/ed79e33e97601d839dd550fd224d583c for 
# information on approaching it this way. (An overarching reason is I didn't 
# want to refactor `similarities_in_proteinprotein_interactions.py` since it 
# works now and will only be getting called by that notebook. So this allows
# easier continuing develpment.)
sys.stderr.write("\nParsing data files from PDBsum ...\n")
with suppress_stdout_stderr():
    exec(open("similarities_in_proteinprotein_interactions.py").read())


# GET INTERACTION PAIRS WITH BOTH RESIDUES ENTIRELY UNIQUE TO EACH STRUCTURE
#------------------------------------------------------------------------------#
# a lot of the 'differences' were already collected in the course of running
# the script `similarities_in_proteinprotein_interactions.py` that will parse
# both data files to make dataframes with tuples of the interactions; however,
# one that still needs identifying is where residues from both chains interact
# in one structure and not in the other. The phrase 'pairs with both residues 
# entirely unique to each structure' is key, with the emphasis on 'ENTIRELY'.
# Maybe describe in report as 
# `residue pairings where both members exclusively interact only in structure #1` 
# for structure1 with list of tupes following & similar working before list of 
# tuples for structure 2.
sys.stderr.write("\nCollecting differences for chain vs chain interactions "
    "in the two structures ...\n")
# Need a list of residues from each structure, from each chain; so four 
# lists total. Make integers so can easily use elsewhere if I want.
#left side residues (chain#1) from structure1
chain1_res_in_structure1 = dfs[0]['Atom1 Res no.'].tolist()
chain1_res_in_structure1 = [int(x) for x in chain1_res_in_structure1]
#right side residues (chain#2) from structure1
chain2_res_in_structure1 = dfs[0]['Atom2 Res no.'].tolist()
chain2_res_in_structure1 = [int(x) for x in chain2_res_in_structure1]
#left side residues (chain#1) from structure2
chain1_res_in_structure2 = dfs[1]['Atom1 Res no.'].tolist()
chain1_res_in_structure2 = [int(x) for x in chain1_res_in_structure2]
#right side residues (chain#2) from structure2
chain2_res_in_structure2 = dfs[1]['Atom2 Res no.'].tolist()
chain2_res_in_structure2 = [int(x) for x in chain2_res_in_structure2]
interaction_pairs_with_both_residues_entirely_unique_to_structure1 = []
# `unique_tuples_sets[0]` is the set from structure #1
for t in unique_tuples_sets[0]:
    left_side_of_tuple = int(t[0].split(":")[0])
    right_side_of_tuple = int(t[1].split(":")[0])
    left_side_residue_in_structure2 = (
        left_side_of_tuple in chain1_res_in_structure2)
    right_side_residue_in_structure2 = (
        right_side_of_tuple in chain2_res_in_structure2)
    if (not left_side_residue_in_structure2) and (
        not right_side_residue_in_structure2):
        if t not in interaction_pairs_with_both_residues_entirely_unique_to_structure1:
            interaction_pairs_with_both_residues_entirely_unique_to_structure1.append(t)
interaction_pairs_with_both_residues_entirely_unique_to_structure2 = []
# `unique_tuples_sets[1]` is the set from structure #2
for t in unique_tuples_sets[1]:
    left_side_of_tuple = int(t[0].split(":")[0])
    right_side_of_tuple = int(t[1].split(":")[0])
    left_side_residue_in_structure1 = (
        left_side_of_tuple in chain1_res_in_structure1)
    right_side_residue_in_structure1 = (
        right_side_of_tuple in chain2_res_in_structure1)
    if (not left_side_residue_in_structure1) and (
        not right_side_residue_in_structure1):
        if t not in interaction_pairs_with_both_residues_entirely_unique_to_structure2:
            interaction_pairs_with_both_residues_entirely_unique_to_structure2.append(t)


# GET INTERACTION PAIRS WITH BOTH RESIDUES ENTIRELY UNIQUE TO EACH STRUCTURE
#------------------------------------------------------------------------------#
# In the script `similarities_in_proteinprotein_interactions.py`, I noted 
# several sets that spell out residues of chains that contribute to one 
# structure and not the other. So have already been collected when that was run
# silently here. Pertinent variables yielded:
# chain1_res_only_contributing_to_structure1
# chain1_res_only_contributing_to_structure2
# chain2_res_only_contributing_to_structure1
# chain2_res_only_contributing_to_structure2


# ASSEMBLE DETAILS ON SHIFTS IN RESIDUE PARTNERS FOR SAME RESIDUE BETWEEN THE 
# DIFFERENT STRUCTURES
#------------------------------------------------------------------------------#
# Use `partners_dicts` to parse the details for the residues in 
# `chain1_shifted_res` and `chain2_shifted_res` where shifts have occured 
# between the two structures for residues in each chain. Remember the list of 
# the four dictionaries in `partners_dicts` will be - Structure#1, chain#1; 
# Structure#2, chain#1; Structure#1, chain#2; Structure#2, chain#2
# To prepare for the report make a dictonary where the key is residue number
# and the values are tuples of the interaction partners in structure#1 and 
# structure#2, in that order
chain1_shifts_dict = {}
for i in chain1_shifted_res:
    chain1_shifts_dict[i] = (partners_dicts[0][i],partners_dicts[1][i])
chain2_shifts_dict = {}
for i in chain2_shifted_res:
    chain2_shifts_dict[i] = (partners_dicts[2][i],partners_dicts[3][i])


#Report
#------------------------------------------------------------------------------#
sys.stderr.write("\nDetermination of DIFFERENCES Completed.\n\n"
    "************************RESULTS************************")
sys.stderr.write("\nThe following are residue pairings where both members "
    "exclusively\n"
    "interact only in " +structure1_pdb_code+" :")
for i in interaction_pairs_with_both_residues_entirely_unique_to_structure1:
    sys.stderr.write("\n("+str(i[0])+", "+str(i[1])+")")
sys.stderr.write("\n\nThe following are residue pairings where both members "
    "exclusively\n"
    "interact only in "+structure2_pdb_code+":")
for i in interaction_pairs_with_both_residues_entirely_unique_to_structure2:
    sys.stderr.write("\n("+str(i[0])+", "+str(i[1])+")")



sys.stderr.write("\n\nThe following residues of chain "+chain1_designation+
    " contribute only to interactions\nwith chain "+chain2_designation+" in "
    +structure1_pdb_code+":")
for i in chain1_res_only_contributing_to_structure1:
    sys.stderr.write("\n"+str(i))

sys.stderr.write("\nThe following residues of chain "+chain1_designation+
    " contribute only to interactions\nwith chain "+chain2_designation+" in "
    +structure2_pdb_code+":")
for i in chain1_res_only_contributing_to_structure2:
    sys.stderr.write("\n"+str(i))

sys.stderr.write("\nThe following residues of chain "+chain2_designation+
    " contribute only to interactions\nwith chain "+chain1_designation+" in "
    +structure1_pdb_code+":")
for i in chain2_res_only_contributing_to_structure1:
    sys.stderr.write("\n"+str(i))

sys.stderr.write("\nThe following residues of chain "+chain2_designation+
    " contribute only to interaction\nwith chain "+chain1_designation+" in "
    +structure2_pdb_code+":")
for i in chain2_res_only_contributing_to_structure2:
    sys.stderr.write("\n"+str(i))




sys.stderr.write("\n\nIf you've previously run the script "
    "`similarities_in_proteinprotein_interactions.py`\nyou received a report "
    "listing residues for each chain that still interact with\nthe other chain "
    "in both structures yet have different sets of residue\npartners in both "
    "structures.\nDetails of the shifts in partners follow.")
sys.stderr.write("\nThe following lists the differing sets of partners for "
    "residues of chain "+chain1_designation+",\nwith the "
    "chain "+chain2_designation+" partners in " +
    structure1_pdb_code+" followed by those in "+structure2_pdb_code+":")
for k,v in chain1_shifts_dict.items():
    sys.stderr.write("\n"+str(k)+": "+str(v[0])+", "+str(v[1]))
sys.stderr.write("\nThe following lists the differing sets of partners for "
    "residues of chain "+chain2_designation+",\nwith the "
    "chain "+chain1_designation+" partners in " +
    structure1_pdb_code+" followed by those in "+structure2_pdb_code+":")
for k,v in chain2_shifts_dict.items():
    sys.stderr.write("\n"+str(k)+": "+str(v[0])+", "+str(v[1]))


#######------------------END OF MAIN SECTION------------------------------######
################################################################################
