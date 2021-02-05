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
# differences at the level of the residue. If the specific atom-to-atom 
# interactions change or are lost while the same residues still interact in some
# way, those SUBTLE CHANGES WILL NOT BE HIGHLIGHTED here. (To add this I think 
# it would probably be best to do in another related script,see 'to do' for 
# possibility later.)
# Changes involving interactions with residues that are only observed in one of
# the structures are not reported as different in the report either. This is 
# because if this residue is not observed because it is among the 
# 'Missing Residues' in one structure then it is moot in regards to differences 
# in interactions between the two structures because cannot accurately say if 
# altered or not.
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
# - for showing all the missing residues, add it making an interval for showing
# in the report so it is much shorter of a list; code is in `has sequence interval ranges intervals overlap related code.md`
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
from Bio.PDB import *
from collections import defaultdict
import uuid 




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

def range_extract(lst):
    'Yield 2-tuple ranges or 1-tuple single elements from list of increasing'
    'ints; interval making code modified from' 
    'https://www.rosettacode.org/wiki/Range_extraction#Python'
    lenlst = len(lst)
    i = 0
    while i< lenlst:
        low = lst[i]
        while i <lenlst-1 and lst[i]+1 == lst[i+1]: i +=1
        hi = lst[i]
        if hi - low >= 1:    #<---MAIN DIFFERENCE
            yield (low, hi)
        else:
            yield (low,)
        i += 1
def ranges_to_text(ranges):
   return ', '.join( (('%i-%i' % r) if len(r) == 2 else '%i' % r)
        for r in ranges ) 


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

# GET THE STRUCTURE FILES
#------------------------------------------------------------------------------#
# Get the structure files in preparation for checking missing residues.
pdb_ids = [structure1, structure2]
files_needed = [pdb_code + ".pdb" for pdb_code in pdb_ids]
for file_needed in files_needed:
    if not os.path.isfile(file_needed):
        from sh import curl
        curl("-OL","https://files.rcsb.org/download/"+file_needed+".gz")
        os.system(f"gunzip {file_needed}.gz")

# MINE THE PDB FILES A LIST OF THE RESIDUES MISSING FOR EACH CHAIN OF INTEREST
#----------------------------------------------------------------------#
# Collect the missing residues per chain per PDB code id (latter based on 
# approach worked out for 
# https://github.com/fomightez/cl_demo-binder/blob/master/notebooks/Using%20Biopython%20PDB%20Header%20Parser%20to%20get%20missing%20residues.ipynb 
# from my repo https://github.com/fomightez/cl_demo-binder and also used 
# in code that will be in what will be the script
# `make_table_of_missing_residues_for_related_PDB_structures.py` [or whatever 
# actual final name is])
missing_per_chain_per_id = {} # PDB code will be a key for two dictionaries. For
# the two dictionaries, chain designations will be keys and for each key the 
# value associated will be a list of missing residues for the corresponding 
# chain with that designation.
for pdb_code in pdb_ids:
    # get the header
    h =parse_pdb_header(pdb_code + ".pdb")
    # for missing residues collecting, first extract information on chains in 
    # current structure. Note that the addition of `QUIET=True` is based on 
    # https://biopython.org/docs/1.75/api/Bio.PDB.PDBParser.html to suppress the 
    # warnings several PDB files were causing.
    structure = PDBParser(QUIET=True).get_structure(pdb_code, pdb_code + ".pdb")
    chains = [each.id for each in structure.get_chains()]
    # Make a dictionary for each chain of interest with value of a list. The 
    # list will be the list of residue positions collected while iterating in 
    # missing. Key will be the chain designation.
    missing_per_chain = defaultdict(list)
    # go through missing residues and populate each chain's list
    for residue in h['missing_residues']:
        if (residue["chain"] in chains):
            missing_per_chain[residue["chain"]].append(residue["ssseq"])
    missing_per_chain_per_id[pdb_code] = missing_per_chain


