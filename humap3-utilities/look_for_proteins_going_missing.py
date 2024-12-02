# Make sure nothing present in HuMAP2 data disappeared in huMAP3 data
# Function to compare UniProt ACCs between HuMAP2 and HuMAP3
def check_disappearing_items(df_correspondences, df2_expanded, df3_expanded):
    # Tracking disappearing items
    disappearing_items = []
    
    for _, correspondence in df_correspondences.iterrows():
        humap2_id = correspondence['HuMAP2_ID']
        humap3_id = correspondence['HuMAP3_ID']
        
        # Get UniProt ACCs for this HuMAP2 group
        humap2_accs = set(df2_expanded[df2_expanded['HuMAP2_ID'] == humap2_id]['Uniprot_ACCs'])
        
        # Get UniProt ACCs for this HuMAP3 group
        humap3_accs = set(df3_expanded[df3_expanded['HuMAP3_ID'] == humap3_id]['Uniprot_ACCs'])
        
        # Find items in HuMAP2 that are not in HuMAP3
        lost_items = humap2_accs - humap3_accs
        
        if lost_items:
            disappearing_items.append({
                'HuMAP2_ID': humap2_id,
                'HuMAP3_ID': humap3_id,
                'lost_items': lost_items,
                'total_humap2_items': len(humap2_accs),
                'total_humap3_items': len(humap3_accs),
                'percent_lost': len(lost_items) / len(humap2_accs) * 100 if humap2_accs else 0
            })
    
    # Convert to DataFrame for easy analysis
    df_disappearing = pd.DataFrame(disappearing_items)
    
    # Display results
    global something_dropped_completely
    something_dropped_completely = False
    if not df_disappearing.empty:
        print("\nDisappearing Items between Hu.MAP2.0 and Hu.MAP3.0 data:")
        for _, row in df_disappearing.iterrows():
            print(f"\nHuMAP2 ID: {row['HuMAP2_ID']} -> HuMAP3 ID: {row['HuMAP3_ID']}")
            print(f"Total items in HuMAP2: {row['total_humap2_items']}")
            print(f"Total items in HuMAP3: {row['total_humap3_items']}")
            print(f"Percent of items lost: {row['percent_lost']:.2f}%")
            print("UniProt ACCs Lost From Corresponding Complex:")
            for item in row['lost_items']:
                dropped_completely = (item not in df3_expanded['Uniprot_ACCs'].to_list())
                if dropped_completely:
                    print(f"  - {item} (AND NOT IN ANY OTHER Hu.MAP3.0 {search_term}-complexes!!!)")
                    something_dropped_completely = True
                else:
                    print(f"  - {item} (But present in other, {search_term}-related Hu.MAP3.0 complexes)")
        
        # Optional: Save to CSV
        df_disappearing.to_csv('disappearing_items.csv', index=False)
        
        return df_disappearing, something_dropped_completely
    else:
        print("\nNo disappearing items found between HuMAP2 and HuMAP3.")
        return None, something_dropped_completely

# Call the function
disappearing_df, something_dropped_completely = check_disappearing_items(df_correspondences, df2_expanded, df3_expanded)
