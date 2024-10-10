import silvio_hypothesis as sv
import leonado_hypothesis as ln
import hipotese_dilmar as dm


# First Hypothesis
ln.analysis(20, 0)


sv.most_frequent_genre(10, 100)
sv.most_popular_genre(10, 100)
sv.most_voted_genre(10, 100)

sv.most_frequent_genre(10, 100, [2022,2023])
sv.most_popular_genre(10, 100, [2022,2023])
sv.most_voted_genre(10, 100, [2022,2023])
sv.most_frequent_genre(10, 100, [2023,2024])
sv.most_popular_genre(10, 100, [2023,2024])
sv.most_voted_genre(10, 100, [2023,2024])