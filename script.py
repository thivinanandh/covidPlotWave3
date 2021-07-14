# %%

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import calendar
from datetime import datetime, date

from setup import *

def setupDate(val):
    return 0


## dictionary to store the dataframes for each of the 934 iterations 
CovidPopulationDataFrame = {}

#Get the Start Date 


### loop over Foldernames
for folder in G_FOLDERNAME:
    CovidPopulationDataFrame[folder] = pd.read_csv(folder + "/" + "PopulationData/" + "CovidPopulation.data", delimiter=" ", header=1)


## Get a cumuliative value of total infected  ["TOTAL"]



## set up the date innthe ["Days"] column

print( CovidPopulationDataFrame[G_FOLDERNAME[3]]["Total"] )


# my_date = datetime.strptime(G_startDate, "%d-%m-%y")
size  = CovidPopulationDataFrame[G_FOLDERNAME[3]]["Total"].size
X = np.linspace(0,size,size)
plt.plot(X, CovidPopulationDataFrame[G_FOLDERNAME[3]]["Total"] )


a = CovidPopulationDataFrame[G_FOLDERNAME[0]]

## plot the frequency for date of peak






# %%
