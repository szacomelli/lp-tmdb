from filter import filter_third
import matplotlib.pyplot as plt # type: ignore
import seaborn as sns # type: ignore
import pandas as pd # type: ignore
import numpy as np # type: ignore

def dilmar_hypotesis(shows_minimum : int, votes_minimum : int):
    """
    Cria gráficos, para varios intervalos de "vote_average", com o eixo x sendo "networks" e o eixo y "popularity"

    Parameters
    ----------
    shows_minimum : int
        A quantidade minima que séries que uma network precisa ter.
    votes_minimum : int
        A quantidade minima de "vote_count" que uma series precisa

    Examples
    --------
    >>> dilmar_hypotesis(10, 150)
    $
    >>> dilmar_hypotesis(0, 1000)
    $

    Notes
    -----
    Retorna os gráficos em png.
    """

    df = filter_third(shows_minimum,votes_minimum)
    df = df[['name', 'vote_count', 'vote_average', 'popularity', 'networks']]
    # Recebe da função filter_third limpo e então guarda apenas as coluna úteis.

    df['networks'] = df['networks'].str.split(',')
    df = df.explode('networks')
    # Dividi as linhas que tem mais de uma network em linhas distintas identicas porém cada uma com um network distinto

    lower_bound = df['vote_average'].min() - 0.1
    upper_bound = df['vote_average'].max() + 0.1
    number_bins = int(np.ceil(np.log2(len(df)) + 1))
    # Encontra o upper bound, lower bound e o número de bins, 
    # o lower_bound e o upper_bound são subtraidos e somados 0.1 
    # para nenhuma série ficar na borda do intervalo e não entrar em nenhum.
    # Foi usado a regra de Sturges para calcular a quantiade de bins.

    bins = range(number_bins)*(upper_bound -lower_bound)/(number_bins - 1) + lower_bound
    bins_intervals = [f"[{round(bins[i], 2)} - {round(bins[i+1], 2)}]" for i in range(len(bins) - 1)]
    # Calcula os bins dividindo o intervalo da menor a maior nota em intervalos iguais.
    # Então faz um array de strings que nomeam cada intervalo.

    df['labels'] = pd.cut(df['vote_average'], bins = bins, labels = bins_intervals, right = True)
    df = df.groupby(['labels', 'networks'], observed = True)['popularity'].mean().reset_index()
    df = df.sort_values(by = ['popularity'], ascending=[True])
    # Rotula cada linha a seu devido intervalo, então juntão as linhas com mesmo rótulo
    # e network fazendo a média da coluna popularity, então organiza por ordem crescente.

    for i in bins_intervals:
        df_filtrado = df[df['labels'] == i]
        sns.barplot(x='networks', y='popularity', data = df_filtrado)
        plt.xticks(rotation=45, ha='right', fontsize = 10)
        plt.savefig(f'grafico{bins_intervals.index(i)}.png')
        fig_legend = plt.figure(figsize=(25, 10))
    # Faz um grafico para cada intervalo

dilmar_hypotesis(10, 150)

