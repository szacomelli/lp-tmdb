import pandas as pd

filepath = "../data/TMDB_tv_dataset_v3.csv"
df = pd.read_csv(filepath)

def analise(df: pd.DataFrame, n_bins: int = 10):
    
    df.loc[(df['number_of_episodes'] > 0) & (df['number_of_seasons'] == 0), 'number_of_seasons'] = 1
    
    df_filtered = df[df['vote_count'] > 0].copy()
    df_filtered = df_filtered[df_filtered['number_of_episodes'] > 0].copy()
    
    
    df_filtered['media_ep_por_temp'] = df_filtered['number_of_episodes'] / df_filtered['number_of_seasons']

    def bins(n_bins: int):
        ep_max = df_filtered['number_of_episodes'].max()
        ep_min = df_filtered['number_of_episodes'].min()
        interval = (ep_max - ep_min) / n_bins

        return [ep_min + i * interval for i in range(n_bins + 1)]
    
    bins_ep = bins(n_bins)

    df_filtered['categorias'] = pd.cut(df_filtered['number_of_episodes'], bins=bins_ep)
    
    df_filtered = df_filtered.sort_values(by=['vote_average', 'number_of_episodes'], ascending=[False, True])
    
    df_filtered_final = df_filtered[['name', 'number_of_episodes', 'number_of_seasons', 'vote_average', 'popularity']]
    
    df_filtered_final.to_csv('ordened_tmdb.csv', index=False)
    
    dict_episodes = df_filtered.set_index('number_of_episodes')['name'].to_dict()
    # print(dict_episodes)

    print(df_filtered_final.head(100))
    
    print(f"Number of shows in the DataFrame: {len(df_filtered)}")

# Running the analysis function
analise(df)