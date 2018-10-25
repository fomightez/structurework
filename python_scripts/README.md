# Structure work scripts

Python scripts by Wayne Decatur for working with biological structure data.

- multiple_model_PDB_file_splitter.py

>Takes a formatted pdb file with multiple models and splits each model into individual files. You specify the file with multiple models in the call to the program.

>  Note that you can also you can also point it at a directory and then it will process all the files ending in '.pdb' or '.PDB' in that folder, similar to the `-r`, recursive, option in many Bash commands.

>An example of a program that makes a PDB-fromatted multi-model file is RNA composer at http://rnacomposer.ibch.poznan.pl/Home .

There is a [demo of this script within the 'Split and Combine multimodel PDB files' notebook launchable in this repo](https://github.com/fomightez/cl_demo-binder); the specific section can be viewed nicely displayed [here](https://nbviewer.jupyter.org/github/fomightez/cl_demo-binder/blob/master/cl_demo-binder%20split%20and%20combine%20multimodel%20PDB%20files.ipynb#Python-script-method-to-split).

#### Limitations
Requires the PDB file include both MODEL and ENDMDL records for each of the models.

#### Dependencies and version compatibility  
Nothing but the fairly standard modules such as os, sys, and argparse.  
Originally developed in Python 2.7, but confirmed to work in Python 3.6.


##### EXAMPLE RUN

TO RUN:
Enter on the command line, the line

	python multiple_model_PDB_file_splitter.py ensemble.pdb

or

	python multiple_model_PDB_file_splitter.py directory/

where `ensemble.pdb` is the name of the file containing multiple PDB structure models, or `directory` is the name of a directory containing files ending in `.pdb` or `.PDB` to split.


There is a [demo of this script within the 'Split and Combine multimodel PDB files' notebook launchable in this repo](https://github.com/fomightez/cl_demo-binder); the specific section can be viewed nicely displayed [here](https://nbviewer.jupyter.org/github/fomightez/cl_demo-binder/blob/master/cl_demo-binder%20split%20and%20combine%20multimodel%20PDB%20files.ipynb#Python-script-method-to-split).

----



- super_basic_multiple_model_PDB_file_splitter.py

>Takes a formatted pdb file with multiple models and splits each model into individual files. Unlike, `multiple_model_PDB_file_splitter.py` you have to edit the code of the script to actually contain the text of the file to split. Copy and paste it into the `PDB_text` value in the script.  See `multiple_model_PDB_file_splitter.py` if you want a script you just want to specify the file to split on the command line when you call the script.

>An example of a program that makes a PDB-fromatted multi-model file is RNA composer at http://rnacomposer.ibch.poznan.pl/Home .

There is a [demo of this script within the 'Split and Combine multimodel PDB files' notebook launchable in this repo](https://github.com/fomightez/cl_demo-binder); the specific section can be viewed nicely displayed [here](https://nbviewer.jupyter.org/github/fomightez/cl_demo-binder/blob/master/cl_demo-binder%20split%20and%20combine%20multimodel%20PDB%20files.ipynb#Basic-Python-method-to-split).

#### Limitations
Requires the PDB file include both MODEL and ENDMDL records for each of the models.

#### Dependencies and version compatibility
None at all.  
Originally developed in Python 2.7, but confirmed to work in Python 3.6.


##### EXAMPLE RUN

TO RUN:
Enter on the command line, the line

	python super_basic_multiple_model_PDB_file_splitter.py ensemble.pdb

where `ensemble.pdb` is the name of the file containing multiple PDB structure models. You'll need to edit the `PDB_text` value to be the text of the pdb file you wish to split up.


There is a [demo of this script within the 'Split and Combine multimodel PDB files' notebook launchable in this repo](https://github.com/fomightez/cl_demo-binder); the specific section can be viewed nicely displayed [here](https://nbviewer.jupyter.org/github/fomightez/cl_demo-binder/blob/master/cl_demo-binder%20split%20and%20combine%20multimodel%20PDB%20files.ipynb#Basic-Python-method-to-split).

----


- merge_multi_PDBs_into_single_file.py

>Takes a directory containing structures in the PDB format and combines them all into a single PDB file with each structure as an individual model.

There is a [demo of this script within the 'Split and Combine multimodel PDB files' notebook launchable in this repo](https://github.com/fomightez/cl_demo-binder); the specific section can be viewed nicely displayed [here](https://nbviewer.jupyter.org/github/fomightez/cl_demo-binder/blob/master/cl_demo-binder%20split%20and%20combine%20multimodel%20PDB%20files.ipynb#Python-script-method-to-merge).


#### Limitations
For now the merged file will not have have `END` at the end like most multi-model PDB files. It seems that everything but the cutting-edge unrealeased Biopython had a bug that caused `END` to be placed after every model upon appending.

The files to be merged need are specified by the ones that end in '.pdb' or '.PDB' in the specified directory.

#### Dependencies
Biopython and the fairly standard modules such as os, sys, and argparse. Written in Python 2.7.


##### EXAMPLE RUN

TO RUN:
Navigate to the directory above a folder containing several PDBs you wish to combine as model. Enter on the command line, the line

	python merge_multi_PDBs_into_single_file.pyensemble.pdb directory_of_pdbs

where `directory_of_pdbs` is the name of the directory containing several PDBs you wish to combine as model.

#### Advanced Options
The default numbering for first model is 1 and not zero. Since `model 0` has special meaning as select all models in Jmol as described at http://www.bioinformatics.org/pipermail/molvis-list/2007q2/000427.html .  By providing a whole number following the `--initial` flag when calling the program you can specify any value for numbering first model in the sequence of models.
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

Another example with the advanced options, in this case the `--initial` flag that can be abbreviated as `-i`, invoking the program to run with

	python merge_multi_PDBs_into_single_file.py test_folder -i 3

, if `test_folder` contains

- `1crn_3.pdb`
- `1tup_5.pdb`
- `1ehz_7.pdb`

, the final file will have three models

- model #3 1crn
- model #4 1tup
- model #5 1ehz.

#### Demo

There is a [demo of this script within the 'Split and Combine multimodel PDB files' notebook launchable in this repo](https://github.com/fomightez/cl_demo-binder); the specific section can be viewed nicely displayed [here](https://nbviewer.jupyter.org/github/fomightez/cl_demo-binder/blob/master/cl_demo-binder%20split%20and%20combine%20multimodel%20PDB%20files.ipynb#Python-script-method-to-merge).

----


Also see
--------
* [a gist](https://gist.github.com/fomightez/2601c0f5a13b85cd21b9377169c79836) I forked from [Joao Rodrigues](https://gist.github.com/JoaoRodrigues/e3a4f2139d10888c679eb1657a4d7080) for aligning structures using Biopython. See [here](http://thread.gmane.org/gmane.comp.python.bio.general/8782/focus=8783) about it.


Related
--------

see [Dockerfiles for Structural Analysis (Structural Bioinformatics) Docker images](https://github.com/fomightez/Dockerfiles#dockerfiles-for-structural-analysis-structural-bioinformatics-docker-images).

Related resources by others
--------

- [atomium](https://github.com/samirelanduk/atomium) is a Python library for opening and saving .pdb, .cif and .xyz files, and presenting and manipulating the information contained within. Documentation is at https://atomium.samireland.com/ .

- [Biopandas](https://github.com/rasbt/biopandas) for working with molecular structures in pandas DataFrames. Documentation at http://rasbt.github.io/biopandas/.

-  [Bio3D](https://github.com/fomightez/bio3d-binder), an R package for the analysis of macromolecular structure, sequence and trajectory data. (***R- and not Python-based, but definitely related***).
