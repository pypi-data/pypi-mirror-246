import os
import tifffile as tff
import numpy as np
import pandas as pd


def get_image_dimensions(path:str):
    files = os.listdir(path)
    files = [x for x in files if '.tif' in x]
    for index, file in enumerate(files):
        image = tff.imread(path + file)
        #print('Image '+ str(index+1)+'' has the following dimesions: '+str(image.shape))
        print(' ')
        print ('Image '+ str(index+1)+', Z dimension seems to be (1): '+str(image.shape[0]))
        print ('Image '+ str(index+1)+', X dimension seems to be (2): '+str(image.shape[1]))
        print ('Image '+ str(index+1)+', Y dimension seems to be (3): '+str(image.shape[2]))
    print(' ')
    print('Please proceed to the analysis only if dimensions are correct. Otherwise you need to change the parameters specified in index values in countagen_main, following the instructions in the IMPORTANT NOTE section')
    return files

def countagen_projection(image:np.array, z_stack_index:int = 1):

    """
    image: np.array, stack of images to be processed - should include z stacks and multiple channels
    """

    import numpy as np

    projected= np.max(image, axis=z_stack_index)

    return projected

def group_channels(path,file,suffixes):
    example1=tff.imread(path+file+'_'+suffixes[0])
    image=np.zeros([len(suffixes),example1.shape[0],example1.shape[1],example1.shape[2]])
    n=0
    for s in suffixes:
        image[n,:,:,:]=tff.imread(path+file+'_'+s)
        n=n+1
    return image