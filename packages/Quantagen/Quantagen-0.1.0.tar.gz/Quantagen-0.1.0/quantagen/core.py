import os
import tifffile as tff
import numpy as np
import pandas as pd
from .image_processing import get_image_dimensions, countagen_projection, group_channels

def countagen_main(
                    image:np.array,
                    channel_index:int = 0,
                    z_stack_index:int = 1,
                    threshold:float = 1.3,
                    run_rolling_ball:bool = True,
                    footprint_value:int = 2,
                    max_radius:int = 30,
                    min_radius:int = 1,
                    quantile_to_filter:float = 0.4,
                    plot_blobs:bool = True,
                    cmap_im:str = 'gray',
                    mult_factor:int = 20,
                    cmap_spots:str = 'Reds',
                   save_figure=True,
                   path_file=None,
                alpha_spots:float = 0.4,
                    channels=None):

    import numpy as np
    import pandas as pd

    projected = countagen_projection(image, z_stack_index)
    tff.imwrite(path_file+'_projected.tif',projected)##########adding saving projected files ###########################
    spots_ = []
    projected_norm=np.zeros(projected.shape)
    for im in range(projected.shape[0]):
        print(im)
        spots_df,norm_image = countagen_spot_detection(
            image = projected[im],
            threshold = threshold,
            run_rolling_ball = run_rolling_ball,
            footprint_value = footprint_value,
            max_sigma = (max_radius**2)/2,
            min_sigma=  (min_radius**2)/2,
            quantile_to_filter = quantile_to_filter,
            plot_blobs = plot_blobs,
            cmap_im = cmap_im,
            mult_factor = mult_factor,
            cmap_spots = cmap_spots,
            alpha_spots = alpha_spots,
            path_file=path_file+'_'+str(channels[im]))
        projected_norm[im]=norm_image
        #spots_l[:, 2] = spots_l[:, 2] * sqrt(2)
        try:
            spots_df['channel'] = im
        except:
            print('not possible')
        spots_.append((spots_df))
    concat_df = pd.concat(spots_)
    print(concat_df.value_counts('channel'))


    return concat_df,projected_norm

def countagen_spot_detection(
                    image:np.array,
                    threshold:float = 1.5,
                    run_rolling_ball:bool = True,
                    footprint_value:int = 2,
                    max_sigma:int = 30,
                    min_sigma:int = 2,
                    quantile_to_filter:float = 0.4,
                    plot_blobs:bool = False,
                    cmap_im:str = 'gray',
                    mult_factor:int = 20,
                    cmap_spots:str = 'Reds',
                    alpha_spots:float = 0.4,
                    path_file=str,
                  ):
    print(image.shape)
    import numpy as np
    from skimage.feature import blob_log
    from skimage import restoration, morphology
    import matplotlib.pyplot as plt
    ####################################################################################################################################
    if run_rolling_ball == True:
        # do background substraction by rolling ball
        background = restoration.rolling_ball(image)
        image = image - background
    else:
      image = image
    ####################################################################################################################################
    # start by applying morphological filter
    footprint = morphology.disk(footprint_value)
    image = morphology.white_tophat(image, footprint)
    image_norm=image/np.percentile(image,70)
    plt.rc_context({'figure.figsize': (40, 40), 'figure.dpi':100})
 #   print(np.percentile(image_norm,99))
 #   plt.figure()
 #  bins=int(np.round(5*np.percentile(image_norm[0:np.round(image_norm.shape[0]/100),0:np.round(image_norm.shape[1]/100)],99))+1)
 #   plt.hist(image_norm[0:np.round(image_norm.shape[0]/100),0:np.round(image_norm.shape[1]/100)],bins,log=True)
 #   plt.xlim([0,np.percentile(image_norm[0:np.round(image_norm.shape[0]/100),0:np.round(image_norm.shape[1]/100)],99)])
 #   plt.axvline(x = threshold, color = 'r', label = 'Threshold used')
 #   plt.title('Pixel values in the image (to define threshold)')
 #   plt.xlabel('relative intensity')
 #   plt.ylabel('number of pixels')
    ####################################################################################################################################
    # find blobs using Laplacian of Gaussian (LoG)
    spots_l = blob_log(image_norm, max_sigma=max_sigma, num_sigma=round(max_sigma-min_sigma), threshold=threshold,min_sigma=min_sigma)
    ####################################################################################################################################
    # extract metadata for each spot
    y_inds = spots_l[:, 0].astype(int)
    x_inds = spots_l[:, 1].astype(int)
    radius = np.round(spots_l[:, 2] * np.sqrt(2))
    intensities = image[tuple([y_inds, x_inds])]

    # create spot dataframe
    spot_data = pd.DataFrame(
                data={'x':x_inds,
                    'y':y_inds,
                    'intensity':intensities,
                    'radius':radius,}
            )
    # remove spots based on intensity
    spot_data_filt = spot_data#[spot_data.intensity > spot_data.intensity.quantile(quantile_to_filter)]
    print('The number of spots detected in your image is: '+ str(len(spot_data_filt)))
    if plot_blobs == True:
        with plt.rc_context({'figure.figsize': (40, 40), 'figure.dpi':100}):
            plt.figure()
            plt.imshow(image*mult_factor, cmap = cmap_im)
            sc = plt.scatter(spot_data_filt['x'], spot_data_filt['y'],
                             s = spot_data_filt['radius']*100,
                             c = spot_data_filt['intensity'],
                             cmap = cmap_spots,
                             alpha = alpha_spots)
            plt.colorbar(sc, shrink= 0.5)
        #plt.savefig(path_file[:]+'_blobs_detected.pdf')
        plt.show()
    return spot_data,image_norm