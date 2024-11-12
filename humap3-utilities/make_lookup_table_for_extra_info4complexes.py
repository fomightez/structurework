lookup_dict = {}
accs = set(df_expanded['Uniprot_ACCs'].to_list())
from unipressed import UniprotkbClient
import time
for acc in accs:
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
    if 'comments' in uniprot_record:
        for comment in uniprot_record['comments']:
            if comment['commentType'] == 'DISEASE':
                disease_info = comment.get('disease', {})
                disease_id = disease_info.get('diseaseId', 'Unknown disease ID')
                disease_info_list.append(disease_id)
    if not disease_info_list:
        disease_info_list = ['None reported']
    disease_info = '; '.join(disease_info_list[:2])
    lookup_dict[acc] = {'protein_name':protein_name, 'disease': disease_info}
    time.sleep(1.1) # don't slam the API
