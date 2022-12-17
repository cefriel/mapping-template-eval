import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

def organize_data(data, engines, mappings):

    average_data = pd.DataFrame(columns = ['engine', 'mapping', 'elapsed_time'])
    for i in range(0, len(data)-2):
        if (data.iloc[i]['engine'] == data.iloc[i+1]['engine'] and data.iloc[i]['engine'] == data.iloc[i+2]['engine']):
            if (data.iloc[i]['mapping'] == data.iloc[i+1]['mapping'] and data.iloc[i]['mapping'] == data.iloc[i+2]['mapping']):
                if data.iloc[i]['elapsed_time'] == "TimeOut" or data.iloc[i+1]['elapsed_time'] == "TimeOut" or data.iloc[i+2]['elapsed_time'] == "TimeOut":
                    time_outs = []
                    for j in range (0,3):
                        time_outs.append(float(data.iloc[i+j]['elapsed_time'].replace("TimeOut", "100000")))

                    av_elapsed_time = (time_outs[0] + time_outs[1] + time_outs[2])/3
                    average_data.loc[len(average_data)] = [data.iloc[i]['engine'], data.iloc[i]['mapping'], math.log10(1 + av_elapsed_time)]
                else:
                    av_elapsed_time = (float(data.iloc[i]['elapsed_time']) + float(data.iloc[i+1]['elapsed_time']) + float(data.iloc[i+2]['elapsed_time']))/3
                    average_data.loc[len(average_data)] = [data.iloc[i]['engine'], data.iloc[i]['mapping'], math.log10(1 + av_elapsed_time)]    
            else:
                next
        else:
            next
    
    ordered_data = pd.DataFrame(columns = mappings, index=engines)
    for i in range(0, len(average_data)):
        for j in range(0, len(ordered_data.index)):
            for k in range(0,len(ordered_data.columns)):
                if str(average_data.iloc[i]['engine']).lower() == ordered_data.index[j] and str(average_data.iloc[i]['mapping']).lower() == ordered_data.columns[k]:
                    ordered_data.iloc[j,k] = average_data.iloc[i]['elapsed_time']
                    break
    #return(ordered_data)
    return(ordered_data.replace(np.nan, 0))


def plot(data, scale):

    # Create dataframe     
    engines = ['rmlmapper', 'morph-kgc', 'mapping-template', 'mapping-template-nj']
    mappings = ['gtfs-csv', 'gtfs-xml', 'gtfs-json']
    ordered_data = organize_data(data, [x.lower() for x in engines], mappings)

    #print(ordered_data)

    barWidth = 0.11

    r1 = np.arange(len(ordered_data.columns))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth * 2 for x in r1]
    r4 = [x + barWidth * 3 for x in r1]

    plt.bar(r1, ordered_data.values.tolist()[0], width=barWidth, color='#F2BABA',#F2BABA
                label='rmlmapper')
    plt.bar(r2, ordered_data.values.tolist()[1], width=barWidth, color='#A46593',#A46593
                label='morph-kgc')
    plt.bar(r3, ordered_data.values.tolist()[2], width=barWidth, color='#2862CC',#2862CC
                label='mapping-template')
    plt.bar(r4, ordered_data.values.tolist()[3], width=barWidth, color='#90AFE9',#90AFE9
                label='mapping-template-nj')


    plt.xticks([r + barWidth*2.5  for r in range(len(r1))], mappings, fontsize=12)

    plt.yticks(np.arange(0, 6), ('0.0', '1.0', '2.0', '3.0', '4.0', 'Timeout'), fontsize=12)
    plt.ylim(top=5)
    plt.ylabel("Time (log$_{10}$(s))", fontsize=12)
    plt.xlabel("Mapping", fontsize=12)
 
    plt.legend(engines, loc='lower center', prop={'size': 10}, ncol=4, bbox_to_anchor=(0.4, -0.34))
        
    plt.savefig("./figures/time_" + scale + ".png", bbox_inches='tight', dpi=700)

    plt.clf()

    print("Finished: 'figures/time_" + scale +"'")

def handler():

    scales = ['GTFS-1', 'GTFS-10', 'GTFS-100']
    for scale in scales:
        plot(pd.read_csv("./Results - Time - " + scale + ".csv"), scale)



if __name__ == "__main__":
    handler()