# MAKE DATAFRAMES FOR BOTH STRUCTURES AND GENERATE THE PYTHON OBJECTS NEEDED:
#------------------------------------------------------------------------------#
#`similarities_in_proteinprotein_interactions.py` does much of what is needed 
# (and more) so silently run that script and then continue on effort to compile
# information needed for sumamry report from this script
# see https://gist.github.com/fomightez/ed79e33e97601d839dd550fd224d583c for 
# information on approaching it this way. (An overarching reason is I didn't 
# want to refactor `similarities_in_proteinprotein_interactions.py` since it 
# works now and will only be getting called by that notebook. So this allows
# easier continuing development.)
sys.stderr.write("\nParsing data files from PDBsum ...\n")
with suppress_stdout_stderr():
    exec(open("similarities_in_proteinprotein_interactions.py").read())


# ACKNOWLEDGE IF RESIDUES MISSING IN INVOLVED CHAINS IN INVOLVED STRUCTURES
#------------------------------------------------------------------------------#
# The idea is the user should be reminded of the limits here if parts of 
# involved chains are missing in either involved chain. FOR NOW THIS ASSUMES
# THAT A PROTEIN IN THE TWO STRUCTURES HAVE THE SAME DESIGNATION AND THIS WON'T
# BE TRUE AND NEED FIXING.
# First determine if any of the four chains, two from each structure are missing
# residues, becuase if not this section is moot.
anything_missing = False
structure1_chain1 = list(unique_tuples_sets[0])[0][0].split(":")[1]
structure1_chain2 = list(unique_tuples_sets[0])[0][1].split(":")[1]
structure2_chain1 = list(unique_tuples_sets[1])[0][0].split(":")[1]
structure2_chain2 = list(unique_tuples_sets[1])[0][1].split(":")[1]

missing_in_structure1_chain1 = set(
    missing_per_chain_per_id[structure1_pdb_code][structure1_chain1]) # see 
# `chain1_designation_rep` in the similarity script
missing_in_structure1_chain2 = set(
    missing_per_chain_per_id[structure1_pdb_code][structure1_chain2]) # see 
# `chain2_designation_rep` in the similarity script
missing_in_structure2_chain1 = set(
    missing_per_chain_per_id[structure2_pdb_code][structure2_chain1])
missing_in_structure2_chain2 = set(
    missing_per_chain_per_id[structure1_pdb_code][structure2_chain2])
# Since 'chain1' should be the same structure, I don't want to call any 
# 'differences' that involved any of those residues so I should combine them to 
# make a set for filtering those out of the  putative difference lists.
# Similarly, for 'chain2'
missing_in_chain1 = (list(missing_in_structure1_chain1 )+
    list(missing_in_structure2_chain1))
missing_in_chain2 = (list(missing_in_structure1_chain2) +
    list(missing_in_structure2_chain2))
missing_in_chain1 = list(set(missing_in_chain1))
missing_in_chain2 = list(set(missing_in_chain2))
# since lists are boolean, make a list of all for testing if any missing
missing = missing_in_chain1 + missing_in_chain2
if missing:
    anything_missing = True

