#Structure work scripts

Python scripts by Wayne Decatur for working with biological structure data.

- multiple_model_PDB_file_splitter.py

>Takes a formatted pdb file with multiple models and splits each model into individual files. You specify the file with multiple models in the call to the program.

>An example of a program that makes a PDB-fromatted multi-model file is RNA composer at http://rnacomposer.ibch.poznan.pl/Home .


####Limitations
Requires the PDB file include both MODEL and ENDMDL records for each of the models.

####Dependencies
Nothing but the fairly standard modules such as os, sys, and argparse. Written in Python 2.7.


##### EXAMPLE RUN

TO RUN:
Enter on the command line, the line

	python multiple_model_PDB_file_splitter.py ensemble.pdb

where `ensemble.pdb` is the name of the file containing multiple PDB structure models.



# ---------------------------------------------------



- super_basic_multiple_model_PDB_file_splitter.py

>Takes a formatted pdb file with multiple models and splits each model into individual files. Unlike, `multiple_model_PDB_file_splitter.py` you have to edit the code of the script to actually contain the text of the file to split. Copy and paste it into the `PDB_text` value in the script.  See `multiple_model_PDB_file_splitter.py` if you want a script you just want to specify the file to split on the command line when you call the script.

>An example of a program that makes a PDB-fromatted multi-model file is RNA composer at http://rnacomposer.ibch.poznan.pl/Home .


####Limitations
Requires the PDB file include both MODEL and ENDMDL records for each of the models.

####Dependencies
None at all. Written in Python 2.7.


##### EXAMPLE RUN

TO RUN:
Enter on the command line, the line

	python super_basic_multiple_model_PDB_file_splitter.py ensemble.pdb

where `ensemble.pdb` is the name of the file containing multiple PDB structure models. You'll need to edit the `PDB_text` value to be the text of the pdb file you wish to split up.


# ---------------------------------------------------


- merge_multi_PDBs_into_single_file.py

>Takes a directory containing structures in the PDB format and combines them all into a single PDB file with each structure as an individual model.


####Limitations
For now the merged file will not have have `END` at the end like most multi-model PDB files. It seems that everything but the cutting-edge unrealeased Biopython had a bug that caused `END` to be placed after every model upon appending.

####Dependencies
Biopython and the fairly standard modules such as os, sys, and argparse. Written in Python 2.7.


##### EXAMPLE RUN

TO RUN:
Navigate to the directory above a folder containing several PDBs you wish to combine as model. Enter on the command line, the line

	python merge_multi_PDBs_into_single_file.pyensemble.pdb directory_of_pdbs

where `directory_of_pdbs` is the name of the directory containing several PDBs you wish to combine as model.

####Advanced Options
The default numbering for first model is 1 and not zero. Since `model 0` has special meaning as select all models in Jmol as described at http://www.bioinformatics.org/pipermail/molvis-list/2007q2/000427.html .  By providing a whole number following the '--initial' flag when calling the programyou can specify any value for numbering first model in the sequence of models.
<br>
There is mechanism where you can specify an order of models within final file by putting a whole number after underscore in front of the `.pdb` suffix. If every PDB file in the directory follows that pattern, the ascending order of those numbers will be used to sequence the models in the produced file The specific number used after the underscore is disregarded when numbering the models; you still need to provide the initial number for the models if you want anything other than 1 and the numbering will be incremented automatically.
<br>
For example, calling the program to run with

python merge_multi_PDBs_into_single_file.py test_folder

, if `test_folder` contains

- `1crn_3.pdb`
- `1tup_5.pdb`
- `1ehz_7.pdb`

, the final file will have three models

- model #1 1crn
- model #2 1tup
- model #3 1ehz.

Another example with the advanced options, invoking the program to run with

	python merge_multi_PDBs_into_single_file.py test_folder -i 3

, if `test_folder` contains

- `1crn_3.pdb`
- `1tup_5.pdb`
- `1ehz_7.pdb`

, the final file will have three models

- model #3 1crn
- model #4 1tup
- model #5 1ehz.

# ---------------------------------------------------
