from scipy import ndimage
import numpy as np
from simulated_hardware import current_time

def simple_integration(image, num_bins=_history['integration_bins']):
    sx, sy = image.shape
    x_, y_ = np.mgrid[-sx // 2 : sx // 2, -sy // 2 : sy // 2]
    r = np.hypot(x_, y_)
    rbin = (num_bins * r / r.max()).astype(np.int)
    radial_mean = ndimage.mean(image, labels=rbin, index=np.arange(1, rbin.max() + 1))
    return radial_mean

def look_at_watch():
    print ('the current time is '+str(current_time()))
    
def normalized_residual(data, ideal):
    return sum(abs(data-ideal))/len(data)

######################

def dark_light_collection(sample_num, num_lights = 1):
    uids = []
    #close shutter if not already closed
    yield from light(False)
        
    #move to desired sample
    yield from load_sample(sample_num)
    
    #take dark image
    uid = yield from count([detector])
    uids.append(uid)
    
    #open shutter
    yield from light(True)
    
    #take light image
    for i in range(num_lights):
        uid = yield from count([detector])
        uids.append(uid)
    
    #close shutter to be nice to detector
    yield from light(False)
    return uids

def process_data(pair, num_lights = 1, return_light = False, return_dark = False):
    #assuming pair is tuple
    my_dark = catalog[pair[0]].primary.read().detector_image[0]
    
    if return_dark:
        return simple_integration(my_dark)
    
    dark_subbed_list = []
    
    for i in range(1,num_lights+1):
        this_light = catalog[pair[i]].primary.read().detector_image[0]
        
        if return_light:
            dark_subbed_list.append(this_light)
        else:
            dark_subbed_list.append(this_light - my_dark)
    
    if num_lights == 1:
        return simple_integration(dark_subbed_list[0])
    
    else: # more than one
        int_list = []
        for j in range(len(dark_subbed_list)):
            int_list.append(simple_integration(dark_subbed_list[j]))
    
        return np.array(int_list).T

def make_ideal_data(sample_num):
    _history['perfect_data'] = True

    perfect_pair = RE(dark_light_collection(sample_num))    

    this_light = catalog[perfect_pair[1]].primary.read().detector_image[0]

    perfect_int = simple_integration(this_light)

    _history['perfect_data'] = False
    
    return perfect_int

def retrieve_im(num):
    return catalog[num].primary.read().detector_image[0]


#startup things

perfect_int1 = make_ideal_data(1)
perfect_int2 = make_ideal_data(2)
perfect_int3 = make_ideal_data(3)
perfect_int4 = make_ideal_data(4)
history_reset()
kkk
q = np.linspace(.1,25, _history['integration_bins'])

d = 2.0*np.pi/q


def hard_mode():
    history_reset()
    _history['decay_a'] = 50
    _history['noise'] = 1000
    _history['panel_wl'] = _history['panel_wl_hard'] 
    