# Report if either chain in either structure has missing residues. Skip this 
# section entirely if neither chain in neither structure has anything missing.
if anything_missing:
    string_for_missing_preamble = ""
    # If both chains contain the same list of missing residues, report that list
    # here stating nothing will be said in regards to these residues.

    # Use sets to see if missing for protein chain1 designation in structure1 is 
    # same as missing for chain1 designation in structure2. Then same for 
    # missing for protein chain2 designation in structure1 is 
    # same as missing for chain2 designation in structure2. Because if all same
    # is missing say residues are missing in appropriate chains but that same 
    # ones are not observed so no effect on apparent differences.
    if (missing_in_structure1_chain1 == missing_in_structure2_chain1) and (
        missing_in_chain1):
        string_for_missing_preamble += ("\nChain {} in both structures is missing"
            " the same residues:".format(chain1_designation_rep))
        string_for_missing_preamble += "\n"+ranges_to_text(range_extract(
            sorted(list(missing_in_structure1_chain1))))
    elif missing_in_chain1:
        if list(missing_in_structure1_chain1):
            string_for_missing_preamble += ("\nChain {} in {} is missing"
                " the residues:".format(structure1_chain1,structure1_pdb_code))
            string_for_missing_preamble += "\n"+ranges_to_text(range_extract(
            sorted(list(missing_in_structure1_chain1))))
        if list(missing_in_structure2_chain1):
            string_for_missing_preamble += ("\nChain {} in {} is missing"
                " the residues:".format(structure2_chain1,structure2_pdb_code))
            string_for_missing_preamble += "\n"+ranges_to_text(range_extract(
            sorted(list(missing_in_structure2_chain1))))
    if (missing_in_structure1_chain2 == missing_in_structure2_chain2) and (
        missing_in_chain2):
        string_for_missing_preamble += ("\nChain {} in both structures is missing"
            " the same residues:".format(chain2_designation_rep))
        string_for_missing_preamble += "\n"+ranges_to_text(range_extract(
            sorted(list(missing_in_structure1_chain2))))
    elif missing_in_chain2:
        if list(missing_in_structure1_chain2):
            string_for_missing_preamble += ("\nChain {} in {} is missing"
                " the residues:".format(structure1_chain2,structure1_pdb_code))
            string_for_missing_preamble += "\n"+ranges_to_text(range_extract(
                sorted(list(missing_in_structure1_chain2))))
        if list(missing_in_structure2_chain2):
            string_for_missing_preamble += ("\nChain {} in {} is missing"
                " the residues:".format(structure2_chain2,structure2_pdb_code))
            string_for_missing_preamble += "\n"+ranges_to_text(range_extract(
                sorted(list(missing_in_structure2_chain2))))
    string_for_missing_preamble += ("\nNothing more will be said in regards to "
        "these 'Missing residues' in this report\nbecause determining whether "
        "they are involved in different interactions\nis moot.\n")



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
# for structure1 with list of tuples following & similar working before list of 
# tuples for structure 2.
sys.stderr.write("\nCollecting differences for interactions between the two "
    "chains\nin the two structures ...\n")
# Need a list of residues from each structure, from each chain; so four 
# lists total. Make integers so can easily use elsewhere if I want.
#left side residues (chain#1) from structure1
chain1_res_in_structure1 = dfs[0]['Atom1 Res no.'].tolist()
chain1_res_in_structure1 = [0 for x in chain1_res_in_structure1 if np.isnan(x)]# 
# add so when 'empty' data gets used, it fails gracefully
chain1_res_in_structure1 = [int(x) for x in chain1_res_in_structure1]
#right side residues (chain#2) from structure1
chain2_res_in_structure1 = dfs[0]['Atom2 Res no.'].tolist()
chain2_res_in_structure1 = [0 for x in chain2_res_in_structure1 if np.isnan(x)]
chain2_res_in_structure1 = [int(x) for x in chain2_res_in_structure1]
#left side residues (chain#1) from structure2
chain1_res_in_structure2 = dfs[1]['Atom1 Res no.'].tolist()
chain1_res_in_structure2 = [0 for x in chain1_res_in_structure2 if np.isnan(x)]
chain1_res_in_structure2 = [int(x) for x in chain1_res_in_structure2]
#right side residues (chain#2) from structure2
chain2_res_in_structure2 = dfs[1]['Atom2 Res no.'].tolist()
chain2_res_in_structure2 = [0 for x in chain2_res_in_structure2 if np.isnan(x)]
chain2_res_in_structure2 = [int(x) for x in chain2_res_in_structure2]
interaction_pairs_with_both_residues_entirely_unique_to_structure1 = []
# `unique_tuples_sets[0]` is the set from structure #1
for t in unique_tuples_sets[0]:
    left_side_of_tuple = int(t[0].split(":")[0])
    right_side_of_tuple = int(t[1].split(":")[0])
    # if either is among the 'missing residues', skip the rest because don't 
    # want this pair because may only be unique in one structure because both
    # not seen in  the other structure
    if left_side_of_tuple in missing_in_chain1:
        continue
    if right_side_of_tuple in missing_in_chain2:
        continue
    left_side_residue_in_structure2 = (
        left_side_of_tuple in chain1_res_in_structure2)
    right_side_residue_in_structure2 = (
        right_side_of_tuple in chain2_res_in_structure2)
    if (not left_side_residue_in_structure2) and (
        not right_side_residue_in_structure2):
        if (
            t not in interaction_pairs_with_both_residues_entirely_unique_to_structure1) and (str(t) != "('0:NA', '0:NA')"):
            interaction_pairs_with_both_residues_entirely_unique_to_structure1.append(t)
