"""
=== scansnap ===

Acquire a set of through-focus images of the pump and probe beams by moving a
stage-mounted camera. The camera is controlled via FLIR Spinaker API, and the
stage is controlled using HARPIA API.

Stock dependencies: numpy, matplotlib, urrlib, time
Custom dependencies: HarpiaAPI

Author: Lukas Kontenis
Copyright (c) 2019-2020 Light Conversion
All rights reserved.
www.lightcon.com
"""
import clr
import time
import os
import sys

import PySpin

import numpy as np

import matplotlib.pyplot as plt

from lightcon.harpia import harpia

def GetImageWithAE(cam):
    max_exposure = 32700
    min_exposure = 45.6
    exposure = cam.ExposureTime.GetValue()
    while(1):
        cam.AcquisitionStart()
        image_result = cam.GetNextImage()
        image_result.Release()
        cam.AcquisitionStart()
        image_result = cam.GetNextImage()
        image_result.Release()
        I = image_result.GetData()
        I = I.reshape( image_result.GetHeight(), image_result.GetWidth() )
        #I = I[:420, :620]
        
        max_val = I.max()
        if( max_val >= 255 ):
            new_exposure = exposure*0.9
            if( new_exposure < min_exposure ):
                print("Max value: %d. Minimum exposure reached, cannot decrease." %(max_val))
                return I
            else:
                exposure = new_exposure
                print( "Max value: %d. Decreasing exposure to: %.2f ms" %(max_val, exposure/1000))
                cam.ExposureTime.SetValue(exposure)
        elif( max_val < 100 ):
            new_exposure = exposure*1.1
            if( new_exposure > max_exposure ):
                print("Max value: %d. Maximum exposure reached, cannot increase." %(max_val))
                return I
            else:
                exposure = new_exposure
                print( "Max value: %d. Increasing exposure to: %.2f ms" %(max_val, exposure/1000))
                cam.ExposureTime.SetValue(exposure)
        else:
            return I

