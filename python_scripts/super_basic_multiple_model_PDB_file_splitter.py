#! /usr/bin/env python

# super_basic_multiple_model_PDB_file_splitter.py by Wayne Decatur
# ver 0.1
#
#*******************************************************************************
# USES Python 2.7
# PURPOSE: Takes a formatted pdb file with multiple models and splits each model
# into individual files. Requires the PDB file include both MODEL and ENDMDL
# records for each of the models.
#
# Dependencies:
#
#
# v.0.1. Started
#
# INSPIRED by: general need to have something to obviate my need to do this by
# hand and code at
# 'Split NMR-style multiple model pdb files into individual models' at
# http://strucbio.biologie.uni-konstanz.de/ccp4wiki/index.php/Split_NMR-style_multiple_model_pdb_files_into_individual_models
#
#
#
# TO RUN:
# First, open this as a text file and place your PDB text below where it says
# PDB_text below.
# Next, enter on the command line of your terminal, the line
#-----------------------------------
# python super_basic_multiple_model_PDB_file_splitter.py
#-----------------------------------
# or run in your favorite IDE, such as IDLE or Canopy.
#
#
#
#
#*******************************************************************************
##################################
#  USER ADJUSTABLE VALUES        #

##################################
#
PDB_text = '''
PASTE YOUR PDB FILE TEXT HERE
'''
#
#*******************************************************************************
#**********************END USER ADJUSTABLE VARIABLES****************************



###-*************************Main portion of script*************************-###
model_number = 1
new_file_text = ""
for line in filter(None, PDB_text.splitlines()):
    line = line.strip () #for better control of ends of lines
    if line == "ENDMDL":
        # save file with file number in name
        output_file = open("model_" + str(model_number) + ".pdb", "w")
        output_file.write(new_file_text.rstrip('\r\n')) #rstrip to remove trailing newline
        # from http://stackoverflow.com/questions/275018/how-can-i-remove-chomp-a-newline-in-python
        output_file.close()
        # reset everything for next model
        model_number += 1
        new_file_text = ""
    elif not line.startswith("MODEL"):
        new_file_text += line + '\n'
###-***********************END MAIN PORTION OF SCRIPT***********************-###
#*******************************************************************************
