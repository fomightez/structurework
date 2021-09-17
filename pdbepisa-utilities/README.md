# PISA-utilities

Utility scripts for working with data from [PDBePISA](https://www.ebi.ac.uk/pdbe/pisa/).

A set of Jupyter notebooks that include demonstrations of all these scripts is launchable in active form right in your browser is at my [pdbepisa-binder repo](https://github.com/fomightez/pdbepisa-binder). Just go [there](https://github.com/fomightez/pdbepisa-binder) and click the `launch binder` badge to get started.

Among this set of tools are several meant to facilitate highlighting differences & similarities in protein-protein interactions of the same protein pairs in different, related complexes. For example, several of these scripts aid in highlighting differences & similarities in protein-protein interactions when comparing macromolecular structures solved with different ligands or substrates or when comparing structures that share subsets of the same protein components. 

Be sure to see the 'Related' seciton below, as some of these utility scripts (or the ideas behind them) are also used to layer on structure information to equivalent residues and conservation.


# The scripts

* pisa_interface_list_to_df.py
> Interface list from PDBePISA for chains interacting in a PDB entry --> dataframe of data for use in Python

Takes a PDB accession code or a file name of text copied from a PDBePISA Interface list page and produces a dataframe of the interchain reactions detailing the intraction area for each chain as well as the number & types of interactons.  
**Importantly, it handles protein and nucleic acid interactions whereas PDBsum just summarizes interfaces between proteins in its summary tables of interactions.**

Verified compatible with both Python 2.7 and Python 3.8.

Written to run from command line or pasted/loaded inside a Jupyter notebook cell.  
The main ways to run the script are demonstrated in the notebook ??????????????.ipynb` that can be found when sessions are launched from [here](https://github.com/fomightez/pdbepisa-binder).


Example calls to run the `pisa_interface_list_to_df.py` script from command line:
```
python pisa_interface_list_to_df.py 4fgf
python pisa_interface_list_to_df.py data.txt
```

(Alternatively, upload the script to a Jupyter environment and use `%run python pisa_interface_list_to_df.py 4fgf` in a Python-backed notebook to run the example.)



#### For running in a Jupyter notebook:

To use this script after pasting or loading into a cell in a Jupyter notebook, in the next cell define the URL and then call the main function similar to below:
```
import pdsum_prot_interactions_list_to_df from pdsum_prot_interactions_list_to_df
df =pdsum_prot_interactions_list_to_df('4fgf')
```
See [here](https://github.com/fomightez/pdbepisa-binder for notebooks demonstrating use within a Jupyter notebook; click `launch binder` to launch a session that will allow you to use the notebooks from there.


Related
-------

- The PDBsum has good summaries of data involving all protein chains in structues. See the related series of demo notebooks available at [pdbsum-binder)](https://github.com/fomightez/pdbsum-binder) for demonstration of related notebooks.
