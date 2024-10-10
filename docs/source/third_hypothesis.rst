Third Hypothesis
================

The third hypothesis is: "Given a rating interval, popularity varies according to the streaming 
service (network)." The code that tests this hypothesis uses the function "third_filter" from the 
"filter.py" file to remove rows of series with low vote counts and streaming services with a small 
total number of series. Then, it generates multiple plots for each rating average interval, 
grouping the streaming services by the average popularity of their series.

Filtering and tests
--------------------

We made some tests of how the data behavior after the filter function, with both parameters set to 
0 (meaning only values greater than 1 are considered), we found that 47,000 lines were preserved. 
However, increasing the values slightly to 10 in both parameters cases caused a drastic reduction 
to 8,800 lines, indicating that a large portion of the data comes from lesser-known services and 
shows. To focus on the more interesting streaming services and meaningful data, we change the 
parameters to 10 for series per service and 100 for votes per series, which resulted in a dataset 
of 2,100 lines.

The graphs obtained
-------------------

.. image:: ./output/graph0

.. image:: ./output/graph1

.. image:: ./output/graph2

.. image:: ./output/graph3

.. image:: ./output/graph4

.. image:: ./output/graph5

.. image:: ./output/graph6


Results from data
-----------------

The first three graphs are not useful since the intervals are almost empty. However, the others can 
provide interesting insights. If we ignore the one or two highest results from each graph, a 
continuity pattern seems to emerge, indicating that they can be approximated by a function. 
Moreover, the most well-known streaming services, such as Netflix, Prime Video, HBO, and Disney+, 
are not the ones with the highest average popularity, probably because they have many tv shows with 
low popularity, decreasing the average popularity, while other networks not so known have less tv 
show, but very popular, also the outliers shows, like "Greys anatomy" can change drastically the 
average popularity. Another observation is that streaming services typically do not maintain a 
consistent popularity across different intervals of rating.

Discussions and hypothesis results
----------------------------------

From the graphs we can see that the average popularity changes through the different networks, 
and the data do not looks to have a linear or random distribution, but forms a exponencial or 
Power law distribution, where few networks have a large popularity and most have a average or 
lower popularity.