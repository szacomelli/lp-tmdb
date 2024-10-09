from filter import filter_second
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt

def most_frequent_genre(top_n : int, series_minimum : int=0, years_interval : list[int]=[0,9999]) -> None:
    raw_data = filter_second(series_minimum, years_interval).groupby(['genres', 'networks'])['networks'].value_counts().reset_index()
    data_idx = raw_data.groupby('networks')['count'].idxmax()
    top_data = raw_data.loc[data_idx].copy()
    top_data = raw_data.sort_values('count', ascending=False).head(top_n)
    top_data['for_plot'] = top_data['networks'] + ": (" + top_data['genres'] + ")"
    
    plot_bar(top_data.set_index('for_plot'), "Gêneros mais frequentes por plataforma", "Plataforma", "Frequência média", years_interval)
    return

def most_voted_genre(top_n : int, series_minimum : int=0, years_interval : list[int]=[0,9999]) -> None:
    raw_data = filter_second(series_minimum, years_interval)
    raw_data['average'] = raw_data['vote_count']*raw_data['vote_average']
    raw_data = raw_data.groupby(['genres', 'networks']).sum(['average', 'vote_count']).reset_index()[['networks', 'genres', 'average', 'vote_count']]
    raw_data['final_average'] = raw_data['average'] / raw_data['vote_count']
    data_idx = raw_data.groupby('networks')['final_average'].idxmax()
    top_data = raw_data.loc[data_idx].copy()
    top_data['for_plot'] = top_data['networks'] + ": (" + top_data['genres'] + ")"
    top_data = top_data[['for_plot', 'final_average']].sort_values('final_average', ascending=False).head(top_n)
    
    plot_bar(top_data.set_index('for_plot'), "Gêneros mais votados por plataforma", "Plataforma", "Média de votos", years_interval)
    return

def most_popular_genre(top_n : int, series_minimum : int=0, years_interval : list[int]=[0,9999]) -> None:
    raw_data = filter_second(series_minimum, years_interval).groupby(['genres', 'networks']).mean('popularity').reset_index()[['networks', 'genres', 'popularity']]
    raw_data['popularity_log'] = np.log(raw_data['popularity'])
    data_idx = raw_data.groupby('networks')['popularity_log'].idxmax()
    top_data = raw_data.loc[data_idx].copy()
    top_data['for_plot'] = top_data['networks'] + ": (" + top_data['genres'] + ")"
    top_data = top_data[['for_plot', 'popularity_log']].sort_values('popularity_log', ascending=False).head(top_n)

    plot_bar(top_data.set_index('for_plot'), "Gêneros mais populares por plataforma", "Plataforma", "Popularidade", years_interval)
    return

def plot_bar(dataframe : pd.DataFrame, plt_title : str, x_axis : str, y_axis : str, year : list[int]=[0,9999]) -> None:
    if year != [0,9999]:
        plt_title = plt_title + ", de " + str(year[0]) + " a " + str(year[1])
    dataframe.plot.bar(title=plt_title)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.subplots_adjust(bottom=0.5)
    plt.show()
    return