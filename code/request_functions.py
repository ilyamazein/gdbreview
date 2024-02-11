import requests
import json
import pandas as pd

def metadata_by_id(db, id_list):
    
    '''
    A function that downloads publication metadata by its internal database ID.
    It also parses publication IDs such as DOI and adds them to the metadata dictionary as separate entities.
    
    Takes in the following parameters:
    db: a string, the name of the required database ('pmc' or 'pubmed')
    id_list: a list of IDs pointing to the required publications in the database
    
    Returns a list of dictionaries, containing publication metadata.
    '''
        
    data_list = []

    data_request = (
        'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db='
        + db
        + '&retmode=json&id='
    )

    ids = ','.join(id_list)
    data_request += ids
    data_result = requests.get(data_request)
    data_result_json = json.loads(data_result.text)

    for j in list(data_result_json['result'].keys())[1:]:

        temp_dict = data_result_json['result'][j]

        if 'articleids' in temp_dict.keys():
            for k in temp_dict['articleids']:

                temp_articleid = k['idtype']
                temp_articleid_value = k['value']

                temp_dict[temp_articleid] = temp_articleid_value

            data_list.append(temp_dict)

    return data_list


def pub_met(query, database, max_date, batch_size):

    '''
    A function that downloads metadata of publications returned by the given database query.
    To do so it extracts all internal database IDs for publications returned by the query,
    and passes them to the metadata_by_id function.
    
    Takes in the following parameters:
    query: a string, the required database query
    database: a string, the name of the required database ('pmc' or 'pubmed'),
    max_date: a string in the format 'YYYY/MM/DD', the cut-off publication date
    batch_size: an integer specifying the batch size of IDs passed to the metadata_by_id function
    
    Returns a dataframe containing publication metadata.
    '''

    query = '+'.join(query.split(' '))

    db_id_request = (
        'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db='
        + database
        + '&retmode=json&retmax=100000&term='
    )

    db_id_request += query.strip('\n')
    db_id_request += (
        '&datetype=pdat&mindate=1000%2F01%2F01&maxdate=' + max_date.replace('/', '%2F')
    )
    db_id_result = requests.get(db_id_request)
    db_id_result_json = json.loads(db_id_result.text)

    db_id_list = db_id_result_json['esearchresult']['idlist']

    db_data_list = []
    iteration = batch_size

    for i in range(len(db_id_list) // iteration):
        db_data_list += metadata_by_id(
            database, db_id_list[i * iteration : (i + 1) * iteration]
        )

    db_data_list += metadata_by_id(
        database, db_id_list[(len(db_id_list) // iteration) * iteration :]
    )

    db_df = pd.DataFrame(db_data_list)

    return db_df
