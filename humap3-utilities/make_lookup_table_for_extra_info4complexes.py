def make_lookup_table_for_extra_info4complexes(df, column_with_identifiers):
    '''
    Takes a dataframe and the column with the UniProt identifiers and looks
    up extra information about the protein/genes associated with identifier.
    Uses Unipressed package to look up the information.

    Returns a dictionary with the details.
    '''
    lookup_dict = {}
    accs = set(df[column_with_identifiers].to_list())
    from unipressed import UniprotkbClient
    import time
    for acc in accs:
        if 'SPECIAL_' in acc: # adds handling for those like `SPECIAL_HGNC12413` and `SPECIAL_HLA-A-related` that are in standardized hu.MAP 2.0 data (This way I can use the same function for both version 2.0 and version 3.0 data)
            uniprot_record = " "
            protein_name = f"{acc}_protein"
        else:
            uniprot_record = UniprotkbClient.fetch_one(acc)
            protein_name = uniprot_record['proteinDescription']['recommendedName']['fullName']['value']
            '''
            def safe_get_disease_id(comment):
                try:
                    return comment['disease']['diseaseId']
                except KeyError:
                    return comment.get('disease', {}).get('diseaseId', 'Unknown disease ID')
            
            disease_info_list = [
                safe_get_disease_id(comment)
                for comment in uniprot_record['comments']
                if comment['commentType'] == 'DISEASE'
            ]
            
            if not disease_info_list:
                disease_info_list = ['None reported']
            '''
        disease_info_list = []
        synonyms_info_list =[]
        if 'comments' in uniprot_record:
            for comment in uniprot_record['comments']:
                if comment['commentType'] == 'DISEASE':
                    disease_info = comment.get('disease', {})
                    disease_id = disease_info.get('diseaseId', 'Unknown disease ID')
                    disease_info_list.append(disease_id)
        if 'genes' in uniprot_record:
            if uniprot_record['genes']:
                for i in uniprot_record['genes']:
                    if 'synonyms' in i:
                        for s in i['synonyms']:
                            synonyms_info_list.append(s['value'])
        if not disease_info_list:
            disease_info_list = ['None reported']
        disease_info = '; '.join(disease_info_list[:2])
        if not synonyms_info_list:
            synonyms_info_list = ['None reported']
        disease_info = '; '.join(disease_info_list[:2])
        synonyms_info = '; '.join(synonyms_info_list)
        lookup_dict[acc] = {'protein_name':protein_name, 'disease': disease_info, 'synonyms': synonyms_info}
        time.sleep(1.1) # don't slam the API
    return lookup_dict
lookup_dict = make_lookup_table_for_extra_info4complexes(df_expanded,'Uniprot_ACCs')
