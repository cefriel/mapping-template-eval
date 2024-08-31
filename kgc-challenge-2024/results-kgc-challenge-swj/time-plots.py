import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

TIMEOUT = 100000000

def organize_data(data, engines, mappings, metric):

    average_data = pd.DataFrame(columns = ['engine', 'mapping', metric])
    for i in range(0, len(data)):
        if data.iloc[i][metric] == "TimeOut":
            average_data.loc[len(average_data)] = [data.iloc[i]['engine'], data.iloc[i]['mapping'], math.log10(TIMEOUT)]
        else:
            value = float(data.iloc[i][metric])
            value = math.log10(1 + value)
            average_data.loc[len(average_data)] = [data.iloc[i]['engine'], data.iloc[i]['mapping'], value]
    
    ordered_data = pd.DataFrame(columns=mappings, index=engines)
    for i in range(0, len(average_data)):
        for j in range(0, len(ordered_data.index)):
            for k in range(0,len(ordered_data.columns)):
                if str(average_data.iloc[i]['engine']) == ordered_data.index[j] and str(average_data.iloc[i]['mapping']) == ordered_data.columns[k]:
                    ordered_data.iloc[j,k] = average_data.iloc[i][metric]
                    break
    #return(ordered_data)
    print(ordered_data)
    return(ordered_data.replace(np.nan, float(0)))

def plot(data, scale):

    # Create dataframe    
    engines = ['mapping-template', 'mapping-template-rml', 'flex-rml', 'rpt-sansa', 'rml-streamer'] #'rmlweaver-js','mapping-template-rml-mtl',
    colors = ['#F2BABA', '#A46593', '#2862CC', '#90AFE9', '#A5D9A5'] #'#AEF359'
    mappings = data['mapping'].dropna().unique()

    ordered_data = organize_data(data, [x.lower() for x in engines], mappings, 'elapsed_time')

    barWidth = 0.11

    rs = []
    for i in range(len(engines)):
        rs.append([x + barWidth * i for x in np.arange(len(ordered_data.columns))])

    for i in range(len(engines)):
        plt.bar(rs[i], ordered_data.values.tolist()[i], width=barWidth, color=colors[i],
                label=engines[i])

    plt.xticks([r + barWidth*2.5  for r in range(len(rs[0]))], mappings, fontsize=16)

    max_value = int(np.ceil(ordered_data.apply(pd.to_numeric, errors='coerce').max(numeric_only=True).max()))
    ticks = [str(i)+'.0' for i in range(max_value)]
    ticks.append('Timeout')
    plt.yticks(np.arange(0, len(ticks)), ticks, fontsize=16)
    plt.ylim(top=min(math.log10(10**(max_value)), math.log10(TIMEOUT)))
    ylabel = "Execution Time"
    plt.ylabel(ylabel + " (log$_{10}$(s))", fontsize=18, labelpad=10)
    plt.xlabel(scale, fontsize=18, labelpad=10)
 
    #plt.legend(engines, loc='lower center', prop={'size': 24}, ncol=len(engines), bbox_to_anchor=(0.4, -0.5))
    
    filename = "./figures/time_" + scale

    plt.savefig(filename + ".png", bbox_inches='tight', dpi=700)

    plt.clf()

    print("Finished: 'figures/time_" + scale +"'")

def handler():

    pd.set_option('future.no_silent_downcasting', True)
    scales = ['GTFS-SCALE','GTFS-HETEROGENEITY','PARAMETERS-DUPLICATES','PARAMETERS-EMPTY','PARAMETERS-JOIN-1-1','PARAMETERS-JOIN-1-N','PARAMETERS-JOIN-N-1','PARAMETERS-JOIN-N-M','PARAMETERS-MAPPINGS','PARAMETERS-RECORDS','PARAMETERS-PROPERTIES']
    for scale in scales:
        plot(pd.read_csv("./Results - " + scale + ".csv"), scale)


if __name__ == "__main__":
    handler()
