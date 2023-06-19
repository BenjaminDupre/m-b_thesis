# Loading Libraries
import numpy as np  # not sure for what
import scipy as sp
import pandas as pd 
#import seaborn as sb
#import heartpy as hp
import os 
import matplotlib.pyplot as plt
from pathlib import Path
import re

# Loading Data
'''path = "C:/Users/49177/Dropbox/My Mac (glaroam2-185-117.wireless.gla.ac.uk)/Documents/Research MaxPlank/P1_propioception/R_tsvr_presentation/data/"
metadat  = pd.read_csv(os.path.join(path,'meta-data.csv'),na_values=" ")'''
notebook_path = os.path.abspath("metdata_analysis.py")
metadat1  = pd.read_csv(os.path.join(os.path.dirname(notebook_path), Path("Data/meta-data.csv")),na_values=" ")
metadat  = metadat1.drop([14, 22])

# Getting Score test # Laterality Quotient. 
laterality = metadat.loc[:,'EHQ1':'EHQ10']
stack = laterality.stack()
stack[stack ==5] = 0
stack[stack ==2] = -1
stack[stack ==1] = -2
stack[stack ==4] = 2
stack[stack ==3] = 1
metadat['laterality_s'] = (stack.unstack().sum(axis=1)/abs(stack.unstack()).sum(axis=1))*100

# Adding a Histogram with the Age Distribution and Pie Chart With Sex 
sigma = np.std(metadat.AGE)
mu = np.mean(metadat.AGE)
explode = (0.1,0)
SEX, allvals = np.unique(metadat.SEX, return_counts=True)
#colors
colors = ['#26C281','#F5D76E']

def func(pct, allvals):
    absolute = int(np.round(pct/100.*np.sum(allvals)))
    return "{:.1f}%\n({:d} )".format(pct, absolute)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,4))
fig.suptitle('Participants Data', fontsize=18 ,x = 0.2, y = 1.01)

