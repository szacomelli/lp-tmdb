import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Function to filter and prepare the data
def filtrar_dados(df: pd.DataFrame):
    # Ensure that shows with episodes but no seasons are assigned at least one season
    df.loc[(df['number_of_episodes'] > 0) & (df['number_of_seasons'] == 0), 'number_of_seasons'] = 1
    
    # Filter out shows with no votes and no episodes
    df_filtered = df[(df['vote_count'] > 0) & (df['number_of_episodes'] > 0)].copy()
    
    # Calculate the average number of episodes per season
    df_filtered['media_ep_por_temp'] = np.floor(df_filtered['number_of_episodes'] / df_filtered['number_of_seasons'])
    
    # Drop rows with NaN values in 'vote_average'
    df_filtered = df_filtered.dropna(subset=['vote_average'])
    
    return df_filtered

# Função para ajustar os bins (categorias de número de episódios)
def bins_IQR(df: pd.DataFrame, num_bins):
    media_ep_por_temp = df['media_ep_por_temp']
    
    # Cálculo dos quartis e IQR
    q1 = np.percentile(media_ep_por_temp, 25)
    q3 = np.percentile(media_ep_por_temp, 75)
    iqr = q3 - q1
    lim_sup = q3 + 1.5 * iqr  # Limite superior para outliers
    
    # Criação de intervalos equidistantes até o limite superior
    bin_edges = np.linspace(media_ep_por_temp.min(), lim_sup, num_bins - 1).astype(int)
    bin_edges = np.append(bin_edges, media_ep_por_temp.max().astype(int))  # Adicionar o valor máximo como último bin

    # Validação do número de rótulos e bins 
    if len(bin_edges) != num_bins:
            raise ValueError("O número de bins e rótulos não coincide.")
    
    # Geração de rótulos
    labels = [f"{bin_edges[i]}-{bin_edges[i+1]-1}" for i in range(len(bin_edges)-1)]
    labels[-1] = f"{bin_edges[-2]} ou mais"
    
    return bin_edges, labels

def bins_with_outliers(df: pd.DataFrame, num_bins):
    media_ep_por_temp = df['media_ep_por_temp']
    
    # Criação de intervalos
    bin_edges = np.linspace(media_ep_por_temp.min(), media_ep_por_temp.max(), num_bins)

    # Validação do número de rótulos e bins 
    if len(bin_edges) != num_bins:
        raise ValueError("O número de bins e rótulos não coincide.")
    
    # Geração de rótulos
    labels = [f"{bin_edges[i]}-{bin_edges[i+1]-1}" for i in range(len(bin_edges)-1)]
    labels[-1] = f"{bin_edges[-2]} ou mais"
    print(bin_edges,labels)
    
    return bin_edges, labels

# Função para exibir análises e calcular métricas
def exibir_analise(df: pd.DataFrame):
    df_filtered_final = df[['name', 'number_of_episodes', 'number_of_seasons', 'media_ep_por_temp', 'vote_average', 'popularity', 'categoria_bin_iqr', 'categoria_bin_outliers']]
    df_filtered_final = df_filtered_final.sort_values(by='media_ep_por_temp', ascending=False)
    df_filtered_final.to_csv('ordened_tmdb.csv', index=False)
    
    # Número de séries em cada intervalo do bins
    series_por_bin_iqr = df_filtered_final['categoria_bin_iqr'].value_counts().sort_index()
    print(series_por_bin_iqr)

    series_por_bin_outliers = df_filtered_final['categoria_bin_outliers'].value_counts().sort_index()
    print(series_por_bin_outliers)

    
    print(df_filtered_final.head(10000))
    
    print(f"Number of shows in the DataFrame: {len(df_filtered_final)}")

# Função para plotar gráfico de barras com a média de avaliações por bin e distribuição
def plotar_graficos(df):
    plt.figure(figsize=(12, 6))
    mean_per_bin_iqr = df.groupby('categoria_bin_iqr')['vote_average'].mean().reset_index()
    
    # Gráfico de barras mostrando a avaliação média por categoria (IQR)
    sns.barplot(x='categoria_bin_iqr', y='vote_average', data=mean_per_bin_iqr, palette='Set2')
    
    plt.title("Média de Avaliação por Categoria (IQR)")
    plt.ylabel("Avaliação Média (Vote Average)")
    plt.xlabel("Categoria de Número de Episódios (Bins)")
    plt.ylim(0, 10)  # Definindo o eixo y de 0 a 10
    plt.xticks(rotation=45)
    plt.savefig('avaliacao_categoria_iqr.png')  # Salvando o gráfico
    plt.show()
    plt.close()

    plt.figure(figsize=(12, 6))
    mean_per_bin_outliers = df.groupby('categoria_bin_outliers')['vote_average'].mean().reset_index()

    # Gráfico de barras mostrando a avaliação média por categoria, incluindo os casos outliers
    sns.barplot(x='categoria_bin_outliers', y='vote_average', data=mean_per_bin_outliers, palette='Set1')
    
    plt.title("Média de Avaliação com Outliers")
    plt.ylabel("Avaliação Média (Vote Average)")
    plt.xlabel("Categoria de Número de Episódios (Bins)")
    plt.ylim(0, 10)  # Definindo o eixo y de 0 a 10
    plt.xticks(rotation=45)
    plt.savefig('avaliacao_outliers.png')  # Salvando o gráfico
    plt.show()
    plt.close()
    
    # Gráfico de distribuição de avaliação (vote_average)
    plt.figure(figsize=(12, 6))
    sns.histplot(df['vote_average'], bins=20, kde=True, color='blue')
    plt.title("Distribuição de Avaliações (Vote Average)")
    plt.xlabel("Avaliação (Vote Average)")
    plt.ylabel("Frequência")
    plt.savefig('distribuicao_avaliacoes.png')  # Salvando o gráfico
    plt.show()
    plt.close()

# Função principal para rodar a análise
def analise(df: pd.DataFrame, num_bins=15):
    # Filtrar e preparar os dados
    df_filtered = filtrar_dados(df)
    bin_iqr = bins_IQR(df_filtered, num_bins)
    bin_outliers = bins_with_outliers(df_filtered, num_bins)
    
    # Ajuste dos bins com base no IQR
    limite_bins_IQR, rotulos_bins_IQR = bin_iqr

    # Ajuste dos bins, levando em conta os outliers
    limite_outliers, rotulos_outliers = bin_outliers
    
    # Criação da coluna de categorias com pd.cut
    df_filtered['categoria_bin_iqr'] = pd.cut(df_filtered['media_ep_por_temp'], bins=limite_bins_IQR, labels=rotulos_bins_IQR)
    df_filtered['categoria_bin_outliers'] = pd.cut(df_filtered['media_ep_por_temp'], bins=limite_outliers, labels=rotulos_outliers)
    
    # Exibir análise e calcular métricas
    exibir_analise(df_filtered)
    
    # Plotagem dos gráficos de avaliação por bins e a distribuição de avaliações
    plotar_graficos(df_filtered)

# Leitura do dataset e execução da análise
filepath = "../data/TMDB_tv_dataset_v3.csv"
df = pd.read_csv(filepath)
analise(df)