interaction_pairs_with_both_residues_entirely_unique_to_structure2 = []
# `unique_tuples_sets[1]` is the set from structure #2
for t in unique_tuples_sets[1]:
    left_side_of_tuple = int(t[0].split(":")[0])
    right_side_of_tuple = int(t[1].split(":")[0])
    # if either is among the 'missing residues', skip the rest because don't 
    # want this pair because may only be unique in one structure because both
    # not seen in the other structure
    if left_side_of_tuple in missing_in_chain1:
        continue
    if right_side_of_tuple in missing_in_chain2:
        continue
    left_side_residue_in_structure1 = (
        left_side_of_tuple in chain1_res_in_structure1)
    right_side_residue_in_structure1 = (
        right_side_of_tuple in chain2_res_in_structure1)
    if (not left_side_residue_in_structure1) and (
        not right_side_residue_in_structure1):
        if (t not in interaction_pairs_with_both_residues_entirely_unique_to_structure2) and (str(t) != "('0:NA', '0:NA')"):
            interaction_pairs_with_both_residues_entirely_unique_to_structure2.append(t)


# GET INTERACTION PAIRS WITH BOTH RESIDUES ENTIRELY UNIQUE TO EACH STRUCTURE
#------------------------------------------------------------------------------#
# In the script `similarities_in_proteinprotein_interactions.py`, I noted 
# several sets that spell out residues of chains that contribute to one 
# structure and not the other. So have already been collected UNFILTERED when 
# that was run silently here. Pertinent variables yielded:
# chain1_res_only_contributing_to_structure1
# chain1_res_only_contributing_to_structure2
# chain2_res_only_contributing_to_structure1
# chain2_res_only_contributing_to_structure2
# I ADDED 'UNFILTERED' IN NOTE ABOVE BECAUSE NEED TO FILTER OUT ANY WHERE ONLY 
# APPEARS TO BE CONTRIBUTING IN ONE STRUCTURE AND NOT THE OTHER BECAUSE NOT 
# RESOLVED IN THE OTHE STRUCTURE. Remove the 'missing residues', if any, from
# consideration in those.
if anything_missing:
    chain1_res_only_contributing_to_structure1 = (
        chain1_res_only_contributing_to_structure1.difference(
        set(missing_in_chain1)))
    chain1_res_only_contributing_to_structure2 = (
        chain1_res_only_contributing_to_structure2.difference(
        set(missing_in_chain1)))
    chain2_res_only_contributing_to_structure1 = (
        chain2_res_only_contributing_to_structure1.difference(
        set(missing_in_chain2)))
    chain2_res_only_contributing_to_structure2 = (
        chain2_res_only_contributing_to_structure2.difference(
        set(missing_in_chain2)))
