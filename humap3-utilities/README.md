# humap3-utilities

Utility scripts for working with data from hu.MAP 3.0.

A set of Jupyter notebooks that include demonstrations of all these scripts is launchable in active form right in your browser is at my [humap3-binder repo](https://github.com/fomightez/humap3-binder). Just go [there](https://github.com/fomightez/pdbepisa-binder) and click the `launch binder` badge to get started.

Be sure to see the 'Related' section below as well.


# The scripts

* complexes_rawCSV_to_df.py
> raw data csv file ---> Python-based dataframe of raw data on all complexes.

   Pickled dataframe saved as `'raw_complexes_pickled_df.pkl'`. ('pickled' just means stored in a special serialized form easy for Python to access.)  
   The script is meant to be run with`uv` using  `uv run complexes_rawCSV_to_df.py hu.MAP3.0_complexes_wConfidenceScores_total15326_wGenenames_20240922.csv`.

* make_lookup_table_for_extra_info4complexes.py
> dataframe with UniProt identifiers  ---> dictionary
This script is meant to be run in a Jupyter notebook `.ipynb` file where the dataframe containing the identifiers is already defined as `df_expanded` and the identifiers are in the `'Uniprot_ACCs'` column. Use `%run -i make_lookup_table_for_extra_info4complexes.py`.

* modularized code for `Highlight_differences_between_hu.MAP2_and_hu.MAP3_data.ipynb` and `Using_snakemake_to_highlight_differences_between_hu.MAP2_and_hu.MAP3_data_for_multiple_indentifiers.ipynb` in [humap3-binder](https://github.com/fomightez/humap3-binder)
Several scripts are modularized code for the referenced notebooks that won't probbaly be much use elsewhere without refactoring:
   - `two_comp_three_details_plus_table.ipy`
   - `look_for_proteins_going_missing.py`
   - `look_for_majority_complex_member_going_missing.py`

* ???????.py
> Placeholder for example input ---> Placeholder for example result


#### For running in a Jupyter notebook:

To use this script after pasting or loading into a cell in a Jupyter notebook, in the next cell define the URL and then call the main function similar to below:
```
import ?????
df = ?????
```
See [here](https://github.com/fomightez/humap3-binder) for notebooks demonstrating use within a Jupyter notebook; click `launch binder` to launch a session that will allow you to use the notebooks from there.


Related items by me
-------------------
- [My humap3-binder repo](https://github.com/fomightez/humap3-binder)
- [My humap2-binder repo](https://github.com/fomightez/humap3-binder)
- I use the Unipressed package a lot with working with this data, see my [Unipressed-binder repo](https://github.com/fomightez/Unipressed-binder) for more on working with this package.
- The PDBePISA has good summaries of data involving all protein chains in structues. See the related series of demo notebooks available at my repo [pdbepisa-binder](https://github.com/fomightez/pdbepisa-binder) for demonstrations of related scripts (scripts listed [here](https://github.com/fomightez/structurework/tree/master/pdbepisa-utilities)).
- The PDBsum has good summaries of data involving all protein chains in structues. See the related series of demo notebooks available at my repo [pdbsum-binder](https://github.com/fomightez/pdbsum-binder) for demonstration of related scripts (scripts listed [here](https://github.com/fomightez/structurework/tree/master/pdbsum-utilities)).

## Related items by others

???
