from filter import filter_third
import matplotlib.pyplot as plt # type: ignore
import seaborn as sns # type: ignore
import pandas as pd # type: ignore
import numpy as np # type: ignore

def dilmar_hypothesis(shows_minimum : int, votes_minimum : int):
    """
    Create graphs for many intervals of the column "vote_average", the x-axis is "networks" and the y-axis is "popularity"

    Parameters
    ----------
    shows_minimum : int
        The minimum amount o tv shows a network need.
    votes_minimum : int
        The minimum amount of "vote_count" a tv show need.

    Examples
    --------
    >>> dilmar_hypotesis(10, 150)
    $
    >>> dilmar_hypotesis(0, 1000)
    $

    Notes
    -----
    Return graphs in png.
    """
    if not isinstance(shows_minimum, int) or not isinstance(votes_minimum, int):       
        raise TypeError("check the argument types")

    try:

        df = filter_third(shows_minimum,votes_minimum)
        df = df[['name', 'vote_count', 'vote_average', 'popularity', 'networks']]
        # Receives clean from the filter_third function and then saves only the useful columns.
        print(df)

        df['networks'] = df['networks'].str.split(',')
        df = df.explode('networks')
        # Divide the lines that have more than one network into distinct identical lines, each with a distinct network

        lower_bound = df['vote_average'].min() - 0.1
        upper_bound = df['vote_average'].max() + 0.1
        number_bins = int(np.ceil(np.log2((upper_bound-lower_bound)*10) + 1))
        # Find the upper bound, lower bound and the number of bins,
        # the lower_bound and upper_bound are subtracted and added to 0.1
        # so that no series is on the edge of the interval and does not fall into any.
        # Sturges' rule was used to calculate the amount of bins based in the tenths between lower and upper bound.

        bins = range(number_bins)*(upper_bound -lower_bound)/(number_bins - 1) + lower_bound
        bins_intervals = [f"[{round(bins[i], 2)} - {round(bins[i+1], 2)}]" for i in range(len(bins) - 1)]
        # Calculate the bins by dividing the range from lowest to highest note into equal intervals.
        # Then make an array of strings that name each interval.

        df['labels'] = pd.cut(df['vote_average'], bins = bins, labels = bins_intervals, right = True)
        df = df.groupby(['labels', 'networks'], observed = True)['popularity'].mean().reset_index()
        df = df.sort_values(by = ['popularity'], ascending=[True])
        # Label each row with its proper range, then merge the rows with the same label
        # and network by averaging the popularity column, then sorting in ascending order.

        for i in bins_intervals:
            df_filtrado = df[df['labels'] == i]
            sns.barplot(x='networks', y='popularity', data = df_filtrado)
            plt.xticks(rotation=45, ha='right', fontsize = 10)
            plt.title(f"Vote average bin: {i}", fontsize=16)
            plt.savefig(f'./output/graph{bins_intervals.index(i)}.png')
            fig_legend = plt.figure(figsize=(25, 10))
        # Make a graph for each interval
    except OverflowError:
        print("Error: the filter is removing all the lines. Change the parameters.")
