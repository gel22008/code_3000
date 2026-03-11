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


    #these make copies to ensure that I don't write over any of the data
    #on accident
    big_anon = anon_df.copy()       #anonymized.csv
    big_aux = aux_df.copy()         #auxiliary.csv

    #this renames the first column to the desired "matched_name" name
    #this is because the auxiliary and the anonymized files have different
    #names for that column only
    big_aux.columns = ['matched_name', 'age', 'zip3', 'gender']

    #all the IDs found that match in just the age, zip3 and gender cols
    #this is because can get sometimes get duplicates with different names
    #so will have to throw those out below to get the "ONLY uniquely matched records."
    IDs_matched = pd.merge(big_anon, big_aux, on=['age', 'zip3', 'gender'], how='inner')

    #now it counts how many times there are pairs, again just with the 
    #age, zip3 and gender cols, because there again can be duplicates with
    #the names
    all_found = IDs_matched['anon_id'].value_counts()

    #this is the beginning of the finding all the pairs
    only_one_match = []

    #now loops through all the matches found, there are
    #still duplciates right now
    #
    for id_val, pair in all_found.items():

        #this finds all the unique matches, hence
        #why the amount of pairs is just 1 
        if (1 == pair):

            #if there is only one match, which is when get 
            #into here, then add it to the dictionary
            #because found a unique value
            only_one_match.append(id_val)


    saved_unique = []

    #this is for saving all the unique names with their 
    #also unique ID's
    for idx, where_in_data in IDs_matched.iterrows():
        #loops through all the overall matches, going 
        #from top to bottom


        if where_in_data['anon_id'] in only_one_match:
            #if current set of name, age, zip3, gender found in the 
            #set of unique ones. 

            #then same their id and name, 
            #can do this because IDs_matched above has both the 
            #auxilary.csv and ethe anonymized.csv so it just takes
            #the id and the name of all the unique peopel
            final_r = {
                'anon_id' : where_in_data['anon_id'],
                'matched_name': where_in_data['matched_name']
            }

            #now save all the name and id's of the unique 
            #people found 
            saved_unique.append(final_r)

    #now save all the values into a DataFrame as to have all 
    #the id's and the names saved
    end_unique_pairs = pd.DataFrame(saved_unique)

    if end_unique_pairs.empty:
        #if there are no pairs just return with the columns 
        return pd.DataFrame(columns=['anon_id', 'matched_name'])

    #now just return the resulting id's and name because there are 
    #matches that were actually found
    return end_unique_pairs


def deanonymization_rate(matches_df, anon_df):
    """
    Compute the fraction of anonymized records
    that were uniquely re-identified.
    """

    #this is used to check if the anonymized.csv file
    #is somehow empty, then return none becasue tehre
    # could be no pairs found if one file is empty 

    #also if one file is empty, so too much the other be
    #also we didn't have access to the other one in this file
    if (anon_df is None) or ( len(anon_df) == 0 ):

        #just return 0.0, I tried 0, but it seemed to 
        #like 0.0 better
        return 0.0
    

    if matches_df is None:
        #this is now if there are no matches found
        #if no matches just again return 0.0

        return 0.0
    


    #this is all to calculate the ending 
    # fraction of anonymized records that were uniquely 
    # re-identified. 

    #this finds the length of all the matches to compare
    #against the amount of files in the anonymize.csv
    len_matches_df = len(matches_df)

    #now find the total amount of people that have saved in the 
    #anonymized file
    len_anon_df = len(anon_df)


    #this is just the number of matches over the total amount 
    #of people we have
    fract_anon_record_unique = len_matches_df / len_anon_df

    #just return back the ratio
    return fract_anon_record_unique