# make it handle 'empty' dataframes more gracefully. Tried to abrogate chance
# it would flag issues where for some reason a residue actually numbered zero
# by restricting to cases where length of the dataframe of interactions is only
# one row and has np.nan.
if len(dfs[0]) == 1 and np.isnan(dfs[0]["Atom1 no."][0]):
    chain1_res_only_contributing_to_structure1 = (
        [x for x in chain1_res_only_contributing_to_structure1 if x != 0])
    chain2_res_only_contributing_to_structure1 = (
        [x for x in chain2_res_only_contributing_to_structure1 if x != 0])
if len(dfs[1]) == 1 and np.isnan(dfs[1]["Atom1 no."][0]):
    chain1_res_only_contributing_to_structure2 = (
        [x for x in chain1_res_only_contributing_to_structure2 if x != 0])
    chain2_res_only_contributing_to_structure2 = (
        [x for x in chain2_res_only_contributing_to_structure2 if x != 0])
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


# SUMMARY REPORT
#------------------------------------------------------------------------------#
sys.stderr.write("\nDetermination of DIFFERENCES Completed.\n\n"
    "************************RESULTS************************")
if anything_missing:
    sys.stderr.write("\n"+string_for_missing_preamble)
    '''
    sys.stderr.write("\nBecause assessment of differences is moot if a residue "
        "is not resolved in one structure, no calls of differences are made "
        "here for any residue position occuring among the 'Missing Residues' "
        "category for a protein chain.\n")
    '''
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



sys.stderr.write("\n\nThe following residues of chain "+chain1_designation_rep+
    " contribute only to interactions\nwith chain "+chain2_designation_rep+" in "
    +structure1_pdb_code+":")
for i in chain1_res_only_contributing_to_structure1:
    sys.stderr.write("\n"+str(i))

sys.stderr.write("\nThe following residues of chain "+chain1_designation_rep+
    " contribute only to interactions\nwith chain "+chain2_designation_rep+" in "
    +structure2_pdb_code+":")
for i in chain1_res_only_contributing_to_structure2:
    sys.stderr.write("\n"+str(i))

sys.stderr.write("\nThe following residues of chain "+chain2_designation_rep+
    " contribute only to interactions\nwith chain "+chain1_designation_rep+" in "
    +structure1_pdb_code+":")
for i in chain2_res_only_contributing_to_structure1:
    sys.stderr.write("\n"+str(i))

sys.stderr.write("\nThe following residues of chain "+chain2_designation_rep+
    " contribute only to interaction\nwith chain "+chain1_designation_rep+" in "
    +structure2_pdb_code+":")
for i in chain2_res_only_contributing_to_structure2:
    sys.stderr.write("\n"+str(i))




sys.stderr.write("\n\nIf you've previously run the script "
    "`similarities_in_proteinprotein_interactions.py`\nyou received a report "
    "listing residues for each chain that still interact with\nthe other chain "
    "in both structures yet have different sets of residue\npartners in both "
    "structures.\nDetails of the shifts in partners follow.")
sys.stderr.write("\nThe following lists the differing sets of partners for "
    "residues of chain "+chain1_designation_rep+",\nwith the "
    "chain "+chain2_designation_rep+" partners in " +
    structure1_pdb_code+" followed by those in "+structure2_pdb_code+":")
for k,v in chain1_shifts_dict.items():
    sys.stderr.write("\n"+str(k)+": "+str(v[0])+", "+str(v[1]))
sys.stderr.write("\nThe following lists the differing sets of partners for "
    "residues of chain "+chain2_designation_rep+",\nwith the "
    "chain "+chain1_designation_rep+" partners in " +
    structure1_pdb_code+" followed by those in "+structure2_pdb_code+":")
for k,v in chain2_shifts_dict.items():
    sys.stderr.write("\n"+str(k)+": "+str(v[0])+", "+str(v[1]))

#delete the retrieved PDB file that was used to check missing residues.


#######------------------END OF MAIN SECTION------------------------------######
################################################################################
