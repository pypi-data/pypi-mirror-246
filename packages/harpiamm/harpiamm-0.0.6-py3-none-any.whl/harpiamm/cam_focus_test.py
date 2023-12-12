"""HARPIA Camera focus scan.

Acquire a set of through-focus images of the pump and probe beams by moving a
stage-mounted camera. The camera is controlled via FLIR Spinaker API, and the
stage is controlled using HARPIA API.

Author: Lukas Kontenis
Copyright (c) 2019-2020 Light Conversion
All rights reserved.
www.lightcon.com
"""
import time
import os
import json
import datetime
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

import PySpin

from lightcon.harpia import Harpia


def read_setup(par_name=None,file_name='setup.xml'):
    try:
        setup = json.load(open('setup.xml'))
        return setup.get(par_name, None)
    except Exception:
        return None


def GetImageWithAE(cam, img_mask=None):
    exposure_units = cam.ExposureTime.GetUnit()
    if exposure_units == 'us':
        exposure_fac = 1E-6
    else:
        raise ValueError("Unsupported exposure time units '{:s}'".format(exposure_units))

    max_exposure = cam.ExposureTime.GetMax()
    min_exposure = cam.ExposureTime.GetMin()
    exposure = cam.ExposureTime.GetValue()
    while(1):
        cam.AcquisitionStart()
        image_result = cam.GetNextImage()
        image_result.Release()
        cam.AcquisitionStart()
        image_result = cam.GetNextImage()
        I = image_result.GetData()
        #while 1:
         #   image_result = cam.GetNextImage()
        #    #image_result.Release()
         #   I = image_result.GetData()
          #  if len(I) > 0:
           #     break
        I = I.reshape( image_result.GetHeight(), image_result.GetWidth() )
        I = np.array(I)
        if img_mask is not None:
            if I.shape == img_mask.shape:
                I[img_mask] = 0
            else:
                print("Incorrect mask size. Clearing mask")
                img_mask = None

        max_val = I.max()
        if( max_val >= 255 ):
            new_exposure = exposure*0.9
            if( new_exposure < min_exposure ):
                print("Max value: %d. Minimum exposure reached, cannot decrease." %(max_val))
                return I
            else:
                exposure = new_exposure
                print( "Max value: %d. Decreasing exposure to: %.2f ms" %(max_val, exposure*exposure_fac*1E3))
                cam.ExposureTime.SetValue(exposure)
        elif( max_val < 100 ):
            new_exposure = exposure*1.1
            if( new_exposure > max_exposure ):
                print("Max value: %d. Maximum exposure reached, cannot increase." %(max_val))
                return I
            else:
                exposure = new_exposure
                print( "Max value: %d. Increasing exposure to: %.2f ms" %(max_val, exposure*exposure_fac*1E3))
                cam.ExposureTime.SetValue(exposure)
        else:
            return I


