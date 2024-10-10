import leonado_hypothesis as ln
import dilmar_hypothesis as dm
import silvio_hypothesis as sv

# First Hypothesis
ln.analysis(20, 0)

# Second Hypothesis
sv.most_frequent_genre(10, 100)
sv.most_popular_genre(10, 100)
sv.most_voted_genre(10, 100)

sv.most_frequent_genre(10, 100, [2022,2023])
sv.most_popular_genre(10, 100, [2022,2023])
sv.most_voted_genre(10, 100, [2022,2023])
sv.most_frequent_genre(10, 100, [2023,2024])
sv.most_popular_genre(10, 100, [2023,2024])
sv.most_voted_genre(10, 100, [2023,2024])

# Third Hypothesis
dm.dilmar_hypothesis(10, 100)

