First Hypothesis
================

Hypothesis:
-----------
The first hypothesis suggests that series with a smaller number of episodes per season tend to 
receive more positive ratings. This assumption is based on several factors:

1. Series with fewer episodes per season need to captivate, impress, and generate interest in a 
shorter period, which requires quick viewer engagement.
2. When well-structured, series with shorter seasons can deliver a more cohesive and concise plot, 
which generally results in higher audience satisfaction.

Analysis Methodology:
---------------------

Initially, we aimed to identify the most suitable method for classifying ratings, considering 
the presence of missing and inconsistent data. Thus, we adopted the following classification 
methodology:

* Using the interquartile range (IQR) method, which handles cases of values that deviate significantly from the standard values (outliers). This can be verified in this `link <https://yooper.com.br/blog/marketing-digital/dados-outliers-ou-dados-especificos-fora-da-curva/>`_.
* Considering all values, including outliers, to ensure the analysis accounts for both the most common series and those that deviate from the norm.

Analysis and Results:
---------------------

Contextualization: In this graph, series are categorized by the number of episodes, and the i
nterquartile range (IQR) method is used to exclude outliers, focusing on the central tendency of 
the data. This method is useful for identifying the most consistent relationship between the 
number of episodes and the average rating of the series.

.. image:: ../output/Average\ Rating\ per\ Category\ (IQR).png
 
Bar Chart: Average Rating by Category (IQR)
+++++++++++++++++++++++++++++++++++++++++++

Analysis: The bar chart categorized using the IQR method showed interesting data. Upon analyzing 
the chart, it is noticeable that the average rating of the series does not vary significantly 
across episode intervals, which may suggest that the number of episodes may not be a determining 
factor in the average rating of the series, at least based on this dataset. As all categories seem 
to fall within the same rating range (between 6 and 7), based on this chart, there is no clear 
evidence supporting the hypothesis.

Contextualization: This graph shows the average ratings (vote average) considering the presence of 
outliers, i.e., series whose characteristics (such as the number of episodes per season) deviate 
significantly from the majority. These outliers are kept in the analysis to check the impact that 
atypical series might have on the overall averages.

.. image:: ../output/Average\ Rating\ with\ outliers.png

Bar Chart: Average Rating Including Outliers
++++++++++++++++++++++++++++++++++++++++++++
Analysis: The categorized bar chart, which includes outlier values, showed significant differences 
compared to the chart categorized by the interquartile range (IQR). We observe that the average 
ratings of the episodes vary more intensely due to the presence of these outliers. Since these 
values are generally derived from a smaller number of series, they tend to present more volatile 
and less representative ratings, unlike categories that encompass a larger number of episodes, 
where averages are influenced by a broader set of series.

Contextualization: The histogram illustrates the distribution of average ratings for series, 
showing how often each rating occurs. The blue curve added to the graph demonstrates the trend 
of the distribution.

.. image:: ../output/Rating\ Distribution\ (Vote\ Average).png

Histogram: Rating Distribution
++++++++++++++++++++++++++++++

Analyzing the graph, we see that most of the points are concentrated on the left side of the chart, 
indicating that most series have a smaller number of episodes per season (mainly below 500 
episodes). Moreover, even with a varied number of episodes, most series present ratings ranging 
from moderate to high (scores between 6 and 8), suggesting a trend toward positive ratings 
regardless of the number of episodes. This suggests that, while there may be a slight trend, the 
number of episodes per season is not a determining factor for the average rating of a series.

.. image:: ../output/Scatter\ Plot\ of\ Ratings\ by\ Average\ Episodes\ per\ Season.png

Scatter: Plot of Ratings by Average Episodes per Season
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

Analyzing the graph, we see that most of the points are concentrated on the left side of the graph, 
indicating that the majority of series have a smaller number of episodes per season (mainly below 
500 episodes). Furthermore, even with a varied number of episodes, most series present ratings 
ranging from moderate to high (scores between 6 and 8), suggesting a tendency toward positive 
ratings regardless of the number of episodes. This suggests that, although there may be a slight 
trend, the number of episodes per season is not a determining factor for the average rating of 
a series.

Results:
--------
Based on the data analysis, using both the IQR method and including the outliers, there is no clear 
evidence supporting the hypothesis that series with fewer episodes per season tend to receive 
higher ratings. However, we can observe a strong tendency for the existence of a central measure 
regarding the ratings of the series, regardless of the number of episodes per season. Thus, there 
are strong indications that other factors, such as plot quality, character development, and 
production, may have a more significant impact on ratings than the number of episodes per season.

Conclusion:
-----------
While the initial hypothesis suggested that series with fewer episodes per season might be better 
rated due to a more concise and focused narrative, the data does not provide concrete evidence to 
support this assumption.