def cam_focus_test(
        start_pos=-2, end_pos=2, num_steps=50,
        meas_seq='bmb',
        use_cam=True,
        cam_id=None, cam_sn=None, show_img=False,
        measure_pump=True, measure_probe=True,
        use_shutters=True):
    """Scan HARPIA XYZ sample stage Z axis and take an image at each step.

    Measurement sequence is determined by '''meas_seq'''.
    In beam-move-beam ('bmb') sequence, the probe shutter is opened, images
    are acquired for each stage position, and probe shutter is closed. The
    procedure is then repeated for the pump beam.

    In move-beam-beam ('mbb') sequence, the stage is stepped over measurement
    positions, and at each position two images are taken for the pump and the
    probe beams by opening and closing each shutter.
    The 'bmb' sequence has far fewer shutter open and close events and thus is
    faster than 'mbb'. In 'mbb' sequence the pump and probe images are acquired
    right after each other, resulting in a lower time delay. In some setups the
    probe beam needs time to stabilize, so the 'mbb' sequence becomes very slow
    and prone to systemic error if the probe beam measurement is taken too soon
    after the shutter is opened.
    """
    print("HARPIA Sample Stage Focusing Scan")

    if cam_sn is None:
        cam_sn = read_setup('cam_sn')
        if cam_sn is None:
            print("Sample plane camera SN not specified, using first available camera")
            cam_id = 0
        else:
            print("Sample plane camera SN: " + cam_sn)

    # Wait after shutter is open for the beam to stabilize
    probe_on_delay_s = 2
    pump_on_delay_s = 0.5

    print("Scan configuration: from {:.2f} mm, to {:.2f} mm, num_steps {:d}".format(start_pos, end_pos, num_steps))

    # Make sure the data directory exists
    try:
        os.mkdir(r".//data")
    except FileExistsError:
        pass
    except Exception:
        print("Cannot create data folder")
        return

    # Make sure the script has write access
    try:
        tmp_file_name = r".//data/test.tmp"
        np.savetxt(tmp_file_name, [123])
    except PermissionError:
        print("Write access to the data folder is denied. Run the script from "
              "a folder where the current user has write access.")
        return

    os.remove(tmp_file_name)

    # Create a timestsamped folder for the current scan
    timestamp = datetime.datetime.now()
    timestamp_str = timestamp.strftime('%Y-%m-%d %H%M%S')
    data_dir = 'data/' + timestamp_str + ' - Overlap scan/'
    os.mkdir(data_dir)

    # Create pump and probe subdirs
    pump_dir = data_dir + "Pump/"
    probe_dir = data_dir + "Probe/"
    os.mkdir(pump_dir)
    os.mkdir(probe_dir)

    if use_cam:
        # Init camera
        system = PySpin.System.GetInstance()
        cam_list = system.GetCameras()

        if len(cam_list) == 0:
            print("No cameras found. Cannot continue.")
            return

        cam = None
        if cam_sn is not None:
            for cam2 in cam_list:
                cam2.Init()
                sn_str = cam2.DeviceSerialNumber.GetValue()
                cam2.DeInit()
                if sn_str == cam_sn:
                    cam = cam2
                    break

        if cam is None:
            cam_id = 0

        if cam_id is not None:
            cam = cam_list[cam_id]

    try:
        if use_cam:
            cam.Init()

            model_str = cam.DeviceModelName.GetValue()
            sn_str = cam.DeviceSerialNumber.GetValue()
            print("Connected to " + model_str + ', SN: ' + sn_str)

            nodemap = cam.GetNodeMap()
            node_acquisition_mode = PySpin.CEnumerationPtr(nodemap.GetNode('AcquisitionMode'))

            node_acquisition_mode_singleframe = node_acquisition_mode.GetEntryByName('SingleFrame')

            acq_mode_singleframe = node_acquisition_mode_singleframe.GetValue()
            node_acquisition_mode.SetIntValue( acq_mode_singleframe )

            # Tur off auto exposure and auto gain
            cam.ExposureAuto.SetValue(0)
            cam.GainAuto.SetValue(0)

            img_mask = None
            mask_file_name = 'img_mask.png'
            if Path(mask_file_name).is_file():
                print("Loading image mask from '{:s}'".format(mask_file_name))
                mask_data = Image.open(mask_file_name)
                print("Mask image size is {:d}x{:d}, mode: {:s}".format(
                    mask_data.size[0], mask_data.size[1], mask_data.mode))
                if mask_data.mode != '1':
                    print("Converting mask to binary")
                    mask_data.convert('1')
                    mask_data.save(mask_file_name)
                img_mask = np.array(mask_data) != 0

            cam.BeginAcquisition()

        arr = np.linspace( start_pos, end_pos, num_steps )

        start_t = time.time()

        # HARPIA address
        deviceAddress = '127.0.0.1'
        print("Connecting to HARPIA Service App at " + deviceAddress)
        try:
            H = Harpia(deviceAddress)
        except:
            print("Could not connect to HARPIA Service App")
            return

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

        default_exposure = 1000

        if use_cam:
            cam.ExposureTime.SetValue( default_exposure )
            exposure = cam.ExposureTime.GetValue()

        pu_exposure = default_exposure
        pr_exposure = default_exposure

        if meas_seq == 'mbb':
            for ind,pos in enumerate(arr):
                print("Step %d of %d, pos=%.2f mm" %(ind+1, num_steps, pos))
                H.microscope_set_sample_stage_position_Z(pos*1000)

                if(measure_probe):
                    if(use_shutters):
                        H.open_probe_shutter()
                        time.sleep(probe_on_delay_s)

                    if use_cam:
                        cam.ExposureTime.SetValue(pr_exposure)

                        print("Acquiring probe image...")
                        I = GetImageWithAE(cam, img_mask=img_mask)
                        print("Done. Image val range [{:d}, {:d}]".format(np.min(I), np.max(I)))
                        pr_exposure = cam.ExposureTime.GetValue()
                    if(use_shutters):
                        H.close_probe_shutter()

                    if use_cam:
                        plt.imsave(probe_dir + "img_%.2f.png"%(arr[ind]), I, cmap='gray', vmin=0, vmax=255)

                    if show_img:
                        plt.sca(ax_pr)
                        plt.imshow(I)



                if(measure_pump):
                    if(use_shutters):
                        H.open_pump_shutter()
                        time.sleep(pump_on_delay_s)

                    if use_cam:
                        cam.ExposureTime.SetValue(pu_exposure)
                        print("Acquiring pump image...")
                        I = GetImageWithAE(cam, img_mask=img_mask)
                        print("Done. Image val range [{:d}, {:d}]".format(np.min(I), np.max(I)))
                        pu_exposure = cam.ExposureTime.GetValue()

                    if(use_shutters):
                        H.close_pump_shutter()

                    if use_cam:
                        plt.imsave(pump_dir + "img_%.2f.png"%(arr[ind]), I, cmap='gray', vmin=0, vmax=255)

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
                    H.microscope_set_sample_stage_position_Z(pos*1000)

                    if use_cam:
                        cam.ExposureTime.SetValue(pr_exposure)
                        print("Acquiring image...")
                        I = GetImageWithAE(cam, img_mask=img_mask)
                        print("Done. Image val range [{:d}, {:d}]".format(np.min(I), np.max(I)))
                        pr_exposure = cam.ExposureTime.GetValue()
                        plt.imsave(probe_dir + "img_%.2f.png"%(arr[ind]), I, cmap='gray', vmin=0, vmax=255)

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
                    H.microscope_set_sample_stage_position_Z(pos*1000)
                    print("Move completed")

                    if use_cam:
                        cam.ExposureTime.SetValue(pu_exposure)
                        print("Acquiring image...")
                        I = GetImageWithAE(cam, img_mask=img_mask)
                        print("Done. Image val range [{:d}, {:d}]".format(np.min(I), np.max(I)))
                        pu_exposure = cam.ExposureTime.GetValue()
                        plt.imsave(pump_dir + "img_%.2f.png"%(arr[ind]), I, cmap='gray', vmin=0, vmax=255)
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
        H.microscope_set_sample_stage_position_Z(arr[0]*1000)

        if use_cam:
            cam.EndAcquisition()
            cam.DeInit()

            del cam
        print("All done")
    except:
        print("Scanning failed!")
        raise

    print("Total time elapsed: {:.1f} s".format(time.time() - start_t))


if __name__ == '__main__':
    cam_focus_test()
