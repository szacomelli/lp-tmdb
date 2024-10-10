import leonado_hypothesis as ln
import dilmar_hypothesis as dm
import silvio_hypothesis as sv
import filter

#Hypothesis 1

#Hypothesis 2
sv.most_frequent_genre(10, 100)
sv.most_popular_genre(10, 100)
sv.most_voted_genre(10, 100)

sv.most_frequent_genre(10, 100, [2022,2023])
sv.most_popular_genre(10, 100, [2022,2023])
sv.most_voted_genre(10, 100, [2022,2023])
sv.most_frequent_genre(10, 100, [2023,2024])
sv.most_popular_genre(10, 100, [2023,2024])
sv.most_voted_genre(10, 100, [2023,2024])

#Hypothesis 3
dm.dilmar_hypotesis(10, 100)

