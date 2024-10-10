import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from filter import filter_first
# from src.filter import filter_first

# Function to adjust bins based on IQR
def bins_IQR(df: pd.DataFrame) -> list:
    """
    Adjusts the number of bins based on the Interquartile Range (IQR).

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the data.

    Raises
    ------
    ValueError
        If the number of bins and labels does not match.
        If DataFrame is empty.
        If 'avg_ep_per_season' column is missing or contains NaN values.
        If 'avg_ep_per_season' contains non-numeric values.
    TypeError
        if type(df) is not pd.DataFrame
    
    Returns
    -------
    list
        A list containing the bin edges and labels.
    
    Example
    -------
    This example uses a set of values ranging from 10 to 100. The function then creates bins of approximately 
    equal size using the interquartile range (IQR), adjusting the last bin to include the maximum value.
    >>> df = pd.DataFrame({'avg_ep_per_season': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]})
    >>> bin_edges, labels = bins_IQR(df)
    >>> print(bin_edges)
    [0 5 10 15 21 26 31 36 42 47 52 57 63 68 73 78 84 89 94 100]
    >>> print(labels)
    ['0-4', '5-9', '10-14', '15-20', '21-25', '26-30', '31-35', '36-41', '42-46', '47-51', '52-56', '57-62', 
    '63-67', '68-72', '73-77', '78-83', '84-88', '89-93', '94 or more']

    In this example, the DataFrame contains small values (from 1 to 10). The function creates almost unitary bins, 
    demonstrating the function's behavior when the values are in a small range. This illustrates how the 
    function handles data with little variation.
    >>> df = pd.DataFrame({'avg_ep_per_season': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
    >>> bin_edges, labels = bins_IQR(df)
    >>> print(bin_edges)
    [0 1 2 3 4 5 6 7 8 9 10]
    >>> print(labels)
    ['0-0', '1-1', '2-2', '3-3', '4-4', '5-5', '6-6', '7-7', '8-8', '9 or more']

    This example has larger and slightly more distant values, ranging from 50 to 140. The function creates bins through 
    a wider range, adapting to data with high and widely distributed values. This illustrates how the function 
    handles data with greater variation.
    >>> df = pd.DataFrame({'avg_ep_per_season': [50, 60, 70, 80, 90, 100, 110, 120, 130, 140]})
    >>> bin_edges, labels = bins_IQR(df)
    >>> print(bin_edges)
    [0 7 14 22 29 36 44 51 58 66 73 81 88 95 103 110 117 125 132 140]
    >>> print(labels)
    ['0-6', '7-13', '14-21', '22-28', '29-35', '36-43', '44-50', '51-57', '58-65', '66-72', '73-80', '81-87',
    '88-94', '95-102', '103-109', '110-116', '117-124', '125-131', '132 or more']
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Check the types of the passed arguments")
    
    if df.empty:
        raise ValueError("DataFrame is empty.")
    
    if 'avg_ep_per_season' not in df.columns:
        raise ValueError("DataFrame does not contain the 'avg_ep_per_season' column.")
    
    if df['avg_ep_per_season'].isnull().any():
        raise ValueError("DataFrame contains NaN values in the 'avg_ep_per_season' column.")

    if not pd.api.types.is_numeric_dtype(df['avg_ep_per_season']):
        raise ValueError("Column 'avg_ep_per_season' must contain only numeric values.")
    
    
    avg_ep_per_season = df['avg_ep_per_season']
    num_bins = 21
    
    # Calculation of quartiles and IQR
    q1 = avg_ep_per_season.quantile(0.25)
    q3 = avg_ep_per_season.quantile(0.75)
    iqr = q3 - q1
    upper_limit = min(q3 + 1.5 * iqr, avg_ep_per_season.max())  # Upper limit for outliers
    
    # Creation of equidistant intervals up to the upper limit
    bin_edges = np.linspace(0, upper_limit, num_bins - 1).astype(int)
    bin_edges = np.append(bin_edges, avg_ep_per_season.max()).astype(int)  # Add the maximum value as the last bin

    bin_edges = np.unique(bin_edges)
    num_bins = len(bin_edges)
    
    # Generation of labels
    labels = [f"{bin_edges[i]}-{bin_edges[i+1]-1}" for i in range(len(bin_edges)-1)]
    labels[-1] = f"{bin_edges[-2]} or more"
    
    if len(labels) != len(bin_edges) - 1:
        raise ValueError(f"Mismatch between number of bins ({len(bin_edges)}) and labels ({len(labels)}).")
    return bin_edges, labels

def bins_with_outliers(df: pd.DataFrame, num_bins: int) -> list:
    """
    Adjusts the number of bins, taking into account outlier values.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the data.
    num_bins : int
        The desired number of bins.

    Raises
    ------
    ValueError
        If the number of bins and labels does not match.
        If DataFrame is empty.
        If 'avg_ep_per_season' column is missing or contains NaN values.
        If 'avg_ep_per_season' contains non-numeric values.
    TypeError
        If DataFrame is not of type pd.DataFrame.
    
    Returns
    -------
    list
        A list containing the bin edges and labels.
    
    Example
    -------
    In this example, a set of values from 10 to 100 is divided into 5 bins. The values are uniformly distributed, 
    and the last bin is adjusted to include any value above the final limit.
    >>> df = pd.DataFrame({'avg_ep_per_season': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]})
    >>> bin_edges, labels = bins_with_outliers(df, 5)
    >>> print(bin_edges)
    [  0  20  40  60  80 100]
    >>> print(labels)
    ['0-19', '20-39', '40-59', '60-79', '80 or more']

    In this example, we have a set with low values and some large outliers, with the function dividing the data into 6 bins. 
    The example illustrates the function's ability to handle dispersed and asymmetric data.
    >>> df = pd.DataFrame({'avg_ep_per_season': [5, 15, 25, 100, 150, 200, 250, 300, 400, 500]})
    >>> bin_edges, labels = bins_with_outliers(df, 6)
    >>> print(bin_edges)
    [  0  83 166 250 333 416 500]
    >>> print(labels)
    ['0-82', '83-165', '166-249', '250-332', '333-415', '416 or more']

    In this example, the values are higher and include large outliers of greater value, such as 2500 and 3000. The function creates 5 appropriate bins, 
    where the last bin groups all values above 2400, highlighting the function's behavior to handle series of large values.
    >>> df = pd.DataFrame({'avg_ep_per_season': [500, 600, 700, 800, 900, 1000, 1500, 2000, 2500, 3000]})
    >>> bin_edges, labels = bins_with_outliers(df, 5)
    >>> print(bin_edges)
    [   0  600 1200 1800 2400 3000]
    >>> print(labels)
    ['0-599', '600-1199', '1200-1799', '1800-2399', '2400 or more']
    """
    if not isinstance(num_bins, int):
        raise ValueError("The number of bins must be an integer.")
    
    if num_bins <= 1:
        raise ValueError("The number of bins must be greater than 1.")
    
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Check the types of the passed arguments")
    
    if df.empty:
        raise ValueError("DataFrame is empty.")
    
    if 'avg_ep_per_season' not in df.columns:
        raise ValueError("DataFrame does not contain the 'avg_ep_per_season' column.")
    
    if df['avg_ep_per_season'].isnull().any():
        raise ValueError("DataFrame contains NaN values in the 'avg_ep_per_season' column.")

    if not pd.api.types.is_numeric_dtype(df['avg_ep_per_season']):
        raise ValueError("Column 'avg_ep_per_season' must contain only numeric values.")
    
    if num_bins > max(df['avg_ep_per_season']):
        raise ValueError("The number of bins is greater than the number of values in the 'avg_ep_per_season' column.")
    
    avg_ep_per_season = df['avg_ep_per_season']
    num_bins = num_bins + 1  # Add one more bin to account for the outliers
    
    # Creation of intervals
    bin_edges = np.linspace(0, avg_ep_per_season.max(), num_bins).astype(int)
    
    # Generation of labels
    labels = [f"{bin_edges[i]}-{bin_edges[i+1]-1}" for i in range(len(bin_edges)-1)]
    labels[-1] = f"{bin_edges[-2]} or more"
    
    return bin_edges, labels

# Function to display analysis and calculate metrics
def display_analysis(df: pd.DataFrame) -> None:
    """
    Display and save an analysis of TV show data by sorting, filtering, and generating bin-based statistics.

    This function filters and sorts the DataFrame containing TV show data based on the average number of episodes 
    per season. It also provides summary statistics on the number of shows within specific bin intervals 
    (IQR and outliers), saves the sorted DataFrame to a CSV file.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing TMDB dataset.

    Raises
    ------
    ValueError
        If DataFrame is empty.
        If 'avg_ep_per_season' column is missing or contains NaN values.
        If 'avg_ep_per_season' contains non-numeric values.
    TypeError
        if type(df) is not pd.DataFrame

    Returns
    -------
    None

    Example
    -------
    This example creates a fictitious DataFrame with information about 5 TV series. The function then counts how many series 
    exist within each bin and displays these results, also showing the total number of series in the DataFrame at the end.
    >>> df = pd.DataFrame({
            'name': ['Serie A', 'Serie B', 'Serie C', 'Serie D', 'Serie E'],
            'number_of_episodes': [50, 100, 200, 250, 300],
            'number_of_seasons': [2, 5, 10, 12, 15],
            'avg_ep_per_season': [25.0, 20.0, 20.0, 20.8, 25.0],
            'vote_average': [7.5, 8.0, 7.9, 7.4, 7.8],
            'popularity': [150, 250, 300, 350, 400],
            'category_bin_iqr': ['15-19', '20-24', '25 or more', '20-24', '25 or more'],
            'category_bin_outliers': ['15-19', '20-24', '25 or more', '20-24', '25 or more']
        })
    >>> display_analysis(df)
        category_bin_iqr
        15-19         1
        20-24         2
        25 or more    2
        Name: count, dtype: int64
        category_bin_outliers
        15-19         1
        20-24         2
        25 or more    2
        Name: count, dtype: int64
        Number of shows in the DataFrame: 5
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Check the types of the passed arguments")
    
    if df.empty:
        raise ValueError("DataFrame is empty.")
    
    if 'avg_ep_per_season' not in df.columns or df['avg_ep_per_season'].isnull().any():
        raise ValueError("DataFrame does not contain the 'avg_ep_per_season' column.")
    
    if not pd.api.types.is_numeric_dtype(df['avg_ep_per_season']):
        raise ValueError("Column 'avg_ep_per_season' must contain only numeric values.")
    
    df_filtered_final = df[['name', 'number_of_episodes', 'number_of_seasons', 'avg_ep_per_season', 'vote_average', 
                            'popularity', 'category_bin_iqr', 'category_bin_outliers']]
    df_filtered_final = df_filtered_final.sort_values(by='avg_ep_per_season', ascending=False)
    
    # Number of shows in each bin interval
    shows_per_bin_iqr = df_filtered_final['category_bin_iqr'].value_counts().sort_index()

    shows_per_bin_outliers = df_filtered_final['category_bin_outliers'].value_counts().sort_index()
    
   

