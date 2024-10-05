import pandas as pd
import numpy as np

#global variables
file_path = "data/TMDB_tv_dataset_v3.csv"
file = pd.read_csv(file_path, delimiter=",")

def filter_first(votes_minimum):
    data = file[['name', 'vote_count', 'vote_average', 'number_of_seasons', 'number_of_episodes']].replace(to_replace=0, value=np.nan).dropna().index
    file_votes = file.loc[data]
    return (file_votes[file_votes['vote_count'] > votes_minimum]).copy()

def filter_second():
    data = file[['name', 'vote_count', 'vote_average', 'popularity', 'genres', 'networks']].replace(to_replace=0, value=np.nan).dropna().index
    file_votes = (file.loc[data]).copy()
    (file_votes[file_votes['vote_count'] > 0]).copy()
    file_votes['genres'] = file_votes['genres'].str.split(", ")
    return file_votes.explode('genres')

def filter_third():
    data = file[['name', 'vote_count', 'vote_average', 'popularity', 'genres', 'networks']].replace(to_replace=0, value=np.nan).dropna().index
    return (file.loc[data]).copy()




