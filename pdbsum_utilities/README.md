# PDBsum-utilities

Utility scripts for working with data from [PDBsum](http://www.ebi.ac.uk/thornton-srv/databases/cgi-bin/pdbsum/GetPage.pl?pdbcode=index.html).

Associated demonstrations launchable in active form right in your browser available at my [pdbsum-binder](https://github.com/fomightez/pdbsum-binder).

Among this set of tools are several meant to facilitate highlighting differences & similarities in protein-protein interactions of the same protein pairs in different, related complexes. For example, several of these scripts aid in highlighting differences & similarities in protein-protein interactions when comparing macromolecular structures solved with different ligands or substrates or when comparing structures that share subsets of the same protein components. 

Note to self: **MENTION AS COMMENT at https://www.biostars.org/p/11880/#12024 WHEN ADD SOME CONTENT HERE**

# The scripts

* pdsum_prot_interactions_list_to_df.py
> PDBsum data for protein-protein interactions --> dataframe of data for use in Python

Takes PDBsum data for protein-protein interactions and makes a dataframe from it for use with Python.

Verified compatible with both Python 2.7 and Python 3.8.

Written to run from command line or pasted/loaded inside a Jupyter notebook cell.  
The main ways to run the script are demonstrated in the notebook `Working with PDBsum in Jupyter Basics.ipynb` that can be found when sessions are launched from [here](https://github.com/fomightez/pdbsum-binder).


Example calls to run the `xxxxx.py` script from command line:
```
python pdsum_prot_interactions_list_to_df.py data.txt
```

(Alternatively, upload the script to a Jupyter environment and use `%run pdsum_prot_interactions_list_to_df.py data.txt` in a Python-backed notebook to run the example.)



#### For running in a Jupyter notebook:

To use this script after pasting or loading into a cell in a Jupyter notebook, in the next cell define the URL and then call the main function similar to below:
```
import pdsum_prot_interactions_list_to_df from pdsum_prot_interactions_list_to_df
df =pdsum_prot_interactions_list_to_df('data.txt')
```
See [here](https://github.com/fomightez/pdbsum-binder) for notebooks demonstrating use within a Jupyter notebook; click `launch binder` to launch a session that will allow you to use the notebooks from there.


Related
-------

- ?
