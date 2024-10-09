import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Function to filter and prepare the data
def filter_data(df: pd.DataFrame) -> pd.DataFrame:
    # Ensure that shows with episodes but no seasons are assigned at least one season
    df.loc[(df['number_of_episodes'] > 0) & (df['number_of_seasons'] == 0), 'number_of_seasons'] = 1
    
    # Filter out shows with no votes and no episodes
    df_filtered = df[(df['vote_count'] > 0) & (df['number_of_episodes'] > 0)].copy()
    
    # Calculate the average number of episodes per season
    df_filtered['avg_ep_per_season'] = np.floor(df_filtered['number_of_episodes'] / df_filtered['number_of_seasons'])
    
    # Drop rows with NaN values in 'vote_average'
    df_filtered = df_filtered.dropna(subset=['vote_average'])
    
    return df_filtered

# Function to adjust bins based on IQR
def bins_IQR(df: pd.DataFrame, num_bins) -> list:
    avg_ep_per_season = df['avg_ep_per_season']
    
    # Calculation of quartiles and IQR
    q1 = np.percentile(avg_ep_per_season, 25)
    q3 = np.percentile(avg_ep_per_season, 75)
    iqr = q3 - q1
    upper_limit = q3 + 1.5 * iqr  # Upper limit for outliers
    
    # Creation of equidistant intervals up to the upper limit
    bin_edges = np.linspace(avg_ep_per_season.min(), upper_limit, num_bins - 1).astype(int)
    bin_edges = np.append(bin_edges, avg_ep_per_season.max().astype(int))  # Add the maximum value as the last bin

    # Validation of the number of labels and bins
    if len(bin_edges) != num_bins:
        raise ValueError("The number of bins and labels does not match.")
    
    # Generation of labels
    labels = [f"{bin_edges[i]}-{bin_edges[i+1]-1}" for i in range(len(bin_edges)-1)]
    labels[-1] = f"{bin_edges[-2]} or more"
    
    return bin_edges, labels

def bins_with_outliers(df: pd.DataFrame, num_bins: int) -> list:
    avg_ep_per_season = df['avg_ep_per_season']
    
    # Creation of intervals
    bin_edges = np.linspace(avg_ep_per_season.min(), avg_ep_per_season.max(), num_bins).astype(int)
    
    # Generation of labels
    labels = [f"{bin_edges[i]}-{bin_edges[i+1]-1}" for i in range(len(bin_edges)-1)]
    labels[-1] = f"{bin_edges[-2]} or more"
    print(bin_edges, labels)
    
    return bin_edges, labels

# Function to display analysis and calculate metrics
def display_analysis(df: pd.DataFrame) -> None:
    # Creating a new dataframe with the relevant columns and then sorting by the average number of episodes per season
    df_filtered_final = df[['name', 'number_of_episodes', 'number_of_seasons', 'avg_ep_per_season', 'vote_average', 
                            'popularity', 'category_bin_iqr', 'category_bin_outliers']]
    df_filtered_final = df_filtered_final.sort_values(by='avg_ep_per_season', ascending=False)

    # Saving the dataframe to a CSV file
    df_filtered_final.to_csv('orderned_tmdb.csv', index=False)
    
    # Number of shows in each bin interval
    shows_per_bin_iqr = df_filtered_final['category_bin_iqr'].value_counts().sort_index()
    print(shows_per_bin_iqr)

    shows_per_bin_outliers = df_filtered_final['category_bin_outliers'].value_counts().sort_index()
    print(shows_per_bin_outliers)

    print(df_filtered_final.head(1000))
    
    print(f"Number of shows in the DataFrame: {len(df_filtered_final)}")

