#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 15:18:10 2020

@author: hoss
"""
from deepcgh import DeepCGH_Datasets, DeepCGH
import numpy as np
from _utils import display_results, get_propagate

def main():
    # Define params
    retrain = True
    frame_path = 'DeepCGH_Frames/*.mat'
    coordinates = False

    data = {
            'path' : 'DeepCGH_Datasets/Disks',
            'shape' : (512, 512, 3),
            'object_type' : 'Disk',
            'object_size' : 10,
            'object_count' : [27, 48],
            'intensity' : [0.1, 1],
            'normalize' : True,
            'centralized' : False,
            'N' : 2000,
            'train_ratio' : 1900/2000,
            'compression' : 'GZIP',
            'name' : 'target',
            }


    model = {
            'path' : 'DeepCGH_Models/Disks',
            'num_frames':5,
            'int_factor':16,
            'quantization':8,
            'n_kernels':[64, 128, 256],
            'plane_distance':0.05,
            'focal_point':0.2,
            'wavelength':1.04e-6,
            'pixel_size': 9.2e-6,
            'input_name':'target',
            'output_name':'phi_slm',
            'lr' : 1e-4,
            'batch_size' : 16,
            'epochs' : 100,
            'token' : 'DCGH',
            'shuffle' : 16,
            'max_steps' : 4000,
            # 'HMatrix' : hstack
            }


    # Get data
    dset = DeepCGH_Datasets(data)

    dset.getDataset()

    # Estimator
    dcgh = DeepCGH(data, model)

    if retrain:
        dcgh.train(dset)

    #%% This is a sample test. You can generate a random image and get the results
    model['HMatrix'] = dcgh.Hs # For plotting we use the exact same H matrices that DeepCGH used

    # Get a function that propagates SLM phase to different planes according to your setup's characteristics
    propagate = get_propagate(data, model)

    # Generate a random sample
    image = dset.get_randSample()[np.newaxis,...]
    # Get the phase for your target using a trained and loaded DeepCGH
    phase = dcgh.get_hologram(image)

    # Simulate what the solution would look like
    reconstruction = propagate(phase).numpy()

    #%% Show the results
    display_results(image, phase, reconstruction, 1)

if __name__ == "__main__":
    main()
