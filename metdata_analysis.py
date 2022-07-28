# Loading Libraries
import numpy as np  # not sure for what
import scipy as sp
import pandas as pd 
import seaborn as sb
import os 
import matplotlib.pyplot as plt

# Loading Data
'''path = "C:/Users/dupre/Dropbox/My Mac (glaroam2-185-117.wireless.gla.ac.uk)/Documents/Research MaxPlank/P1_propioception/R_tsvr_presentation/data/"
metadat  = pd.read_csv(os.path.join(path,'meta-data.csv'),na_values=" ")'''
notebook_path = os.path.abspath("metdata_analysis.py")
metadat  = pd.read_csv(os.path.join(os.path.dirname(notebook_path), "Data\\meta-data.csv"),na_values=" ")
# Getting Score test
    # Laterality Quotient. 
laterality = (metadat[['EHQ1',
                 'EHQ2',
                 'EHQ3',
                 'EHQ4',
                 'EHQ5',
                 'EHQ6',
                 'EHQ7',
                 'EHQ8',
                 'EHQ9',
                 'EHQ10']]-3)*25 
metadat["laterality"] =laterality.sum(axis=1)
metadat.drop(22)

# Adding a Histogram with the Age Distribution and Pie Chart With Sex 
sigma = np.std(metadat.AGE)
mu = np.mean(metadat.AGE)
explode = (0.1,0)
SEX, allvals = np.unique(metadat.SEX, return_counts=True)

def func(pct, allvals):
    absolute = int(np.round(pct/100.*np.sum(allvals)))
    return "{:.1f}%\n({:d} )".format(pct, absolute)

fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle('Participants Data', x= 0)

ax1.pie(allvals,explode=explode, autopct=lambda pct: func(pct, allvals),
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax1.legend( ['Femenine','Masculine'],
          title="Gender",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))

#ax1.plt.setp( ['Femenine','Masculine'], size=8, weight="bold")

ax1.set_title("Matplotlib bakery: A pie")

n, bins, patches = plt.hist(metadat.AGE, facecolor='g', alpha=0.75)
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.title('Histogram of Participants Age')
plt.text(40,6, f'$\mu={mu:.1f},\ \sigma={sigma:.1f}$')
plt.axvline(mu, color = 'r', linestyle = 'dashed', linewidth = 2)
plt.grid(True)

plt.show()
'''   
# Geting pre-Simulator Sickness Questionnaire scores 
# Scoring method from "Simulator Sickness Questionnaire: An Enhanced Method for Quantifying Simulator Sickness"
pre = metadat[['pre_csq1',
                     'pre_csq2',
                     'pre_csq3',
                     'pre_csq4',
                     'pre_csq5',
                     'pre_csq6',
                     'pre_csq7',
                     'pre_csq8',
                     'pre_csq9',
                     'pre_csq10',
                     'pre_csq11',
                     'pre_csq12',
                     'pre_csq13',
                     'pre_csq14',
                     'pre_csq15',
                     'pre_csq16']]
pre -1 

pre.loc[pre['pre_csq1']==1, :] = pre.loc[pre['pre_csq1']==1,:]*9.54


pre == 2, 7.58
pre = 3, 13.92
#TS = np.sum()
metadat["pre"] =pre.sum(axis=1)


# Geting post Simulator Sickness Questionnaire scores 
# Scoring method from "Simulator Sickness Questionnaire: An Enhanced Method for Quantifying Simulator Sickness"
post = metadat[['post_csq1',
                 'post_csq2',
                 'post_csq3',
                 'post_csq4',
                 'post_csq5',
                 'post_csq6',
                 'post_csq7',
                 'post_csq8',
                 'post_csq9',
                 'post_csq10',
                 'post_csq11',
                 'post_csq12',
                 'post_csq13',
                 'post_csq14',
                 'post_csq15',
                 'post_csq16']]
metadat["post"] =post.sum(axis=1)


# Geting Experiment VR Questionaire 
list(metadat.columns) # Are they all on the same 'direction'?
vr_quest = metadat[['post_VRF1',
                 'post_VRF2',
                 'post_VRF3',
                 'post_VRF4',
                 'post_VRF5',
                 'post_VRF6',
                 'post_VRF7',
                 'post_VRF8',
                 'post_VRF9',
                 'post_VRF10',
                 'post_VRF11',
                 'post_VRF12',
                 'post_VRF13',
                 'post_VRF14',
                 'post_VRF15',
                 'post_VRF16',
                 'post_VRF17',
                 'post_VRF18',
                 'post_VRF19',
                 'post_VRF20',
                 'post_VRF21',
                 'post_VRF22',
                 'post_VRF23',
                 'post_VRF24',
                 'post_VRF25',
                 'post_VRF26',
                 'post_VRF27',]]

metadat["vr_quest"] =vr_quest.sum(axis=1)

# difference between pre and post 
metadat[['post']].sub(metadat['pre'], axis=0)

# Scatter Plot 
sb.pairplot(metadat[['post','pre','laterality']])

# Running PCA 

'''
 

