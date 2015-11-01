#! /usr/bin/env python

# merge_multi_PDBs_into_single_file by Wayne Decatur
# ver 0.1
#
# fuse_pdbs function code from Claudia Millan Nebot
#
# To GET HELP/MANUAL, enter on command line:
# python merge_multi_PDBs_into_single_file.py --help
#
#*************************************************************************
# USES Python 2.7
#
# DEPENDENCIES:
# Biopython and other typical modules like argparse, os
#
# Purpose: Takes a directory containing structures in the PDB format and
# combines them all into a single PDB file with each structure as an individual
# model.
#
#
# v.0.1.
# To do: make so can specify order by putting a number after underscore in front
# of the `.pdb` suffix
# How do we add "End" to end of file but no in middle?
# How do we get so it doesn't add Model 0 since that has special all treatment in Jmol, see http://www.bioinformatics.org/pipermail/molvis-list/2007q2/000427.html ( or has this been fixed?)
#
#
# TO RUN:
# For example, when in the directory containing the directory with the PDB files
# `DIRECTORYcontainingPDBs`, enter on the command line, the line
#-----------------------------------
# python merge_multi_PDBs_into_single_file.py DIRECTORYcontainingPDBs
#-----------------------------------
# to generate the file named'DIRECTORYcontainingPDBs.pdb' in your working
# directory.
#
# Meaning that you can point it at a directory and then it will process
# all the files ending in '.pdb' or '.PDB' in that folder.
#
#*************************************************************************












#*************************************************************************
#*************************************************************************
###DO NOT EDIT BELOW HERE - ENTER VALUES ABOVE###
import os
import sys
from stat import *
#from urllib import urlopen
import logging
import argparse
from argparse import RawTextHelpFormatter
from Bio.PDB import *

#DEBUG CONTROL
#comment line below to turn off debug print statements
#logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)





#argparser from http://docs.python.org/2/library/argparse.html#module-argparse and http://docs.python.org/2/howto/argparse.html#id1
parser = argparse.ArgumentParser(prog='merge_multi_PDBs_into_single_file.py',description="merge_multi_PDBs_into_single_file is a program that takes\nstructures in the PDB format and combines them all into\na single PDB file with each structure as an individual model.\n \nWritten by Wayne Decatur --> Fomightez @ Github or Twitter. \n\n\nActual example what to enter on command line to run program:\npython merge_multi_PDBs_into_single_file DIRECTORYcontainingPDBs", formatter_class=RawTextHelpFormatter)
#learned how to control line breaks in description above from http://stackoverflow.com/questions/3853722/python-argparse-how-to-insert-newline-the-help-text
#DANG THOUGH THE 'RawTextHelpFormatter' setting seems to apply to all the text then. Not really what I wanted.
parser.add_argument("Directory", help="directory containing PDB files to merge into single file. REQUIRED.")
#I would also like trigger help to display if no arguments provided because need at least a directory
if len(sys.argv)==1:    #from http://stackoverflow.com/questions/4042452/display-help-message-with-python-argparse-when-script-is-called-without-any-argu
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()



###---------------------------HELPER FUNCTIONS---------------------------------###


def fuse_pdbs(list_of_filepaths,current_path):
    '''
    function written by Claudia Millan Nebot

    The function takes as input a list of filepaths for several individual PDB
    files and combines them into a single file that is saved as path_pdb, where
    the path portion of the name specifies the directory to save the file.
    '''
    list_of_structures=[]
    parser=PDBParser()
    for pdb_file in list_of_filepaths:
        structure=parser.get_structure(pdb_file[:-4],pdb_file)
        list_of_structures.append(structure)
    main_structure=list_of_structures[0]
    for x,structure in enumerate(list_of_structures):
        #print "Processing ",structure," ",x
        model=structure[0]
        if x!=0:
            model.id=x
            model.serial_num=x
            main_structure.add(model)
    #print Selection.unfold_entities(main_structure,'M')
    io=PDBIO()
    io.set_structure(main_structure)
    io.save(current_path,write_end=False)
    sys.stderr.write("The PDB-formatted file "+current_path+" has been created.\n")

###--------------------------END OF HELPER FUNCTIONS---------------------------###






###----------------------MAIN PART OF SCRIPT--------------------------------###
current_path = str(args.Directory) + ".pdb"
list_of_filepaths_for_PDB_files = []

# If provided argument is a DIRECTORY loop through collecting information on
# each PDB file.
#from http://stackoverflow.com/questions/3204782/how-to-check-if-a-file-is-a-directory-or-regular-file-in-python
if os.path.isfile(args.Directory):
    sys.stderr.write("\n***ERROR ********************ERROR ***************** \n")
    sys.stderr.write("Oops! You only provided a single file.\n This program is for merging multiple structures PDB file format into one.\n This file already exists as a single file.")
    sys.stderr.write("***ERROR ********************ERROR ***************** \n \n")
elif os.path.isdir(args.Directory):
    for f in os.listdir(args.Directory):
        pathname = os.path.join(args.Directory, f)
        #FOR DEBUGGING
        logging.debug(pathname)
        mode = os.stat(pathname).st_mode
        if S_ISREG(mode) and pathname[-4:].upper() == ".PDB":
            # It's a PDB file, collect the path and file name info
            list_of_filepaths_for_PDB_files.append(pathname)


#Now that the name and path info on each PDB file has been collected, extract
#the data from each and merge into one
fuse_pdbs(list_of_filepaths_for_PDB_files,current_path)