# Function to plot bar charts with the average ratings per bin and distribution
def plot_charts(df) -> None:
    plt.figure(figsize=(12, 6))
    mean_per_bin_iqr = df.groupby('category_bin_iqr', observed=False)['vote_average'].mean().reset_index()
    
    # Bar chart showing the average rating per category (IQR)
    sns.barplot(x='category_bin_iqr', y='vote_average', hue='category_bin_iqr', data=mean_per_bin_iqr, palette='Set2', legend=False)
    
    plt.title("Average Rating per Category (IQR)")
    plt.ylabel("Average Rating (Vote Average)")
    plt.xlabel("Episode Number Category (Bins)")
    plt.ylim(0, 10)  # Setting the y-axis from 0 to 10
    plt.xticks(rotation=45)
    plt.savefig('rating_category_iqr.png')  # Saving the chart
    plt.show()
    plt.close()

    plt.figure(figsize=(12, 6))
    mean_per_bin_outliers = df.groupby('category_bin_outliers', observed=False)['vote_average'].mean().reset_index()

    # Bar chart showing the average rating per category, including outliers
    sns.barplot(x='category_bin_outliers', y='vote_average', hue='category_bin_outliers', data=mean_per_bin_outliers, palette='Set1', legend=False)
    
    plt.title("Average Rating with Outliers")
    plt.ylabel("Average Rating (Vote Average)")
    plt.xlabel("Episode Number Category (Bins)")
    plt.ylim(0, 10)  # Setting the y-axis from 0 to 10
    plt.xticks(rotation=45)
    plt.savefig('rating_outliers.png')  # Saving the chart
    plt.show()
    plt.close()
    
    # Distribution chart of ratings (vote_average)
    plt.figure(figsize=(12, 6))
    sns.histplot(df['vote_average'], bins=20, kde=True, color='blue')
    plt.title("Rating Distribution (Vote Average)")
    plt.xlabel("Rating (Vote Average)")
    plt.ylabel("Frequency")
    plt.savefig('rating_distribution.png')  # Saving the chart
    plt.show()
    plt.close()

    plt.figure(figsize=(12, 6))

    # Scatter plot with IQR categories on the X-axis and ratings on the Y-axis
    sns.scatterplot(x='avg_ep_per_season', y='vote_average', data=df, hue='avg_ep_per_season', palette='viridis', legend=False)
    
    plt.title("Scatter Plot of Ratings by Average Episodes per Season")
    plt.ylabel("Rating (Vote Average)")
    plt.xlabel("Average Episodes per Season")
    plt.ylim(0, 10)  # Setting the y-axis from 0 to 10
    plt.xlim(df['avg_ep_per_season'].min(), df['avg_ep_per_season'].max())  # Set the X-axis limits
    plt.xticks(rotation=45)
    plt.savefig('scatter_avg_episodes_per_season.png')  # Saving the scatter plot
    plt.show()
    plt.close()
    
# Main function to run the analysis
def analysis(df: pd.DataFrame, num_bins=15) -> None:
    # Filter and prepare the data
    df_filtered = filter_data(df)
    bin_iqr = bins_IQR(df_filtered, num_bins)
    bin_outliers = bins_with_outliers(df_filtered, num_bins)
    
    # Adjust bins based on IQR
    limit_bins_IQR, labels_bins_IQR = bin_iqr

    # Adjust bins, taking into account outliers
    limit_outliers, labels_outliers = bin_outliers
    
    # Create the category column with pd.cut
    df_filtered['category_bin_iqr'] = pd.cut(df_filtered['avg_ep_per_season'], bins=limit_bins_IQR, labels=labels_bins_IQR)
    df_filtered['category_bin_outliers'] = pd.cut(df_filtered['avg_ep_per_season'], bins=limit_outliers, labels=labels_outliers)
    
    # Display analysis and calculate metrics
    display_analysis(df_filtered)
    
    # Plot charts of ratings per bins and the rating distribution
    plot_charts(df_filtered)

# Read the dataset and run the analysis
filepath = "../data/TMDB_tv_dataset_v3.csv"
df = pd.read_csv(filepath)
analysis(df)