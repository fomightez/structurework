#Structure work scripts

Python scripts by Wayne Decatur for working with biological structure data.

- multiple_model_PDB_file_splitter.py

>Takes a formatted pdb file with multiple models and splits each model into individual files. You designate the file with multiple models in the call to the program.

>An example of a program that makes a PDB-fromatted multi-model file is RNA composer at http://rnacomposer.ibch.poznan.pl/Home .


####Limitations
Requires the PDB file include both MODEL and ENDMDL
# records for each of the models.

####Dependencies
Nothing but the fairly standard modules such as os, sys, and argparse. Written in Python 2.7.


####Example of input and output for multiple_model_PDB_file_splitter.py:
##### EXAMPLE RUN

TO RUN:
Enter on the command line, the line

	python multiple_model_PDB_file_splitter.py ensemble.pdb

where `ensemble.pdb` is the name of the file containing multiple PDB structure models.





- super_basic_multiple_model_PDB_file_splitter.py

>Takes a formatted pdb file with multiple models and splits each model into individual files. Unlike, `multiple_model_PDB_file_splitter.py` you have to edit the code of the script to actually contain the text of the file to split. Copy and paste it into the `PDB_text` value in the script.  See `multiple_model_PDB_file_splitter.py` if you want a script you just want to specify the file to split on the command line when you call the script.

>An example of a program that makes a PDB-fromatted multi-model file is RNA composer at http://rnacomposer.ibch.poznan.pl/Home .


####Limitations
Requires the PDB file include both MODEL and ENDMDL
# records for each of the models.

####Dependencies
None at all. Written in Python 2.7.


####Example of input and output for super_basic_multiple_model_PDB_file_splitter.py:
##### EXAMPLE RUN

TO RUN:
Enter on the command line, the line

	python super_basic_multiple_model_PDB_file_splitter.py ensemble.pdb

where `ensemble.pdb` is the name of the file containing multiple PDB structure models. You'll need to edit the `PDB_text` value to be the text of the pdb file you wish to split up.