ax1.pie(allvals,explode=explode, colors=colors,autopct=lambda pct: func(pct, allvals),
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax1.legend( ['Femenine','Masculine'],
          title="Gender",
          loc="center left",
          bbox_to_anchor=(0.1, 0, 0.5, 1))

#ax1.plt.setp( ['Femenine','Masculine'], size=8, weight="bold")

ax1.set_title("(A) Pie Chart: Gender Composition")

n, bins, patches = plt.hist(metadat.AGE, facecolor='#26C281', alpha=0.7)
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.title(' (B) Histogram: Participants Age', loc='left')
plt.text(40,6, f"$\\mu={mu:.1f},\\ \\sigma={sigma:.1f}$")
plt.axvline(mu, color = 'r', linestyle = 'dashed', linewidth = 2)
plt.grid(True)
plt.show()

#########
pre_score = metadat.loc[:,'pre_csq1':'pre_csq16'].sum(axis=1)
post_score = metadat.loc[:,'post_csq1':'post_csq16'].sum(axis=1)
mu = np.mean(pre_score/16)
sigma = np.std(pre_score/16)
mu1 = np.mean(post_score/16)
sigma1 = np.std(post_score/16)

fig, ax = plt.subplots()
ax.hist(pre_score/16, histtype="barstacked", bins=20, facecolor='#26C281' ,alpha=0.6)
ax.hist(post_score/16, histtype="barstacked", bins=20,facecolor='#757D75', alpha=0.6)
ax.axvline(mu, color = '#26C281', linestyle = 'dashed', linewidth = 2)
ax.axvline(mu1, color = '#757D75', linestyle = 'dashed', linewidth = 2)
ax.set_title("Pre and Post Cybersicknes Questionaire")
ax.legend( [f"Pre VR $\\mu={mu:.2f},\\ \\sigma={sigma:.2f}$",f"Post VR $\\mu={mu1:.2f},\\ \\sigma={sigma1:.2f}$"],
          title="Gender",
          loc="center left",
          bbox_to_anchor=(0.5, 0.35, 0.5, 1))

plt.show()
### Comparing Two Samples 
# compare samples
stat, p = sp.stats.ttest_rel(pre_score, post_score)
print('Statistics=%.3f, p=%.3f' % (stat, p))
# interpret
alpha = 0.05
if p > alpha:
	print('Same distributions (fail to reject H0)')
else:
	print('Different distributions (reject H0)')


####### VRF Qestionaire
# Get the absolute path of the notebook file
notebook_path = os.path.abspath("metdata_analysis.py")

# Construct the path to the meta-data.csv file using os.path.join()
data_directory = os.path.join(os.path.dirname(notebook_path), "Data")
csv_file_path = os.path.join(data_directory, "meta-data.csv")

# Load the CSV file into a DataFrame
metadat1 = pd.read_csv(csv_file_path, na_values=" ")

# Drop rows with indices 14 and 22 from the DataFrame
metadat = metadat1.drop([14, 22])
#  
# The order of appearance in the list is relevant for the graph now its in desorder 
Questions = 'datagloves felt unnatural to wear','difficult to remember the location of the red ball',\
'difficulty in detecting and counting my pulse','easy to remember the location of the red ball when Haptic feedback was congruent',\
'did not recognize the differences in haptic feedback because I was concentrated on the task',\
'distracted when the  haptic feedback was incongruent',\
'the Haptic Feedback had no influence in my results',\
'easy to remember the location of the red ball',' felt in control of the virtual hands'\
,'ball felt natural to place with congruent haptic feedback', 'my  performance decreased when  there was no haptic feedback'\
,'faster when the haptic feedback was given', 'felt right target to place the red ball with haptic'\
,'performance improved when there was no haptic feedback', ' ball I was holding felt  real when there was haptic  feedback'\
,'easy to remember  the location of the red ball  when there was no haptic'\
,'frustrated by the  game at times', ' easier to count my  heartbeat at the beginning of  the experiment'\
,'task was fun at times', 'my  self-perceived heartbeat  detection was better at the end  of the experiment'\
,'for a moment felt as if the virtual hands were  my own hands','It felt natural as I moved my hands toward the templates',\
'I lost track of time because I was so focused on completing the task','data gloves have increased my  sense of presence in virtual  environment'\
,' the experiment distanced me from  my own body',' haptic feedback I received has improved my performance'\
,'the  experiment brought me closer to my own body'


    
    
        
       
category_names = [ "does not apply at all" , "does not apply" ,
                  "reather not applicable" , "niether nor applicable" , 
                  "reather applies" , "applies" , "totally applies" ,]
     
results = {
    f'({x}) ' + Questions[x-1]: {
        'counts': list(np.bincount(metadat[f'post_VRF{x}'], minlength=8)),
        'mean': round(np.mean(metadat[f'post_VRF{x}']),2),
        'stand dev': round(np.std(metadat[f'post_VRF{x}']),2),
        'median': round(np.median(metadat[f'post_VRF{x}']),2)

    }
    for x in range(1, 28)
}
def survey(results, category_names):
    """
    Parameters
    ----------
    results : dict
        A mapping from question labels to a list of answers per category.
        It is assumed all lists contain the same number of entries and that
        it matches the length of *category_names*.
    category_names : list of str
        The category labels.
    """
    labels = [
    f"{key} ( Mdn:{results[key]['median']}, \u03BC: {results[key]['mean']}, \u03C3:{results[key]['stand dev']})"
    for key in results.keys()
]
    #data = np.array(list(results[key]['counts']))[:,1:8]
    data = np.array([result['counts'] + [0] * (8 - len(result['counts'])) for result in results.values()])[:,1:8]
    data_cum = data.cumsum(axis=1)
    category_colors = plt.colormaps['RdYlGn'](
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(17, 12))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        rects = ax.barh(labels,widths, left=starts, height=0.5,
                        label=colname, color=color)

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
            # format the number of decimal places and replace 0 with an empty string
        #bar_labels = widths
        
        bar_labels = np.char.replace(list(map(str,widths)),'0','')  #widths[j] if widths[j] > 0 for j in enumerate(widths) else ''  
        ax.bar_label(rects,labels=bar_labels ,label_type='center', color=text_color)
    ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')

    return fig, ax


survey(results, category_names)
plt.show()


# =============================================================================
# #### Getting real amount of hearbeats for the pre and the post
# 
# 
# # bpm fuction for my heart rate files using heartpy
# ''' Atention:  problem when file is corrupted and has commas where not required ''' 
# import warnings
# warnings.filterwarnings("error")
# def get_heartcount(filepath):
#     hr = pd.read_csv(filepath,sep=';',decimal=",")
#     hr = hr.loc[:,'TimeElapsedArduinoBeginInMicroSec']
#     try: 
#         start = hr.index[hr==99999999] 
#         stop =  hr.index[hr==88888888]
#         hr = hr.iloc[int(start[0])+1:int(stop[0])]
#     except: 
#         print(f'Error in Series {x} file {y}- Many Commas \n')
#         start = hr.index[hr=='99999999'] 
#         stop =  hr.index[hr=='88888888']
#         hr = hr.iloc[int(start[0])+1:int(stop[0])]
#         hr = [s.replace(',','.') for s in hr]
#     hr = np.asarray(hr)
#     hr = hr.astype(float)
#     try:
#         working_data, measures = hp.process(hr, 133)
#         
#     except:
#         'Noisy Data'
#         if min(hr) < 0  and max(hr) < 0:
#             hr = hr*-1
#             scaled = hp.scale_sections(hr, sample_rate=133, windowsize=266)
#             working_data, measures = hp.process(scaled, 133)
#         else:
#             print(f'Signal not counted in {only_dir[x]} file {only_files[y]}')
#     return measures['bpm']
# 
# 
# # getting all folder 
# #path = "C:\\Users\\49177\\Dropbox\\My Mac (glaroam2-185-117.wireless.gla.ac.uk)\\Documents\\Research MaxPlank\\P1_propioception\\Data_Wrangling\\Matlab Analysis\\Data_Wrangling"
# path = "/Users/benjamin/Documents/Data_Wrangling/"
# all_path = os.listdir(path) 
# only_dir =  [f for f in os.listdir(path) if os.path.isdir(os.path.join(path,f))]
# only_dir.remove('__MACOSX')
# heart_result=[]
# for x in range(len(only_dir)):
#     file_list_path = os.path.join(path,only_dir[x])
#     only_files =  [f for f in os.listdir(file_list_path) if os.path.isfile(os.path.join(file_list_path,f))]
#     for y in range(len(only_files)):
#         filepath = os.path.join(file_list_path,only_files[y])
#         heart_result.append(get_heartcount(filepath))
#         
# =============================================================================
#### Geting Heart beat count 
filepath = "C:\\Users\\49177\\Dropbox\\My Mac (glaroam2-185-117.wireless.gla.ac.uk)\\Documents\\Research MaxPlank\\P1_propioception\\Data_Wrangling\\Matlab Analysis\\Data_Wrangling\\tsvr06\\_20200908_14.36.45_411517_IntroceptiveLog.csv"

#####
##### Multivariate Analysis with behavioral VR Data 
#####

# Loading VR data 
behaviour  = pd.read_csv(os.path.join(os.path.dirname(notebook_path), Path("Data/behavior.csv")),na_values=" ")
behaviour["Stimulus"].value_counts()
behaviour["set"].value_counts()
# Removing failed trails 
behaviour_clean = behaviour.drop(behaviour[behaviour.set==0].index)
behaviour_clean = behaviour.drop(behaviour[behaviour.Stimulus==0].index)

# descriptive overall view on conditions 
behaviour_clean.groupby("Stimulus").mean(numeric_only=True)
behaviour_clean["Stimulus"].value_counts()

'''
#ANOVA oneway
#F, p = sp.stats.f_oneway(behaviour_clean[behaviour_clean.Stimulus==1],
#                      behaviour_clean[behaviour_clean.Stimulus==1],
#                      behaviour_clean[behaviour_clean.Stimulus==1])
# Box Plot 
#Create a boxplot
behaviour_clean.boxplot('diff', by='Stimulus', figsize=(12, 8))

ctrl = behaviour_clean['weight'][data.group == 'ctrl']

grps = pd.unique(data.group.values)
d_data = {grp:data['weight'][data.group == grp] for grp in grps}

k = len(pd.unique(data.group))  # number of conditions
N = len(data.values)  # conditions times participants
n = data.groupby('group').size()[0] #Participants in each condition

# distribution of accuracy percentage by condition 
plt.style.use('default')

a = behaviour_clean[behaviour_clean.Stimulus==1]
b = behaviour_clean[behaviour_clean.Stimulus==2]
c = behaviour_clean[behaviour_clean.Stimulus==3]


fig, ax = plt.subplots()
plt.hist(a['diff'],
            histtype="stepfilled", bins=50, alpha=0.5, density=True)
plt.hist(b['diff'],
            histtype="stepfilled", bins=50, alpha=0.5, density=True)
plt.hist(c['diff'],
            histtype="stepfilled", bins=50, alpha=0.5, density=True)
ax.set_title("'bmh' style sheet")

plt.show()

# distribution of reponse time by condition 
a = behaviour_clean[behaviour_clean.Stimulus==1]

trying to show a grpah with the time difference.
'''




'''  
 
:prefix[a] + ' csq16'

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
 
''' Answering Zeynep questions '''
smaller_behaviour= behaviour_clean.loc[:,["ptcp","accuracy"]].groupby('ptcp' , as_index = False).sum()
metadat["PARTICIPANT ID"] = metadat["PARTICIPANT ID"].str.lower() 
metadat["PARTICIPANT ID"] = [s.replace('_', '') for s in metadat["PARTICIPANT ID"]]
metadat = metadat.rename(columns={"PARTICIPANT ID":"ptcp"})
metadat_behaviour = pd.merge(metadat,
         smaller_behaviour,
         on="ptcp",
         how='left')
pozoso = metadat_behaviour.loc[:,["post_VRF2","accuracy"]].groupby(["post_VRF2"]).mean()