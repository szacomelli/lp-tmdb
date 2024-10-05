from filter import filter_second
import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt

def shows_by_network_count(n):
    #print(filter_second().groupby(['genres', 'networks'])['networks'].value_counts()) 
    data = filter_second().groupby(['genres', 'networks'])['networks'].value_counts().nlargest(n).reset_index()
    #debug: print(data)

    data['for_plot'] = data['networks'] + ": (" + data['genres'] + ")"

    #debug: print(data)
    data.set_index('for_plot').plot.bar(title="teste")
    
    plt.xlabel('for_plot')
    plt.ylabel('count')
    plt.show()


shows_by_network_count(60)

shows_by_network_count(250)