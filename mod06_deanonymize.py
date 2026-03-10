import pandas as pd

def load_data(anonymized_path, auxiliary_path):
    """
    Load anonymized and auxiliary datasets.
    """
    anon = pd.read_csv(anonymized_path)
    aux = pd.read_csv(auxiliary_path)
    return anon, aux
 

def link_records(anon_df, aux_df):
    """
    Attempt to link anonymized records to auxiliary records
    using exact matching on quasi-identifiers.

    Returns a DataFrame with columns:
      anon_id, matched_name
    containing ONLY uniquely matched records.
    """
    #big_copy = aud

    #containing ONLY uniquely matched records.

    big_anon = anon_df.copy()
    big_aux = aux_df.copy()

    big_aux.columns = ['matched_name', 'age', 'zip3', 'gender']


    IDs_matched = pd.merge(big_anon, big_aux, on=['age', 'zip3', 'gender'], how='inner')

    all_found = IDs_matched['anon_id'].value_counts()

    only_one_match = []

    for id_val, pair in all_found.items():
        if (1 == pair):
            only_one_match.append(id_val)


    saved_unique = []

    for idx, where_in_data in IDs_matched.iterrows():
        if where_in_data['anon_id'] in only_one_match:
            final_r = {
                'anon_id' : where_in_data['anon_id'],
                'matched_name': where_in_data['matched_name']
            }

            saved_unique.append(final_r)


    end_unique_pairs = pd.DataFrame(saved_unique)

    if end_unique_pairs.empty:
        return pd.DataFrame(columns=['anon_id', 'matched_name'])


    return end_unique_pairs


def deanonymization_rate(matches_df, anon_df):
    """
    Compute the fraction of anonymized records
    that were uniquely re-identified.
    """

    if (anon_df is None) or ( len(anon_df) == 0 ):
        return 0.0
    

    if matches_df is None:
        return 0.0
    

    len_matches_df = len(matches_df)

    len_anon_df = len(anon_df)

    fract_anon_record_unique = len_matches_df / len_anon_df

    return fract_anon_record_unique
