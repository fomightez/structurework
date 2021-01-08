# PDBsum-utilities

Utility scripts for working with data from [PDBsum](http://www.ebi.ac.uk/thornton-srv/databases/cgi-bin/pdbsum/GetPage.pl?pdbcode=index.html).

# The scripts

* xxxxx.py
> xxxxx data --> dataframe of data for use in Python

Takes xxxx and makes a dataframe from it for use with Python.

Verified compatible with both Python 2.7 and Python 3.8.

Written to run from command line or pasted/loaded inside a Jupyter notebook cell.  
The main ways to run the script are demonstrated in xxxxxx


Alternatively, you can use the HHpred webserver to make these result files using your favorite web browser. For example, go to [HHpred site here](https://toolkit.tuebingen.mpg.de/tools/hhpred) and paste in a protein sequence. Feel free to adjust the search options if you'd like before hitting the 'Submit' button in the bottom right. After the submitted job finishes, from the 'Results' tab, you can select 'Download HHR' to retrieve a HH-suite3 results file in `.hhr` format to your local machine. You can upload that to a running session launched from [here](https://github.com/fomightez/hhsuite3-binder) and edit some of the examples in the series of notebooks there to use the hhsuite3_results_to_df.py script on your data present in your downloaded `.hhr` file.


Example calls to run the `xxxxx.py` script from command line:
```
python xxxxx.py xxxxxxx
```

(Alternatively, upload the script to a Jupyter environment and use `%run xxxxxxx.py xxxxxx` in a Python-backed notebook to run the example.)



#### For running in a Jupyter notebook:

To use this script after pasting or loading into a cell in a Jupyter notebook, in the next cell define the URL and then call the main function similar to below:
```
df =xxxxx("xxxxx")
```
See [here](xxxxxx) for notebooks demonstrating use within a Jupyter notebook; click `launch binder` to launch a session that will allow you to use the notebooks from there.


Related
-------

- ?