def scansnap(
    start_pos=-2, end_pos=2, num_steps=50,
    meas_seq='bmb',
    cam_sn=None, show_img=False,
    measure_pump= True, measure_probe=True,
    use_shutters=True):
    """
    Scan HARPIA XYZ sample stage Z axis and take an image at each step.
    
    Measurement sequence is determined by '''meas_seq'''.
    In beam-move-beam ('bmb') sequence, the probe shutter is opened, images
    are acquired for each stage position, and probe shutter is closed. The
    procedure is then repeated for the pump beam.
    In move-beam-beam ('mbb') sequence, the stage is stepped over the positions,
    and at each position two images are taken for the pump and the probe beams
    by opening and closing each shutter.
    
    """
    
    if cam_sn is None:
        cam_sn = '19105005'
        print("Using default sample plane camera SN " + cam_sn)
  
    # Wait after shutter is open for the beam to stabilize
    probe_on_delay_s = 2
    pump_on_delay_s = 0.5
          
    print("Scan configuration: from {:.2f} mm, to {:.2f} mm, num_steps {:d}".format(start_pos, end_pos, num_steps))

    # HARPIA address
    deviceAddress = '127.0.0.1'

    # TODO: Need to make sure the data directory exists and is empty
    try:
        os.mkdir(r".//data")
    except:
        pass
        
    try:
        os.mkdir(r".//data//Pump")
    except:
        pass
        
    try:
        os.mkdir(r".//data//Probe")
    except:
        pass

    # Init camera
    system = PySpin.System.GetInstance()
    cam_list = system.GetCameras()

    cam = None
    for cam2 in cam_list:
        if cam2.GetUniqueID() == cam_sn:
            cam = cam2

    if cam is None:
        print("Camera with SN {:s} not found".format(cam_sn))
        print("Using first available camera")
        cam = cam_list[0]
        
    try:    
        cam.Init()

        nodemap = cam.GetNodeMap()
        node_acquisition_mode = PySpin.CEnumerationPtr(nodemap.GetNode('AcquisitionMode'))

        node_acquisition_mode_singleframe = node_acquisition_mode.GetEntryByName('SingleFrame')

        acq_mode_singleframe = node_acquisition_mode_singleframe.GetValue()
        node_acquisition_mode.SetIntValue( acq_mode_singleframe )

        cam.BeginAcquisition()


        arr = np.linspace( start_pos, end_pos, num_steps )
           

        start_t = time.time()
        print("HARPIA Sample Stage Focusing Scan")
        H = Harpia(deviceAddress)

        if(use_shutters):
            if(measure_probe):
                H.close_probe_shutter()
            if(measure_pump):
                H.close_pump_shutter()
             

        plt.figure(1)
        plt.clf()

        if(measure_probe and measure_pump):
            ax_pr = plt.subplot(1,2,1)
            ax_pu = plt.subplot(1,2,2)
        else:
            if(measure_probe):
                ax_pr = plt.gca()
            if(measure_pump):
                ax_pu = plt.gca()

        default_exposure = 8000

        cam.ExposureTime.SetValue( default_exposure )
        exposure = cam.ExposureTime.GetValue()

        pu_exposure = default_exposure
        pr_exposure = default_exposure

        if meas_seq == 'mbb':
            for ind,pos in enumerate(arr):
                print("Step %d of %d, pos=%.2f mm" %(ind+1, num_steps, pos))
                H.microscope_sample_stage_go_to_z(pos*1000)

                if(measure_probe):
                    if(use_shutters):
                        H.open_probe_shutter()
                        time.sleep(probe_on_delay_s)
                    cam.ExposureTime.SetValue(pr_exposure)
                    
                    print("Acquiring probe image...")
                    I = GetImageWithAE(cam)
                    print("Done. Image val range [{:d}, {:d}]".format(np.min(I), np.max(I)))
                    pr_exposure = cam.ExposureTime.GetValue()
                    if(use_shutters):
                        H.close_probe_shutter()

                    plt.imsave( r"data\\Probe\\" + "img_%.2f.png"%(arr[ind]), I, cmap='gray', vmin=0, vmax=255)

                    if show_img:                
                        plt.sca(ax_pr)
                        plt.imshow(I)
                    
                    
                    
                if(measure_pump):
                    if(use_shutters):
                        H.open_pump_shutter()
                        time.sleep(pump_on_delay_s)
                    cam.ExposureTime.SetValue(pu_exposure)
                    print("Acquiring pump image...")
                    I = GetImageWithAE(cam)
                    print("Done. Image val range [{:d}, {:d}]".format(np.min(I), np.max(I)))
                    pu_exposure = cam.ExposureTime.GetValue()
                    if(use_shutters):
                        H.close_pump_shutter()

                    plt.imsave( r"data\\Pump\\" + "img_%.2f.png"%(arr[ind]), I, cmap='gray', vmin=0, vmax=255)

                    if show_img:                
                        plt.sca(ax_pu)
                        plt.imshow(I)
                    
                if show_img: 
                    plt.pause(0.05)

        elif meas_seq == 'bmb':
            if(measure_probe):
                if(use_shutters):
                    H.open_probe_shutter()
                    time.sleep(probe_on_delay_s)

                for ind,pos in enumerate(arr):
                    print("Step %d of %d, pos=%.2f mm" %(ind+1, num_steps, pos))
                    H.microscope_sample_stage_go_to_z(pos*1000)

                    cam.ExposureTime.SetValue(pr_exposure)
                    print("Acquiring image...")
                    I = GetImageWithAE(cam)
                    print("Done. Image val range [{:d}, {:d}]".format(np.min(I), np.max(I)))
                    pr_exposure = cam.ExposureTime.GetValue()
                    plt.imsave( r"data\\Probe\\" + "img_%.2f.png"%(arr[ind]), I, cmap='gray', vmin=0, vmax=255)
                    
                    if show_img:
                        plt.sca(ax_pr)
                        plt.imshow(I)
                        plt.pause(0.05)
                    
                        
            if(measure_pump):
                if(use_shutters):
                    H.close_probe_shutter()
                    H.open_pump_shutter()
                    time.sleep(pump_on_delay_s)

                for ind,pos in enumerate(arr):
                    print("Step %d of %d, pos=%.2f mm" %(ind+1, num_steps, pos))
                    H.microscope_sample_stage_go_to_z(pos*1000)
                    print("Move completed")

                    cam.ExposureTime.SetValue(pu_exposure)
                    print("Acquiring image...")
                    I = GetImageWithAE(cam)
                    print("Done. Image val range [{:d}, {:d}]".format(np.min(I), np.max(I)))
                    pu_exposure = cam.ExposureTime.GetValue()
                    plt.imsave( r"data\\Pump\\" + "img_%.2f.png"%(arr[ind]), I, cmap='gray', vmin=0, vmax=255)
                    if show_img:
                        plt.sca(ax_pu)
                        plt.imshow(I)
                        plt.pause(0.05)

        if(use_shutters):
            if(measure_probe):
                H.close_probe_shutter()
            if(measure_pump):
                H.close_pump_shutter()
                
        print("Moving to starting position: {:.2f} mm".format(arr[0]))
        H.microscope_sample_stage_go_to_z(arr[0]*1000)
         
        cam.EndAcquisition()
        cam.DeInit()
            
        del cam
        print("All done")
    except:
        print("Scanning failed!")
        raise
        
    print("Total time elapsed: {:.1f} s".format(time.time() - start_t))
  