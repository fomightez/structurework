# This uses uv to run. First install `uv` with `pip install uv` then run `!uv run complexes_rawCSV_to_df.py hu.MAP3.0_complexes_wConfidenceScores_total15326_wGenenames_20240922.csv`
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "numpy",
#   "pandas",
#   "rich",
# ]
# ///

import sys
try:
    file = sys.argv[1]
except IndexError:
    import rich
    rich.print("\n[bold red]I suspect you forgot to specify the file to read?[/bold red]\n Perhaps try the following:\n [bold black]!uv run complexes_rawCSV_to_df.py hu.MAP3.0_complexes_wConfidenceScores_total15326_wGenenames_20240922.csv[/bold black]\n[bold red]**EXITING !!**[/bold red]\n"); sys.exit(1)
import pandas as pd
df = pd.read_csv(file)
#print(df.head()) # for debugging
df.to_pickle('raw_complexes_pickled_df.pkl')