# Function to plot bar charts with the average ratings per bin and distribution
def plot_charts(df: pd.DataFrame) -> None:
    """ 
    Creates the graphs needed for analysis: bar graph, scatter plot and histogram.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the data.

    Raises
    ------
    ValueError
        If the DataFrame is empty.
        If 'vote_average' column is missing or contains NaN values.
        If 'vote_average' contains non-numeric values.
    TypeError
        if type(df) is not pd.DataFrame

    Returns
    -------
    None

    Example
    -------
    This example creates a dummy DataFrame with information about 5 TV series. 
    The plot_charts(df) function then generates the requested charts.
    >>> df = pd.DataFrame({
            'name': ['Serie A', 'Serie B', 'Serie C', 'Serie D', 'Serie E'],
            'number_of_episodes': [50, 100, 200, 250, 300],
            'number_of_seasons': [2, 5, 10, 12, 15],
            'avg_ep_per_season': [25.0, 20.0, 20.0, 20.8, 25.0],
            'vote_average': [7.5, 8.0, 7.9, 7.4, 7.8],
            'popularity': [150, 250, 300, 350, 400],
            'category_bin_iqr': ['15-19', '20-24', '25 or more', '20-24', '25 or more'],
            'category_bin_outliers': ['15-19', '20-24', '25 or more', '20-24', '25 or more']
        })
    >>> plot_charts(df)
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Check the types of the passed arguments")
    
    if df.empty:
        raise ValueError("DataFrame is empty.")
    
    if 'vote_average' not in df.columns or df['vote_average'].isnull().any():
        raise ValueError("DataFrame does not contain the 'vote_average' column.")
    
    
    # Bar chart showing the average rating per category (IQR)
    plt.figure(figsize=(12, 6))
    plt_title = "Average Rating per Category (IQR)"
    mean_per_bin_iqr = df.groupby('category_bin_iqr', observed=False)['vote_average'].mean().reset_index()
    
    sns.barplot(x='category_bin_iqr', y='vote_average', hue='category_bin_iqr', data=mean_per_bin_iqr, palette='Set2', legend=False)
    plt.title(plt_title)
    plt.ylabel("Average Rating (Vote Average)")
    plt.xlabel("Episode Number Category (Bins)")
    plt.ylim(0, 10)  # Setting the y-axis from 0 to 10
    plt.xticks(rotation=45)
    plt.savefig(f"./output/{plt_title}.png", dpi=100)  # Saving the chart

    # Bar chart showing the average rating per category, including outliers
    plt.figure(figsize=(12, 6))
    plt_title = "Average Rating with outliers"
    mean_per_bin_outliers = df.groupby('category_bin_outliers', observed=False)['vote_average'].mean().reset_index()
    sns.barplot(x='category_bin_outliers', y='vote_average', hue='category_bin_outliers', data=mean_per_bin_outliers, palette='Set1', legend=False)
    plt.title(plt_title)
    plt.ylabel("Average Rating (Vote Average)")
    plt.xlabel("Episode Number Category (Bins)")
    plt.ylim(0, 10)  # Setting the y-axis from 0 to 10
    plt.xticks(rotation=45)
    plt.savefig(f"./output/{plt_title}.png", dpi=100)  # Saving the chart
    
    # Distribution chart of ratings (vote_average)
    plt.figure(figsize=(12, 6))
    plt_title = "Rating Distribution (Vote Average)"
    sns.histplot(df['vote_average'], bins=20, kde=True, color='blue')
    plt.title(plt_title)
    plt.xlabel("Rating (Vote Average)")
    plt.ylabel("Frequency")
    plt.savefig(f"./output/{plt_title}.png", dpi=100)  # Saving the chart

    # Scatter plot with IQR categories on the X-axis and ratings on the Y-axis
    plt.figure(figsize=(12, 6))
    plt_title = "Scatter Plot of Ratings by Average Episodes per Season"
    sns.scatterplot(x='avg_ep_per_season', y='vote_average', data=df, hue='avg_ep_per_season', palette='viridis', legend=False)
    plt.title(plt_title)
    plt.ylabel("Rating (Vote Average)")
    plt.xlabel("Average Episodes per Season")
    plt.ylim(0, 10)  # Setting the y-axis from 0 to 10
    plt.xlim(df['avg_ep_per_season'].min(), df['avg_ep_per_season'].max())  # Set the X-axis limits
    plt.xticks(rotation=45)
    plt.savefig(f"./output/{plt_title}.png", dpi=100)  # Saving the chart
    
    plt.close()
    
    
# Function to run the analysis
def analysis(num_bins: int = 5, votes_minimum: int = 0) -> None:
    """ 
    Runs the analysis.

    Parameters
    ----------
    num_bins : int
        The number of bins to use in the analysis, the default is 5.

    Raises
    ------
    ValueError
        If the number of bins and labels does not match.
        If the DataFrame returned by `filter_first()` is empty.

    Returns
    -------
    None

    Example
    -------
    In this example, the analysis function performs a series of operations, including filtering data, 
    creating bins based on IQR, managing outliers, and displaying the results and generating graphs.

    >>> df = pd.DataFrame({
            'name': ['Serie A', 'Serie B', 'Serie C', 'Serie D', 'Serie E'],
            'number_of_episodes': [50, 100, 200, 250, 300],
            'number_of_seasons': [2, 5, 10, 12, 15],
            'avg_ep_per_season': [25.0, 20.0, 20.0, 20.8, 25.0],
            'vote_average': [7.5, 8.0, 7.9, 7.4, 7.8],
            'popularity': [150, 250, 300, 350, 400]
        })
    >>> analysis()
    """
    if num_bins < 1:
        raise ValueError("The number of bins must be greater than 1.")
    
    df_filtered = filter_first(votes_minimum)

    if df_filtered.empty:
        raise ValueError("The filtered DataFrame is empty.")
    
    bin_iqr = bins_IQR(df_filtered)
    # Adjust bins based on IQR
    limit_bins_IQR, labels_bins_IQR = bin_iqr
    
    bin_outliers = bins_with_outliers(df_filtered, num_bins)
    # Adjust bins, taking into account outliers
    limit_outliers, labels_outliers = bin_outliers
    
    if len(limit_bins_IQR) - 1 != len(labels_bins_IQR):
        raise ValueError("The number of bins and labels for IQR does not match.")
    if len(limit_outliers) - 1 != len(labels_outliers):
        raise ValueError("The number of bins and labels for outliers does not match.")
    
    # Create the category column with pd.cut
    df_filtered['category_bin_iqr'] = pd.cut(df_filtered['avg_ep_per_season'], bins=limit_bins_IQR, labels=labels_bins_IQR)
    df_filtered['category_bin_outliers'] = pd.cut(df_filtered['avg_ep_per_season'], bins=limit_outliers, labels=labels_outliers, duplicates='drop')

    display_analysis(df_filtered)
    plot_charts(df_filtered)