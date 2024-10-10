import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt

from filter import filter_second

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

    Raises
    ------
    TypeError:
        When top_n and shows_minimum aren't instances of int, or years_interval isn't a list of two integers.
    ValueError:
        When shows_minimum is greater then the highest value of series per network.  
    
    Examples
    -------
    >>> most_frequent_genre(60)
    >>> most_frequent_genre(1000, 100, [2023,2024])

    Notes
    -----
    The function won't return anything, but plots a pyplot bar graph.
    Expects a bar graph with networks:(series) as x_labels and absolute count of frequency as y_label
    """
    if not isinstance(top_n, int) or not isinstance(shows_minimum, int) or not isinstance(years_interval[0], int) \
            or not isinstance(years_interval, list) or len(years_interval) != 2:
        raise TypeError("check the argument types")
    if not isinstance(years_interval[1], int):
        raise TypeError("check the argument types")
    if years_interval[0] > years_interval[1]:
        raise ValueError("the first element of years_interval must be less or equal the second")
    
    #counting frequency of shows per network
    raw_data = filter_second(shows_minimum, years_interval).groupby(['genres', 'networks'])['networks'].value_counts().reset_index()
    data_idx = raw_data.groupby('networks')['count'].idxmax()
    top_data = raw_data.loc[data_idx].copy()

    #creating the output for the plot
    top_data = raw_data.sort_values('count', ascending=False).head(top_n)
    top_data['for_plot'] = top_data['networks'] + ": (" + top_data['genres'] + ")"
    
    if top_data.empty:
        raise ValueError("shows_minimum can't be greater then the highest count of shows per network")
    plot_bar(top_data.set_index('for_plot'), "Most frequent genres by network", "Network and genre", "Average frequency", years_interval)
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

    Raises
    ------
    TypeError:
        When top_n and shows_minimum aren't instances of int, or years_interval isn't a list of two integers.
    ValueError:
        When shows_minimum is greater then the highest value of series per network.  
        
    Examples
    -------
    >>> most_frequent_genre(60)
    >>> most_frequent_genre(1000, 100, [2023,2024])

    Notes
    -----
    The function won't return anything, but plots a pyplot bar graph.
    Expects a bar graph with networks:(series) as x_labels and vote average of genre as y_label
    """
    if not isinstance(top_n, int) or not isinstance(shows_minimum, int) or not isinstance(years_interval[0], int) \
            or not isinstance(years_interval, list) or len(years_interval) != 2:
        raise TypeError("check the argument types")
    if not isinstance(years_interval[1], int):
        raise TypeError("check the argument types")
    if years_interval[0] > years_interval[1]:
        raise ValueError("the first element of years_interval must be less or equal the second")
    
    raw_data = filter_second(shows_minimum, years_interval)
    #creating a column that'll be used to create the final vote average (the final average is calculated
    # by the sum of these averages divided by the sum ov vote_count, grouping by "series by networks")
    raw_data['average'] = raw_data['vote_count']*raw_data['vote_average']
    raw_data = raw_data.groupby(['genres', 'networks']).sum(['average', 'vote_count']).reset_index()[['networks', 'genres', 'average', 'vote_count']]
    raw_data['final_average'] = raw_data['average'] / raw_data['vote_count']
    data_idx = raw_data.groupby('networks')['final_average'].idxmax()
    top_data = raw_data.loc[data_idx].copy()
    #preparing the data to be plotted
    top_data['for_plot'] = top_data['networks'] + ": (" + top_data['genres'] + ")"
    top_data = top_data[['for_plot', 'final_average']].sort_values('final_average', ascending=False).head(top_n)

    if top_data.empty:
        raise ValueError("shows_minimum can't be greater then the highest count of shows per network")
    plot_bar(top_data.set_index('for_plot'), "Most voted genres by network", "Networks and genres", "Vote average", years_interval)
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

    Raises
    ------
    TypeError:
        When top_n and shows_minimum aren't instances of int, or years_interval isn't a list of two integers.
    ValueError:
        When shows_minimum is greater then the highest value of series per network.      

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
    if not isinstance(top_n, int) or not isinstance(shows_minimum, int) or not isinstance(years_interval[0], int) \
            or not isinstance(years_interval, list) or len(years_interval) != 2:       
        raise TypeError("check the argument types")
    if not isinstance(years_interval[1], int):
        raise TypeError("check the argument types")
    if years_interval[0] > years_interval[1]:
        raise ValueError("the first element of years_interval must be less or equal the second")
    
    #taking the average popularity by "genres by network" and using it's log instead the real value for plot (a way to normalize the data)
    raw_data = filter_second(shows_minimum, years_interval).groupby(['genres', 'networks']).mean('popularity').reset_index()[['networks', 'genres', 'popularity']]
    raw_data['popularity_log'] = np.log(raw_data['popularity'])
    data_idx = raw_data.groupby('networks')['popularity_log'].idxmax()
    #creating the data to plot
    top_data = raw_data.loc[data_idx].copy()
    top_data['for_plot'] = top_data['networks'] + ": (" + top_data['genres'] + ")"
    top_data = top_data[['for_plot', 'popularity_log']].sort_values('popularity_log', ascending=False).head(top_n)

    if top_data.empty:
        raise ValueError("shows_minimum can't be greater then the highest count of shows per network")
    plot_bar(top_data.set_index('for_plot'), "Most popular genres by network", "Networks and genres", "Popularity", years_interval)
    return

def plot_bar(dataframe : pd.DataFrame, plt_title : str="plot", x_axis : str="x", y_axis : str="y", years : list[int]=[0,9999]) -> None:
    """
    Auxiliar function for the other three functions. Should not be called individually.
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
    Note that there aren't Raises because the other functions should handle the Exceptions before 
    calling this auxiliar function.

    """
    
    if years != [0,9999]:
        plt_title = plt_title + ", from " + str(years[0]) + " to " + str(years[1])
    print(plt_title)
    
    #changing resolution
    figure = plt.subplots(figsize=(19.2, 10.8))  
    dataframe.plot.bar(title=plt_title, ax=figure[1])
    
    figure[1].set_xlabel(x_axis)
    figure[1].set_ylabel(y_axis)
    plt.subplots_adjust(bottom=0.5)
    
    plt.savefig(f"./output/{plt_title}.png", dpi=100)
    plt.close()
    print("plot saved")
    return
