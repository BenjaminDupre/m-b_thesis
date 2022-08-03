# Loading Libraries
import numpy as np  # not sure for what
import scipy as sp
import pandas as pd 
#import seaborn as sb
import heartpy as hp
import os 
import matplotlib.pyplot as plt

# Loading Data
'''path = "C:/Users/dupre/Dropbox/My Mac (glaroam2-185-117.wireless.gla.ac.uk)/Documents/Research MaxPlank/P1_propioception/R_tsvr_presentation/data/"
metadat  = pd.read_csv(os.path.join(path,'meta-data.csv'),na_values=" ")'''
notebook_path = os.path.abspath("metdata_analysis.py")
metadat1  = pd.read_csv(os.path.join(os.path.dirname(notebook_path), "Data\\meta-data.csv"),na_values=" ")
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
plt.text(40,6, f'$\mu={mu:.1f},\ \sigma={sigma:.1f}$')
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
ax.legend( [f'Pre VR $\mu={mu:.2f},\ \sigma={sigma:.2f}$',f'Post VR $\mu={mu1:.2f},\ \sigma={sigma1:.2f}$'],
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
      


Questions = 'datagloves felt unnatural to wear','difficult to remember the location of the red ball',\
'difficulty in detectingand counting my heartbeat','easy to remember the location of the red ball',\
'easy to remember the location of the red ball when haptic was congruent',\
'distracted when the  haptic feedback was incongruent',\
'did not recognize the differences in haptic feedback because I was concentrated on the task',\
'haptic feedback I felt  did not influence my performance'\
,'easy to remember the location of the red ball',' in control of the virtual  hands'\
,'ball felt natural with congruent haptic feedback', 'my  performance decreased when  there was no haptic feedback'\
,'faster when the haptic feedback was given', 'felt right target to place the red ball with haptic'\
,'performance improved when there was no haptic feedback', ' ball I was holding felt  real when there was haptic  feedback'\
,'easy to remember  the location of the red ball  when there was no haptic'\
,'frustrated by the  game at times', ' easier to count my  heartbeat at the beginning of  the experiment'\
,'task was fun at times', 'my  self-perceived heartbeat  detection was better at the end  of the experiment'\
,'for a moment felt as if the virtual hands were  my own hands','felt natural as I move my  hands '\
,'data gloves have increased my  sense of presence in virtual  environment'\
,' the experiment distanced me from  my own body',' haptic feedback I received has improved my performance'\
,'the  experiment brought me closer my own body'


    
    
        
       
category_names = [ "does not apply at all" , "does not apply" ,
                  "reather not applicable" , "niether nor applicable" , 
                  "reather applies" , "applies" , "totally applies" ,]
     
results = { f'({x}) '+ Questions[x-1]  : list(np.bincount(metadat[f'post_VRF{x}'],minlength = 8)) for x in range(1,28) }

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
    labels = list(results.keys())
    data = np.array(list(results.values()))[:,1:8]
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
    

#### Getting real amount of hearbeats for the pre and the post


# bpm fuction for my heart rate files using heartpy
''' Atention:  problem when file is corrupted and has commas where not required ''' 

def get_heartcount(filepath):
    hr = pd.read_csv(filepath,sep=';',decimal=",")
    hr = hr.loc[:,'TimeElapsedArduinoBeginInMicroSec']
    try: 
        start = hr.index[hr==99999999] 
        stop =  hr.index[hr==88888888]
        hr = hr.iloc[int(start[0])+1:int(stop[0])]
    except: 
        print('Error in Series - Many Commas')
        start = hr.index[hr=='99999999'] 
        stop =  hr.index[hr=='88888888']
        hr = hr.iloc[int(start[0])+1:int(stop[0])]
        hr = [s.replace(',','.') for s in hr]
    hr = np.asarray(hr)
    hr = hr.astype(float)
    working_data, measures = hp.process(hr, 133)
    return measures['bpm']


# getting all folder 
path = "C:\\Users\\dupre\\Dropbox\\My Mac (glaroam2-185-117.wireless.gla.ac.uk)\\Documents\\Research MaxPlank\\P1_propioception\\Data_Wrangling\\Matlab Analysis\\Data_Wrangling"
all_path = os.listdir(path) 
only_dir =  [f for f in os.listdir(path) if os.path.isdir(os.path.join(path,f))]
only_dir.remove('__MACOSX')
heart_result=[]
for x in range(len(only_dir)):
    file_list_path = os.path.join(path,only_dir[x])
    only_files =  [f for f in os.listdir(file_list_path) if os.path.isfile(os.path.join(file_list_path,f))]
    for y in range(len(only_files)):
        filepath = os.path.join(file_list_path,only_files[y])
        heart_result.append(get_heartcount(filepath))
        
#### Geting Heart beat count 
filepath = "C:\\Users\\dupre\\Dropbox\\My Mac (glaroam2-185-117.wireless.gla.ac.uk)\\Documents\\Research MaxPlank\\P1_propioception\\Data_Wrangling\\Matlab Analysis\\Data_Wrangling\\tsvr06\\_20200908_14.36.45_411517_IntroceptiveLog.csv"







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
 

