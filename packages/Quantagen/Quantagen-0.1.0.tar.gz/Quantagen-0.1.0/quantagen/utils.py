import os
import tifffile as tff
import numpy as np
import pandas as pd

def extract_metrics(dataframe):
    dictionary_ = {}
    for channel_ in sorted(dataframe.channel.unique()):
        channel_list = []
        print(channel_)
        concat_df_int = dataframe[dataframe.channel == channel_]
        channel_list.append(concat_df_int.intensity.mean())
        channel_list.append(len(concat_df_int.intensity))
        dictionary_[channel_] = channel_list
    df = pd.DataFrame.from_dict(dictionary_, orient = 'index')
    df = df.reset_index()
    df = df.rename(columns = {'index':'channel',0:'mean_intensity',1:'count'})
    return df

def add_quality(concat_df,image_norm):
    concat_df['quality']=0
    for num in range(0,concat_df.shape[0]):
        arrnum=image_norm[:,concat_df.iloc[num,1],concat_df.iloc[num,0]]
        channelsel=concat_df.iloc[num,4]
        other= [i for i in list(range(0,len(arrnum))) if i not in [channelsel]]
        quality_of_spot=arrnum[channelsel]/(np.mean(arrnum[other])+0.1)
        concat_df.iloc[num,concat_df.shape[1]-1]=quality_of_spot
    return concat_df