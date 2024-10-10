Second Hypothesis
==================

The basics of the hypothesis
++++++++++++++++++++++++++++
Let's first remember our second hypothesis:
When it comes to genres, networks have different "favorites", or better said, they tend to have a 
predominant type of genre for their shows.

To start with, think of the shows as divided in groups: The label of the groups are all the network
names we have in our dataset. Then, for every "network group", we count the ocurrences of each 
genre. A show with two genres, for instance, will count as +1 for both genres. With that, we have 
a new dataset: genres by network.

Our three ways of counting: popularity, votes and frequency
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
We could, now, ask ourselves: but how do we decide which genre is the favorite? We have the network
groups, but any of them have a lot of different genres to consider. The way we'll be approaching 
this question is by considering the absolute value of the genres in three different categories, 
that we'll call "columns". We'll see if the top 10 networks - that is, the 10 networks with the 
highest value in the respective columns we will be considering - have something in common, most 
specifically their favorite genre, and, if not, we'll be able to conclude that our hypothesis is 
reasonable - or maybe not.

Frequency
---------
Here, frequency stands to "how many series of that genre have been produced". As we can filter our 
dataset as we please, we'll use the range of data that fits this criteria:

1. The networks with top 10 most frequent genres, considering just networks that have at least 100 shows
2. The same as the previous one, but considering only shows which aired, for the first time, between 2022 and 2023
3. Again, the same as before, but considering shows which aired between 2023 and 2024

You can see the result of the filtering, for each of the previous topics, in the plots below

.. image:: ../output/Most\ frequent\ genres\ by\ network.png

.. image:: ../output/Most\ frequent\ genres\ by\ network,\ from\ 2022\ to\ 2023.png

.. image:: ../output/Most\ frequent\ genres\ by\ network,\ from\ 2023\ to\ 2024.png

As you can see in the plots, some networks indeed follow a tendency to have a specific genre as 
their most frequent one (note Drama and Animation taking the scene in all the charts). But, at 
the same time, we can feel a little disappointed: the networks don't have a different genre, 
between them, as their favorite. Indeed, it seems like the other way around: the favorite genre 
of those networks appears be the same in a lot of them, what suggests the existance of a group 
of genres which are mainly prefered above all others.

Popularity
----------
Popularity is a measure used by TMDB (the online database from where our data came from), which 
calculates the importance of a show based in some statistics of the site, including:

* Number of user votes for the day
* Number of page views for the day
* Number of users who marked it as a "favourite" for the day
* Number of users who added it to their "watchlist" for the day
* Next/last episode of the show to air date
* Number of total user votes
* Previous days score

To read more, you can access their `docs page <https://developer.themoviedb.org/docs/popularity-and-trending>`_. 
That being said, let's go the the analysis.

This time, we'll take in account the top series based in their average popularity score. In short,
the filters used are:

1. The top 10 networks with most popular genres, considering just networks which have, at least, 100 shows
2. Like before, the top 10 networks with the same filters as above, but airing between 2022 and 2023
3. At last, the top 10 networks with the same filtering, but airing from 2023 to 2024

.. image:: ../output/Most\ popular\ genres\ by\ network.png

.. image:: ../output/Most\ popular\ genres\ by\ network,\ from\ 2022\ to\ 2023.png

.. image:: ../output/Most\ popular\ genres\ by\ network,\ from\ 2023\ to\ 2024.png

This time, there ins't a strong predominance of some genres above all others. But, as you may 
notice, Sci-Fi & Fantasy, along with Soap, have a high number of ocurrences: they take place in
50% of all the plots. One important thing to notice is the difference between the data we got 
from the frequency plots to the data we got here: the favorite genres aren't the same, for the
same networks! That seems odd, and even makes we doubt the veracity of our hypothesis. But, at the
same time, we could just argue that, even if these genres are more popular than Drama and 
Animation, maybe they don't have the cost-benefit necessary for the networks to produce them
massively.

Vote average
------------
Last but not least, we have vote average: it stands for the average of the ratings for each genre. 
Simple as that. For the filtering, we go as always:

1. Top 10 networks with highest vote average, considering just networks with at least 100 shows.
2. Top 10 networks following the filter above, but that aired between 2022 and 2023
3. The same as above, but airing between 2023 and 2024

.. image:: ../output/Most\ voted\ genres\ by\ network.png

.. image:: ../output/Most\ voted\ genres\ by\ network,\ from\ 2022\ to\ 2023.png

.. image:: ../output/Most\ voted\ genres\ by\ network,\ from\ 2023\ to\ 2024.png

This time, we can't see a pattern in the data. The values of the highest vote averages are very 
close from one position to another and the genres don't repeat at all. At first we can, again, 
just assume that we were wrong in speculating about this from the beggining. Or, if we insist a 
little more, we can try to find a relation between all of our data. See: this non-uniformity in 
the data can be pointing us the exaplanation for why our frequency and popularity plots haven't 
matched at all: maybe there isn't a formula to make the best shows, and it all depends on the 
singularities of the show itself. Then, if we imagine a little further, while the networks 
persists in doing the same type of shows (maybe because it's easy money, or because they're more 
specialized in certain types of productions), they also create trending series to engage their 
public or  buy the rights of some well-known shows which have a higher popularity. At last, 
there is something we could almost certainly assert: the most popular shows and the most producted 
ones are, in fact, different.