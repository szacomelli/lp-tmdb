import pandas as pd
import numpy as np
import os
import sys

#global variables
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data/TMDB_tv_dataset_v3.csv'))
raw_file = pd.read_csv(file_path, delimiter=",")

def filter_first(votes_minimum: int = 0) -> pd.DataFrame:
    # Ensure that shows with episodes but no seasons are assigned at least one season
    raw_file.loc[(raw_file['number_of_episodes'] > 0) & (raw_file['number_of_seasons'] == 0), 'number_of_seasons'] = 1


    # Filter out shows with no votes and no episodes
    df_filtered = raw_file[(raw_file['vote_count'] >= votes_minimum) & (raw_file['number_of_episodes'] > 0)].copy()
    
    df_index = df_filtered[['name', 'vote_count', 'vote_average', 'number_of_episodes']].replace(to_replace=0, value=np.nan).dropna().index
    df_filtered = df_filtered.loc[df_index].copy()
    
    # Calculate the average number of episodes per season
    df_filtered['avg_ep_per_season'] = np.floor(df_filtered['number_of_episodes'] / df_filtered['number_of_seasons'])
    
    # Drop rows with NaN values in 'vote_average'
    df_filtered = df_filtered.dropna(subset=['vote_average'])
    
    return df_filtered

def filter_second(shows_minimum : int, date_interval : list[int]=[0, 9999]) -> pd.DataFrame:
    """
    Filters the TMDB TV Shows database presented in the data folder, accordingly with the needs 
    of the 2nd hypotheses (aka. hipotheses_silvio).

    Parameters
    ----------
    series_minimum : int
        Minimum number of shows that every streaming networks needs to have in order to continue 
        in the dataset.
    date_interval : list[int], default [0, 9999]
        A list with two elements, which represents the interval of time (in years) in which the 
        shows needs to have been aired in order to be kept in the dataset.

    Returns
    -------
    pandas.Dataframe
        The filtered version of the dataset.

    Raises
    ------
    TypeError:
        When shows_minimum isn't instances of int, or date_interval isn't a list of two integers.
    ValueError:
        When the first element of date_interval is greater than the second.  

    Examples
    --------
    >>> filter_second(0)
                   id  ... episode_run_time
        0        1399  ...                0
        0        1399  ...                0
        0        1399  ...                0
        1       71446  ...               70
        1       71446  ...               70
        ...       ...  ...              ...
        57497  238881  ...                0
        57497  238881  ...                0
        57498  238853  ...                0
        57498  238853  ...                0
        57500   29024  ...               60

        [90676 rows x 29 columns]

    >>> filter_second(100, [2023, 2024])
                   id  ... episode_run_time
        642    111110  ...                0
        642    111110  ...                0
        953    129552  ...                0
        953    129552  ...                0
        953    129552  ...                0
        ...       ...  ...              ...
        57489  241206  ...                0
        57489  241206  ...                0
        57489  241206  ...                0
        57497  238881  ...                0
        57497  238881  ...                0

        [1057 rows x 29 columns]
        
    """
    if not isinstance(shows_minimum, int) or not isinstance(date_interval[0], int) or len(date_interval) != 2:
        raise TypeError("check the argument types")
    if not isinstance(date_interval[1], int):
        raise TypeError("check the argument types")
    if date_interval[0] > date_interval[1]:
        raise ValueError("the first element of date_interval must be less or equal the second")
    
    raw_data = raw_file[['name', 'vote_count', 'vote_average', 'popularity', 'genres', 'networks', 'first_air_date']].replace(to_replace=0, value=np.nan).dropna()
    data_index = raw_data[[int(item[0]) >= date_interval[0] and int(item[0]) <= date_interval[1] for item in raw_data['first_air_date'].str.split('-')[:].tolist()]].index
    flt_data = (raw_file.loc[data_index]).copy()
    flt_data['genres'] = flt_data['genres'].str.split(", ")
    flt_data['networks'] = flt_data['networks'].str.split(", ")
    flt_data = flt_data.explode('genres').explode('networks')
    spl_data = flt_data[['networks', 'genres']].copy()
    net_list = (spl_data.groupby('networks').count() > shows_minimum).replace(to_replace=False, value=np.nan).dropna().reset_index()['networks'].tolist()
    flt_data = flt_data[flt_data['networks'].isin(net_list)]
    return flt_data.copy()

def filter_third(shows_minimum : int, votes_minimum : int=1) -> pd.DataFrame:
    """
    Filters the TMDB TV Shows database presented in the data folder, accordingly with the needs 
    of the 3rd hypotheses (aka. hipotheses_dilmar).

    Parameters
    ----------
    series_minimum : int
        Minimum number of shows that every streaming networks needs to have in order to continue 
        in the dataset.
    votes_minimum : int, default 1
        Minimum number of votes a series needs to have in order to continue in the dataset.

    Returns
    -------
    pandas.Dataframe
        The filtered version of the dataset.

    Raises
    ------
    TypeError:
        When shows_minimum or votes_minimum aren't instances of int.   

    Examples
    --------
    >>> filter_third(1)
               id  ... episode_run_time
    0        1399  ...                0
    2       66732  ...                0
    3        1402  ...               42
    4       63174  ...               45
    5       69050  ...               45
    ...       ...  ...              ...
    57493  238871  ...                0
    57495  237677  ...                0
    57497  238881  ...                0
    57498  238853  ...                0
    57500   29024  ...               60

    [43481 rows x 29 columns]


    >>> filter_third(100, 100)
              id                 name  ...      production_countries  episode_run_time
    2      66732      Stranger Things  ...  United States of America                 0
    6      93405           Squid Game  ...               South Korea                 0
    8      71712      The Good Doctor  ...  United States of America                43
    11      1418  The Big Bang Theory  ...  United States of America                22
    13      1416       Grey's Anatomy  ...  United States of America                43
    ...      ...                  ...  ...                       ...               ...
    2997   89785      Family Business  ...                    France                27
    2999  216811             Triptych  ...                    Mexico                 0
    3012    3162         Hart to Hart  ...                       NaN                60
    3015   67118           Conviction  ...  United States of America                42
    3017   81946     The Enemy Within  ...  United States of America                43

    [744 rows x 29 columns]

        
    """
    if not isinstance(shows_minimum, int) or not isinstance(votes_minimum, int): 
        raise TypeError("check the argument types")
    
    data_idx = raw_file[['name', 'vote_count', 'vote_average', 'popularity', 'networks']].replace(to_replace=0, value=np.nan).dropna().index
    raw_data = raw_file.loc[data_idx]
    flt_data = (raw_data[raw_data['vote_count'] >= votes_minimum]).copy()
    sub_data = flt_data[['networks', 'genres']].copy()
    net_list = (sub_data.groupby('networks').count() > shows_minimum).replace(to_replace=False, value=np.nan).dropna().reset_index()['networks'].tolist()
    return flt_data[flt_data['networks'].isin(net_list)].copy()


