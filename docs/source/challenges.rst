Challenges
==========

The challenges encountered in the production of the analyses are the most expected ones, when 
dealing with dataframes downloaded on-line. Some of them are:

* Cleaning invalid rows 
        As in ``number_of_episodes``, which could came with value 0.
* Non-padronized columns 
        As in ``networks``, where one show could have multiple values for the field.
* Establishing arguments for filtering functions
        As in ``filter_second()``, where we came to the conclusion it would be better to pass a minimum number of shows per network.
* Dealing with outliers 
        As in the third hypothesis.

In summary, we dealed with the most common types of problems in this project.