from filter import filter_second
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt

def most_frequent_genre(top_n : int, shows_minimum : int=0, years_interval : list[int]=[0,9999]) -> None:
    """
    Generates a graph showing the genres of the most producted shows by networks.

    Parameters
    ----------
    top_n : int
        Plots just the first top_n networks and genres
    series_minimum : int, default 0
        Plots just networks that have at least this number os shows
    years_interval : list[int], default [0,9999]
        Plots just the series aired between the first and second element (in years) of the list 

    Examples
    -------
    >>> most_frequent_genre(60)
    >>> most_frequent_genre(1000, 100, [2023,2024])

    Notes
    -----
    The function won't return anything, but plots a pyplot bar graph.
    Expects a bar graph with networks:(series) as x_labels and absolute count of frequency as y_label
    """
    raw_data = filter_second(shows_minimum, years_interval).groupby(['genres', 'networks'])['networks'].value_counts().reset_index()
    data_idx = raw_data.groupby('networks')['count'].idxmax()
    top_data = raw_data.loc[data_idx].copy()
    top_data = raw_data.sort_values('count', ascending=False).head(top_n)
    top_data['for_plot'] = top_data['networks'] + ": (" + top_data['genres'] + ")"
    
    plot_bar(top_data.set_index('for_plot'), "Gêneros mais frequentes por plataforma", "Plataforma", "Frequência média", years_interval)
    return

def most_voted_genre(top_n : int, shows_minimum : int=0, years_interval : list[int]=[0,9999]) -> None:
    """
    Generates a graph showing the genres of the shows with highest average of votes by networks.

    Parameters
    ----------
    top_n : int
        Plots just the first top_n networks and genres
    series_minimum : int, default 0
        Plots just networks that have at least this number os shows
    years_interval : list[int], default [0,9999]
        Plots just the series aired between the first and second element (in years) of the list 

    Examples
    -------
    >>> most_frequent_genre(60)
    >>> most_frequent_genre(1000, 100, [2023,2024])

    Notes
    -----
    The function won't return anything, but plots a pyplot bar graph.
    Expects a bar graph with networks:(series) as x_labels and vote average of genre as y_label
    """
    raw_data = filter_second(shows_minimum, years_interval)
    raw_data['average'] = raw_data['vote_count']*raw_data['vote_average']
    raw_data = raw_data.groupby(['genres', 'networks']).sum(['average', 'vote_count']).reset_index()[['networks', 'genres', 'average', 'vote_count']]
    raw_data['final_average'] = raw_data['average'] / raw_data['vote_count']
    data_idx = raw_data.groupby('networks')['final_average'].idxmax()
    top_data = raw_data.loc[data_idx].copy()
    top_data['for_plot'] = top_data['networks'] + ": (" + top_data['genres'] + ")"
    top_data = top_data[['for_plot', 'final_average']].sort_values('final_average', ascending=False).head(top_n)
    
    plot_bar(top_data.set_index('for_plot'), "Gêneros mais votados por plataforma", "Plataforma", "Média de votos", years_interval)
    return

def most_popular_genre(top_n : int, shows_minimum : int=0, years_interval : list[int]=[0,9999]) -> None:
    """
    Generates a graph showing the genres of the most popular shows by networks.

    Parameters
    ----------
    top_n : int
        Plots just the first top_n networks and genres.
    series_minimum : int, default 0
        Plots just networks that have at least this number os shows.
    years_interval : list[int], default [0,9999]
        Plots just the series aired between the first and second element (in years) of the list. 

    Examples
    -------
    >>> most_frequent_genre(60)
    >>> most_frequent_genre(1000, 100, [2023,2024])

    Notes
    -----
    The function won't return anything, but plots a pyplot bar graph.
    Expects a bar graph with networks:(series) as x_labels and popularity average as y_label.
    Popularity is a measure based on the current rate of votes, favorites and other 
    metrics in a daily basis, along with aired date and some other information.
    To know more, consult https://developer.themoviedb.org/docs/popularity-and-trending
    """
    raw_data = filter_second(shows_minimum, years_interval).groupby(['genres', 'networks']).mean('popularity').reset_index()[['networks', 'genres', 'popularity']]
    raw_data['popularity_log'] = np.log(raw_data['popularity'])
    data_idx = raw_data.groupby('networks')['popularity_log'].idxmax()
    top_data = raw_data.loc[data_idx].copy()
    top_data['for_plot'] = top_data['networks'] + ": (" + top_data['genres'] + ")"
    top_data = top_data[['for_plot', 'popularity_log']].sort_values('popularity_log', ascending=False).head(top_n)

    plot_bar(top_data.set_index('for_plot'), "Gêneros mais populares por plataforma", "Plataforma", "Popularidade", years_interval)
    return

def plot_bar(dataframe : pd.DataFrame, plt_title : str="plot", x_axis : str="x", y_axis : str="y", years : list[int]=[0,9999]) -> None:
    """
    Plots a bar graph of a dataframe, saving it to output folder.

    Parameters
    ----------
    dataframe : pd.DataFrame
        The dataframe containing info to plot the graph.
    plt_title : str, default "plot"
        The title of the graph. If years is not in default value, the elements of years are added
        in the title, which becomes title + " from " + years[0] + " to " + years[1]
    x_axis : str, default "x"
        The label of the x_axis.
    y_axis : str, default "y"
        The label of the y_axis
    years : list[int], default [0,9999]
        Interval of years in which the information of the graph is restricted to.

    Examples
    --------
    >>> plot_bar(some_dataframe)
    plot saved
    >>> plot_bar(some_dataframe, "an awesome graph", "my x axis", "my y axis", [2023, 2024])
    plot saved

    Notes
    -----
    The function returns None, but expect to have it plotting a pyplot bar graph with the 
    parameters as title, x and y labels.

    """
    
    if years != [0,9999]:
        plt_title = plt_title + ", de " + str(years[0]) + " a " + str(years[1])

    figure = plt.subplots(figsize=(19.2, 10.8))  
    dataframe.plot.bar(title=plt_title, ax=figure[1])
    
    figure[1].set_xlabel(x_axis)
    figure[1].set_ylabel(y_axis)
    plt.subplots_adjust(bottom=0.5)

    
    
    plt.savefig("./output/graph.png", dpi=100)
    plt.close()
    print("plot saved")
    return

most_frequent_genre(60, 100)