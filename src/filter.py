import pandas as pd
import numpy as np

#global variables
file_path = "data/TMDB_tv_dataset_v3.csv"
raw_file = pd.read_csv(file_path, delimiter=",")

def filter_first(votes_minimum : int) -> pd.DataFrame:
    data = raw_file[['name', 'vote_count', 'vote_average', 'number_of_seasons', 'number_of_episodes']].replace(to_replace=0, value=np.nan).dropna().index
    file_votes = raw_file.loc[data]
    return (file_votes[file_votes['vote_count'] > votes_minimum]).copy()

def filter_second(series_minimum : int, date_max : list[int]=[0, 9999]) -> pd.DataFrame:
    d_file = raw_file[['name', 'vote_count', 'vote_average', 'popularity', 'genres', 'networks', 'first_air_date']].replace(to_replace=0, value=np.nan).dropna()
    data_index = d_file[[int(item[0]) >= date_max[0] and int(item[0]) <= date_max[1] for item in d_file['first_air_date'].str.split('-')[:].tolist()]].index
    flt_file = (raw_file.loc[data_index]).copy()
    flt_file['genres'] = flt_file['genres'].str.split(", ")
    flt_file['networks'] = flt_file['networks'].str.split(", ")
    flt_file = flt_file.explode('genres').explode('networks')
    spl_file = flt_file[['networks', 'genres']].copy()
    net_list = (spl_file.groupby('networks').count() > series_minimum).replace(to_replace=False, value=np.nan).dropna().reset_index()['networks'].tolist()
    flt_file = flt_file[flt_file['networks'].isin(net_list)]
    return flt_file.copy()

def filter_third(votes_minimum : int) -> pd.DataFrame:
    data = raw_file[['name', 'vote_count', 'vote_average', 'popularity', 'networks']].replace(to_replace=0, value=np.nan).dropna().index
    file_votes = raw_file.loc[data]
    return (file_votes[file_votes['vote_count'] > votes_minimum]).copy()


