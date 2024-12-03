# Also make sure nothing that is in the majority of complexes in hu.MAP 2.0 data disappears entirely from hu.MAP 3.0 data.
# That can only occur as the case if `something_dropped_completely`, that we've already check on, is True
majority_item_dropped_completely = False #set up by declaring false
if something_dropped_completely:
    # collect information on what identifiers occur in the majority of complexes in hu.MAP 2.0 data
    # the search term should always be present and can thus serve as a sanity check for this collection
    majority_identifiers = []
    def find_majority_uniprot_accs(df):
        # Group by HuMAP2_ID and get unique Uniprot_ACCs for each complex
        complex_accs = df.groupby('HuMAP2_ID')['Uniprot_ACCs'].unique()
        
        # Count total number of unique complexes
        total_complexes = len(complex_accs)
        
        # Flatten and count occurrences of each Uniprot ACC across complexes
        all_accs = df['Uniprot_ACCs'].tolist()
        acc_counts = pd.Series(all_accs).value_counts()
        
        # Find ACCs that appear in more than 50% of complexes
        majority_accs = acc_counts[acc_counts >= 0.51 * total_complexes].index.tolist()
        
        return majority_accs
    if find_majority_uniprot_accs(df2_expanded):
        majority_identifiers = find_majority_uniprot_accs(df2_expanded)
    # Now check none of those `majority_identifiers` match the disappearing ones dropped completely
    print("\nHu.MAP2.0-Majority Complex Members Disappearing in Hu.MAP3.0 data:")
    for item in list(set.union(*disappearing_df['lost_items'])): # note `list(set.union(*disappearing_df['lost_items']))` gets the unique set members from the 'lost_items' column
        if item in majority_identifiers:
            majority_item_dropped_completely = (item not in df3_expanded['Uniprot_ACCs'].to_list())
            if majority_item_dropped_completely:
                total_complexes = len(df2_expanded.groupby('HuMAP2_ID')['Uniprot_ACCs'].unique())
                all_accs = df2_expanded['Uniprot_ACCs'].tolist()
                acc_counts = pd.Series(all_accs).value_counts()
                acc_counts_dict = acc_counts.to_dict()
                print(f"  - {item} IS IN MAJORITY OF Hu.MAP2.0 COMPLEXES ({acc_counts_dict[item]} of {total_complexes}) YET NOT IN ANY Hu.MAP3.0 {search_term}-complexes!!! (PERHAPS CONCERNING?)")
                majority_item_dropped_completely = True
    if majority_item_dropped_completely == False:
        print("NONE")
