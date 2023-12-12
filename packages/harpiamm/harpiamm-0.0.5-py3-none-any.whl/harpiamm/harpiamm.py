#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""HARPIA Microscopy Extension alignment routines.

Contact: lukas.kontenis@lightcon.com, support@lightcon.com

Copyright (c) 2019-2021 Light Conversion
All rights reserved.
www.lightcon.com
"""
import logging

logger = logging.getLogger('harpiamm')

file_log_handler = logging.FileHandler('harpiamm.log')
logger.addHandler(file_log_handler)

stderr_log_handler = logging.StreamHandler()
logger.addHandler(stderr_log_handler)

# nice output format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_log_handler.setFormatter(formatter)
stderr_log_handler.setFormatter(formatter)

logger.setLevel('DEBUG')

logger.info('Loading harpiamm')

import os
import xmltodict
import numpy as np
import matplotlib.pyplot as plt
import time

from scipy.ndimage.measurements import center_of_mass
from PIL import Image

from lklib.fileread import enum_files, join_paths, check_file_exists
from lklib.util import cut_by_x_range, get_common_range, isarray, isnone, \
     handle_general_exception, find_closest, get_color, get_exception_info_str
from lklib.fit import fit_gaussian_2d, fit_poly_2, get_poly_2_max_x
from lklib.standard_func import poly_2
from lklib.image import make_gif, load_img, comb_img
from lklib.plot import add_x_marker, add_y_marker

from harpiamm.harpiamm_ui import get_report_metainfo

logger.info('Imports loaded')


def EnumerateOverlapScanFiles(path=".", mode="pinhole", **kwargs):
    """
    Enumerate overlap scan data files and return sorted file names and Z positions in um.
    """
    if(mode=="pinhole"):
        return enum_files(path=path, extension="dat", preffix="I", **kwargs, files_to_remove=".\\I.dat")
    elif(mode=="camera"):
        [file_names, Z] = enum_files(path=path, extension="png", preffix="img", **kwargs)
        Z = Z*1000
        return [file_names, Z]

def MakeXYProfileGIF(path='.', output_name="XYProfiles.gif", verbose=False):
    """
    Make a GIF showing the XY profile as a function of Z position.
    """
    output_path = join_paths(path, output_name)
    if check_file_exists(output_path):
        print("{:s} already exists".format(output_path))
        return

    file_names = enum_files(path=path, extension="png", preffix="XY_profile", verbose=verbose, prepend_path=True)[0]

    if(verbose):
        print("Found {:d} files".format(len(file_names)))
        print("Making GIF...")

    make_gif(file_names=file_names, output_name=output_path)

    if(verbose):
        print("Done")

def GetNumberOfPixels(sensor):
    if(sensor=="ICX445"):
        return [1288, 964]
    else:
        print("Unknown sensor " + str(sensor))
        return [None, None]

def GetCameraPixelSize(sensor):
    if(sensor=="ICX445"):
        return 3.8
    else:
        print("Unknown sensor " + sensor)
        return None

def GetXYZOverlapScanXYArrays(mode="pinhole", **kwargs):
    if(mode=="pinhole"):
        [stepsX, stepsY, stepsZ] = GetCalibScanSteps(**kwargs)
        [spanX, spanY, spanZ] = GetCalibScanSpan(**kwargs)
        [ofsX, ofsY, ofsZ] = GetCalibScanOfs(**kwargs)

        X = np.linspace(-spanX/2-ofsX, spanX/2+ofsX, stepsX)
        Y = np.linspace(-spanY/2-ofsY, spanY/2+ofsY, stepsY)
    elif(mode=="camera"):
        [stepsX, stepsY, stepsZ] = GetXYZScanNumSteps(**kwargs)
        sensor = GetCameraSensorType(**kwargs)
        [numC, numR] = GetNumberOfPixels(sensor)
        pxsz = GetCameraPixelSize(sensor)
        spanX = numC*pxsz
        spanY = numR*pxsz
        [ofsX, ofsY, ofsZ] = GetXYZScanOfs(**kwargs)

        X = np.linspace(-spanX/2-ofsX, spanX/2+ofsX, numC)
        Y = np.linspace(-spanY/2-ofsY, spanY/2+ofsY, numR)
    else:
        print("Unknown mode " + str(mode))


    return [X, Y]

def GetPixelSize(X, Y):
    return np.mean(np.concatenate((np.diff(X), np.diff(Y))))

def GetXYZOverlapScanData(path='.', mode='pinhole', verbose=False, WithCube=False):
    """
    Get XYZ overlap parameters from a pinhole or a camera scan. The retrieved
    parameters for very XY slice are: Z position, controid locations, beam
    widths and maximum intensity.
    """
    # Load stored fit parameters, if available
    if(mode == "camera"):
        try:
            fit_arr = np.loadtxt(join_paths(path, GetOverlapFitArrayFileName()))
            Z = fit_arr[:, 0]
            Imax = fit_arr[:,1]
            C = fit_arr[:,2:4]
            W = fit_arr[:,4:6]
            logger.info("Loading stored fit parameters")
            return [Z, Imax, C, W]
        except:
            pass

    if(mode == 'pinhole'):
        [file_names, Z] = EnumerateOverlapScanFiles(path=path, verbose=verbose)
    elif(mode == 'camera'):
        [file_names, Z] = enum_files(path=path, extension="png", preffix="img", prepend_path=False, verbose=verbose, neg_inds=False)

    # Sort data so that Z is increasing
    sort_order = np.argsort(Z)
    Z = Z[sort_order]
    file_names = [file_names[i] for i in sort_order]

    if(mode == 'pinhole'):
        [X, Y] = GetXYZOverlapScanXYArrays()
        pxsz = GetPixelSize(X, Y)
    else:
        # TODO: get camera pixel size
        pxsz = 3.75
        print("WARNING: camera pixel size not define, assuming ICX445 sensor with {:.2f} um".format(pxsz))

    orig_path = os.getcwd()
    try:
        os.chdir(path)

        numF = len(file_names)

        Imax = np.ndarray(numF)
        C = np.ndarray([numF,2])
        W = np.ndarray([numF,2])

        fit_arr = np.ndarray([len(file_names), 8])
        fit_arr.fill(np.nan)

        # Camera images typically contain a lot of pixels so it makes sense to crop the image to a smaller size to increase fitting speed. The cropped image size is determined
        # from the estimated std. dev. of the 2D gaussian fit so there's many ways this may not work.
        # Pinhole datasets typically contain far less pixels and thus can be fitted without cropping
        if(mode=='pinhole'):
            crop_to_fit_region = False
        if(mode=='camera'):
            crop_to_fit_region = True

        # Find the center of mass of the image closest to Z=0 and use it to center the fit crop area for all images.
        z_zero_ind = find_closest(Z, 0)
        I = np.array(Image.open(file_names[z_zero_ind]))
        Isz = I.shape
        if len(Isz)>2 and I.shape[2] > 1:
            I = I[:,:,0]

        # Background illumination can skew the center of mass of the image. Set pixels at half the maximum intensity to zero to avoid that.
        I[I<np.max(I)/2] = 0
        fit_area_center = center_of_mass(I)
        fit_area_sz=[100, 100]
        fit_crop_area = np.round([
            fit_area_center[1] - fit_area_sz[1]/2,
            fit_area_center[1] + fit_area_sz[1]/2,
            fit_area_center[0] - fit_area_sz[0]/2,
            fit_area_center[0] + fit_area_sz[0]/2]).astype('int')

        for ind,file_name in enumerate(file_names):
            print("Processing file {:d} {:s}".format(ind, file_name))
            if(mode == 'pinhole'):
                I = np.loadtxt(file_name)
                Isz = I.shape
            elif(mode == 'camera'):
                I = np.array(Image.open(file_name))
                Isz = I.shape
                X = np.arange(0, Isz[1])*pxsz
                Y = np.arange(0, Isz[0])*pxsz

                # Select the R channel in RGB images
                if len(Isz)>2 and Isz[2] > 1:
                    I = I[:,:,0]

            # Determine maximum intensity
            Imax[ind] = np.max(I)

            # Find center of mass
            C[ind,:] = center_of_mass(I)

            try:
                plt.figure()
                fr = FitXYZScanXYProfile(I, X=X, Y=Y, pxsz=pxsz, crop_area=fit_crop_area, \
                    plot=True, suptitle_str="XY Profile at Z={:.2f}".format(Z[ind]))

                fit_arr[ind,0] = Z[ind]
                fit_arr[ind,1:] = fr

                fr = fr[3:5]

                np.savetxt(GetOverlapFitArrayFileName(), fit_arr)

                fig_file_name = "XY_profile_{:.2f}.png".format(Z[ind])
                plt.draw()
                plt.savefig(fig_file_name)
                #plt.show()
                plt.close()

            except RuntimeWarning:
                print("A runtime warning was issued during the processing of file '{:s}'".format(file_name))
                fr = [np.NaN, np.NaN]
            except:
                handle_general_exception("Could not fit file {:s}".format(file_name))
                fr = [np.NaN, np.NaN]

            W[ind,:] = fr

        os.chdir(orig_path)

        if(mode == 'pinhole'):
            # Get calibration scan XYZ span and offset
            [scanSpanX,scanSpanY,scanSpanZ] = GetCalibScanSpan(samplingCubeInserted=WithCube)
            [scanOfsX,scanOfsY,scanOfsZ] = GetCalibScanOfs(samplingCubeInserted=WithCube)

            # Scan data is saved as 2D arrays where each element corresponds
            # to one scan step. Maximum position array C values are calculated in
            # pixel units. To convert the values from pixels to um we need to:
            # 1) change the scale from px to um; 2) apply an offset due to the scan
            # being centered at (0,0) and the pixel origin (0,0) being at the edge;
            # 3) apply an XY scan offset that was used to translate the stage
            # before scanning.

            # Determine the um/px steps
            stepX = scanSpanX/Isz[0]
            stepY = scanSpanY/Isz[1]

            # Determine the offsets in um
            ofsX = -scanSpanX/2 + scanOfsX
            ofsY = -scanSpanY/2 + scanOfsY

            # Calculate center positions in um
            C[:,0] = C[:,0]*stepX + ofsX
            C[:,1] = C[:,1]*stepY + ofsY
        elif(mode=='camera'):
            # Calculate center positions in um
            C[:,0] = C[:,0]*pxsz
            C[:,1] = C[:,1]*pxsz

    except:
        os.chdir(orig_path)
        raise

    return [Z, Imax, C, W]

def FitXYZScanXYProfile(data, **kwargs):
    return fit_gaussian_2d(data, **kwargs, return_fwhm=True)

def LoadImageData(file_name=None, mode="pinhole", crop=None):
    if(mode=="pinhole"):
        I = np.loadtxt(file_name)*1E3
    elif(mode=="camera"):
        I = plt.imread(file_name)

    if(not isnone(crop)):
        I = I[crop[1]:crop[3], crop[0]:crop[2]]
    return I

def GetOverlapFitArrayFileName():
    return "fit_arr.txt"

def FitXYProfiles(path='.', mode='pinhole', verbose=False, crop=None):
    """
    Fit overlap scan XY profiles.
    """
    [X, Y] = GetXYZOverlapScanXYArrays(path='../', mode=mode)
    pxsz = GetPixelSize(X, Y)

    fig_file_names = []
    [file_names, Z] = EnumerateOverlapScanFiles(path=path, verbose=verbose, mode=mode)

    if(mode=='pinhole'):
        crop_to_fit_region = False
    if(mode=='camera'):
        crop_to_fit_region = False

    # The fit array stores the Z position of the XY slice and the 7 parameters of a rotated 2D Gaussian fit: A, cx, cy, wx, wy, y0, theta
    fit_arr = np.ndarray([len(file_names), 8])
    fit_arr.fill(np.nan)

    for ind, file_name in enumerate(file_names):
        I = LoadImageData(file_name, mode=mode)
        if(not isnone(crop)):
            I_roi = I[crop[1]:crop[3], crop[0]:crop[2]]
            X_roi = X[crop[0]:crop[2]]
            Y_roi = Y[crop[1]:crop[3]]
        else:
            I_roi = I
            X_roi = X
            Y_roi = Y
        try:
            fit_arr[ind,0] = Z[ind]
            fit_arr[ind,1:] = FitXYZScanXYProfile(I=I_roi, X=X_roi, Y=Y_roi, fit_rotation=True, pxsz=pxsz, crop_to_fit_region=crop_to_fit_region, \
                plot=True, pause_on_plot=False, suptitle_str="XY Profile at Z={:.1f}".format(Z[ind]))
            fig_file_name = "XY_profile_{:.1f}.png".format(Z[ind])
            plt.savefig(fig_file_name)
            fig_file_names.append(fig_file_name)
            np.savetxt(GetOverlapFitArrayFileName(), fit_arr)
        except:
            print("Fitting failed")

def ConvertToPNG(path='.', verbose=False, **kwargs):
    [file_names, Z] = EnumerateOverlapScanFiles(path=path, **kwargs)

    orig_path = os.getcwd()
    try:
        os.chdir(path)
        if(verbose):
            print("Converting {:d} files to PNG".format(len(file_names)))
        fig_file_names = []
        for ind, file_name in enumerate(file_names):
            if(verbose):
                print("Converting {:d}/{:d}".format(ind,len(file_names)))
            I = np.loadtxt(file_name)
            fig_file_name = "I_{:d}.png".format(int(round(Z[ind])))
            fig_file_names.append(fig_file_name)

            # If I has nan values imsave will produce an empty image. FODE
            # gives nan when it is saturated, so setting these values to 0
            # should give an indication that something is wrong.
            # TODO: show saturated values clearly, maybe using a baked
            # colourmap
            I[np.isnan(I)] = 0

            plt.imsave(fig_file_name, I)

    except:
        os.chdir(orig_path)
        raise

    os.chdir(orig_path)

    return [fig_file_names,Z]

def GetXYZScanNode(path='.'):
    return ReadXYZScanHeader(path=path)

def GetCameraSensorType(path='.'):
    return GetValue_string(ReadXYZScanHeader(path=path).get('setup').get('camera').get('sensor'))

def GetCalibScanNode(path='.', samplingCubeInserted=False):
    if(samplingCubeInserted):
        samplingCubeInserted_str = 'True'
    else:
        samplingCubeInserted_str = 'False'

    calib_arr = ReadCalib(path=path).get('configSection').get('overlapCalib').get('calibScanConfig')
    if(not isarray(calib_arr)):
        calib_arr = [calib_arr]
    for calib in calib_arr:
        if(calib.get('@samplingCubeInserted') == samplingCubeInserted_str):
            return calib
    return None

def GetCalibScanInfoNode(path='.'):
    calib = ReadCalib(path=path).get('configSection').get('overlapCalib').get('calibScanInfo')
    if(isarray(calib)):
        RuntimeWarning("Multiple calibScanInfo nodes found, using ind=0")
        calib = calib[0]

    return calib

def ReadXYZScanHeader(path='.'):
    with open(join_paths(path,'scan.xml')) as fd:
        calib = xmltodict.parse(fd.read())

    return calib.get('XYZScan')

def ReadCalib(path='.'):
    with open(join_paths(path,'calib.xml')) as fd:
        calib = xmltodict.parse(fd.read())

    return calib.get('config')

def GetValue_double(node):
    if(not isnone(node)):
        return float(node.get('#text'))
    else:
        return None

def GetValue_string(node):
    if(not isnone(node)):
        return node.get('#text')
    else:
        return None

def GetXYZScanNumSteps(**kwargs):
    nd = GetXYZScanNode(**kwargs).get('scanConfig')
    if(not isnone(nd)):
        stepsX = GetValue_double(nd.get('stepsX'))
        stepsY = GetValue_double(nd.get('stepsY'))
        stepsZ = GetValue_double(nd.get('stepsZ'))
        return [stepsX, stepsY, stepsZ]
    else:
        return None

def GetCalibScanSteps(**kwargs):
    calib = GetCalibScanNode(**kwargs)
    if(not isnone(calib)):
        stepsX = GetValue_double(calib.get('stepsX'))
        stepsY = GetValue_double(calib.get('stepsY'))
        stepsZ = GetValue_double(calib.get('stepsZ'))
        return [stepsX, stepsY, stepsZ]
    else:
        return None

def GetXYZScanSpan(**kwargs):
    nd = GetXYZScanNode(**kwargs).get('scanConfig')
    if(not isnone(nd)):
        spanX = GetValue_double(nd.get('spanX'))
        spanY = GetValue_double(nd.get('spanY'))
        spanZ = GetValue_double(nd.get('spanZ'))
        return [spanX, spanY, spanZ]
    else:
        return None

def GetCalibScanSpan(**kwargs):
    calib = GetCalibScanNode(**kwargs)
    if(not isnone(calib)):
        spanX = GetValue_double(calib.get('spanX'))
        spanY = GetValue_double(calib.get('spanY'))
        spanZ = GetValue_double(calib.get('spanZ'))
        return [spanX, spanY, spanZ]
    else:
        return None

def GetXYZScanOfs(**kwargs):
    nd = GetXYZScanNode(**kwargs).get('scanConfig')
    if(not isnone(nd)):
        ofsX = GetValue_double(nd.get('ofsX'))
        ofsY = GetValue_double(nd.get('ofsY'))
        ofsZ = GetValue_double(nd.get('ofsZ'))
        return [ofsX, ofsY, ofsZ]
    else:
        return None

def GetCalibScanOfs(**kwargs):
    calib = GetCalibScanNode(**kwargs)
    if(not isnone(calib)):
        ofsX = GetValue_double(calib.get('ofsX'))
        ofsY = GetValue_double(calib.get('ofsY'))
        ofsZ = GetValue_double(calib.get('ofsZ'))
        return [ofsX, ofsY, ofsZ]
    else:
        return None

def GetCalibInputPower(beam=None, **kwargs):
    if(isnone(beam)):
        RuntimeWarning("Undefined beam")
        return None
    calib = GetCalibScanInfoNode(**kwargs)
    if(isnone(calib)):
        RuntimeWarning("Could not read calibScanInfo node")
        return None

    return GetValue_double(calib.get("inputPower{:s}".format(beam)))


def print_check_result(fail_mask, message, zarr=None):
    """Print mask check result.

    Report the number of failed elements in an a mask check array. If the z
    position array is given, report the failed positions too.
    """
    num_failed = np.nansum(fail_mask)
    num_pts = len(fail_mask)
    if num_failed > 0:
        logger.warn("{:d} out of {:d} ".format(num_failed, num_pts) + message)

def validate_beam_fit_results(par):
    """Validate beam fit results.

    Check whether pump fit amplitude values are within the expected range.
    """
    # Minimum and maximum intensity values to check for bad fit values. The
    # maximum value needs to be larger than 255 even though the data is capped
    # at 255. Gaussian fits with narrow widths can spike above this value and
    # still be valud.
    MIN_AMPL = 10
    MAX_AMPL = 300

    if par is None:
        return None

    name = par['name']

    ampl_fail = np.logical_or(par['ampl'] > MAX_AMPL, par['ampl'] < MIN_AMPL)
    print_check_result(ampl_fail, name + " fit amplitudes are "
                       "outside of the valid range")

    # Count the number of failed fits
    failed_pts = np.logical_or( np.logical_or(
            np.isnan(par['zpos']), np.isnan(par['width'][:,0])), ampl_fail)

    if failed_pts.all():
        print.error("All " + name + " fit values failed, there is no valid "
                    "data")
        return None
    elif failed_pts.any():
        print_check_result(failed_pts, name + " fits failed, removing...")
        par['zpos'] = par['zpos'][np.logical_not(failed_pts)]
        par['ampl'] = par['ampl'][np.logical_not(failed_pts)]
        par['xypos'] = par['xypos'][np.logical_not(failed_pts), :]
        par['width'] = par['width'][np.logical_not(failed_pts), :]

    return par

def PlotOverlapScanSummaryFigure(
        path=r'./', mode='camera', width_metric='mean', xy_pos_rel_to_z0=True,
        fig_style='whole_range', WithCube=False, subplot_rows=1, subplot_row=0,
        plot_wl=None, suptitle_str=None, obj_id=None,
        device_sn=None, date_str=None):
    """Make pump-probe overlap report figure and GIFs.

    Create a pump-probe overlap figure.
    """
    if obj_id is None or device_sn is None:
        obj_id, device_sn = get_report_metainfo()

    # Number of overlap-related warnings
    overlap_warn = 0

    # Is the overlap result within specification
    overlap_in_spec = True

    # Supported objectives
    SUPPORTED_OBJ = ['nikon_pf_4x', 'nikon_pf_10x']
    if obj_id not in SUPPORTED_OBJ:
        logger.warn("Objective '" + obj_id + "' is not supported, not all beam"
                    " size checks will be performed")
        overlap_warn += 1
        obj_ind = 0
    else:
        for ind, name in enumerate(SUPPORTED_OBJ):
            if name == obj_id:
                obj_ind = ind + 1
                break

    # Expected pump and probe beam size ranges
    # Objective indices: unknonw, Plan Fluor 4x, Plan Fluor 10x
    MIN_PROBE_FOCUS_SZ = [0.1, 7, 3][obj_ind]
    MAX_PROBE_FOCUS_SZ = [50, 12, 12][obj_ind]
    MAX_PROBE_SZ = [500, 100, 100][obj_ind]
    MIN_PROBE_FOCUS_Z = [-2, -0.1, -0.1][obj_ind]
    MAX_PROBE_FOCUS_Z = [2, 0.1, 0.1][obj_ind]

    MIN_PUMP_FOCUS_SZ = [0.1, 5, 3][obj_ind]
    MAX_PUMP_FOCUS_SZ = [50, 25, 25][obj_ind]
    MAX_PUMP_SZ = [500, 100, 100][obj_ind]
    MIN_PUMP_FOCUS_Z = [-2, -0.5, -0.5][obj_ind]
    MAX_PUMP_FOCUS_Z = [2, 0.5, 0.5][obj_ind]

    # Allowed pump-probe focus distance
    MAX_PP_XY_R = [50, 5, 4][obj_ind]

    # Allowed pump-probe focal spot size ratio
    MIN_OVERLAP_RATIO = 1.4
    MAX_OVERLAP_RATIO = 2.1

    if(mode == 'pinhole'):
        if(WithCube):
            path_pu = path + r'Pump with Cube/'
            path_pr = path + r'Probe with Cube/'
        else:
            path_pu = path + r'Pump no Cube/'
            path_pr = path + r'Probe no Cube/'
    elif(mode == 'camera'):
        path_pu = path + r'Pump'
        path_pr = path + r'Probe'

    try:
        logger.info("Getting pump focus parameters...")
        [Z1, Imax1, xypos_pu, W1] = GetXYZOverlapScanData(path=path_pu, WithCube=WithCube, mode=mode)
        par_pu = {'name': 'pump', 'zpos': Z1, 'ampl': Imax1, 'xypos': xypos_pu, 'width': W1}
    except:
        logger.warn("Pump data not available")
        overlap_in_spec = False
        par_pu = None

    try:
        logger.info("Getting probe focus parameters...")
        [Z2, Imax2, xypos_pr, W2] = GetXYZOverlapScanData(path=path_pr, WithCube=WithCube, mode=mode)
        par_pr = {'name': 'probe', 'zpos': Z2, 'ampl': Imax2, 'xypos': xypos_pr, 'width': W2}
    except:
        logger.warn("Probe data not available")
        overlap_in_spec = False
        par_pr = None

    # Make sure either pump or probe data is available
    if par_pu is None and par_pr is None:
        logger.error("Neither pump nor probe data is available")
        return

    # Determine the number of fit points
    if par_pu is not None and par_pr is not None:
        len_pu = len(par_pu['zpos'])
        len_pr = len(par_pr['zpos'])
        num_pts = len_pu
        if len_pu != len_pr:
            logger.error("The number of pump ({:d})".format(len_pu) +
                  " and probe ({:d}) imges is not equal".format(len_pr))
            return
    elif par_pu is not None:
        num_pts = len(par_pu['zpos'])
    else:
        num_pts = len(par_pr['zpos'])

    par_pu = validate_beam_fit_results(par_pu)
    par_pr = validate_beam_fit_results(par_pr)

    if par_pr is not None:
        beam_sz_pr = np.sqrt(np.mean(par_pr['width']**2, 1))

        probe_focus_sz = np.min(beam_sz_pr)
        if probe_focus_sz < MIN_PROBE_FOCUS_SZ:
            logger.warn("Probe focus size is too small " +
                  "(<{:.1f} µm)".format(MIN_PROBE_FOCUS_SZ))
            overlap_warn += 1
        if probe_focus_sz > MAX_PROBE_FOCUS_SZ:
            logger.warn("Probe focus size is too large " +
                  "(>{:.0f} µm)".format(MAX_PROBE_FOCUS_SZ))
            overlap_warn += 1

        probe_sz_max = np.max(beam_sz_pr)
        if probe_sz_max > MAX_PROBE_SZ:
            logger.warn("Maximum probe beam size is too large " +
                  "(>{:.0f} µm)".format(MAX_PROBE_SZ))
            overlap_warn += 1

        probe_focus_ind = np.argmin(beam_sz_pr)
        probe_focus_x = xypos_pr[probe_focus_ind, 0]
        probe_focus_y = xypos_pr[probe_focus_ind, 1]

        probe_focus_z = Z2[probe_focus_ind]
        if probe_focus_z < MIN_PROBE_FOCUS_Z:
            logger.warn("Probe focus Z position is too close " +
                  "(<{:.1f} mm)".format(MIN_PROBE_FOCUS_Z))
            overlap_warn += 1
        if probe_focus_z > MAX_PROBE_FOCUS_Z:
            logger.warn("Probe focus Z position is too far " +
                  "(>{:.1f} mm)".format(MAX_PROBE_FOCUS_Z))
            overlap_warn += 1

        logger.info("Probe focus size is {:.1f} µm FWHM at Z = {:.2f} mm".format(
            probe_focus_sz, probe_focus_z))

    if par_pu is not None:
        beam_sz_pu = np.sqrt(np.mean(W1**2, 1))

        pump_focus_sz = np.min(beam_sz_pu)
        if pump_focus_sz < MIN_PUMP_FOCUS_SZ:
            logger.warn("Pump focus size is too small " +
                  "(<{:.1f} µm)".format(MIN_PUMP_FOCUS_SZ))
            overlap_warn += 1
        if pump_focus_sz > MAX_PUMP_FOCUS_SZ:
            logger.warn("Pump focus size is too large " +
                  "(>{:.0f} µm)".format(MAX_PUMP_FOCUS_SZ))
            overlap_warn += 1
            overlap_in_spec = False

        pump_sz_max = np.max(beam_sz_pu)
        if pump_sz_max > MAX_PUMP_SZ:
            logger.warn("Maximum pump beam size is too large " +
                  "(>{:.0f} µm)".format(MAX_PUMP_SZ))
            overlap_warn += 1

        pump_focus_ind = np.argmin(beam_sz_pu)
        pump_focus_x = xypos_pu[pump_focus_ind, 0]
        pump_focus_y = xypos_pu[pump_focus_ind, 1]

        pump_focus_z = Z1[pump_focus_ind]
        if pump_focus_z < MIN_PUMP_FOCUS_Z:
            logger.warn("Pump focus Z position is too close " +
                  "(<{:.1f} mm)".format(MIN_PUMP_FOCUS_Z))
            overlap_warn += 1
        if pump_focus_z > MAX_PUMP_FOCUS_Z:
            logger.warn("Pump focus Z position is too far " +
                  "(>{:.1f} mm)".format(MAX_PUMP_FOCUS_Z))
            overlap_warn += 1

        logger.info("Pump focus size is {:.1f} µm FWHM at Z = {:.2f} mm".format(
            pump_focus_sz, pump_focus_z))

    # Calculate XY position wiht respect to probe focus
    if xy_pos_rel_to_z0 and par_pr is not None:
        par_pr['xypos'][:, 0] = par_pr['xypos'][:, 0] - probe_focus_x
        par_pr['xypos'][:, 1] = par_pr['xypos'][:, 1] - probe_focus_y

        if par_pu is not None:
            par_pu['xypos'][:, 0] = par_pu['xypos'][:, 0] - probe_focus_x
            par_pu['xypos'][:, 1] = par_pu['xypos'][:, 1] - probe_focus_y
            pump_focus_x -= probe_focus_x
            pump_focus_y -= probe_focus_y

        probe_focus_x = 0
        probe_focus_y = 0

    if par_pr is not None and par_pu is not None:
        pp_xy_r = np.sqrt((pump_focus_x - probe_focus_x)**2 + (pump_focus_y - probe_focus_y)**2)
        logger.info("XY distance between pump and probe is {:.1f} µm".format(pp_xy_r))
        if pp_xy_r > MAX_PP_XY_R:
            logger.warn("XY distance between pump and probe focus is too large " +
                  "(>{:.1f} µm)".format(MAX_PP_XY_R))
            overlap_warn += 1
            overlap_in_spec = False

    focus_region_size = 0.5
    if fig_style is 'at_focus':
        focus_rng = [probe_focus_z - focus_region_size/2, probe_focus_z + focus_region_size/2]
        if par_pr is not None:
            zpos = par_pr['zpos']
            par_pr['ampl'] = cut_by_x_range(zpos, par_pr['ampl'], rng=focus_rng)[1]
            par_pr['xypos'] = cut_by_x_range(zpos, par_pr['xypos'], rng=focus_rng)[1]
            par_pr['zpos'], par_pr['width'] = cut_by_x_range(zpos, par_pr['width'], rng=focus_rng)
        if par_pu is not None:
            zpos = par_pu['zpos']
            par_pu['ampl'] = cut_by_x_range(zpos, par_pu['ampl'], rng=focus_rng)[1]
            par_pu['xypos'] = cut_by_x_range(zpos, par_pu['xypos'], rng=focus_rng)[1]
            par_pu['zpos'], par_pu['width'] = cut_by_x_range(zpos, par_pu['width'], rng=focus_rng)

    if par_pu is not None:
        [plot_xl1, plot_yl1, plot_zl1, plot_wl1] = GetDataRanges(par_pu)

    if par_pr is not None:
        [plot_xl2, plot_yl2, plot_zl2, plot_wl2] = GetDataRanges(par_pr)

    if(mode == 'pinhole'):
        ampl_units = 'T'
        I01 = GetCalibInputPower(beam='Pump')
        I02 = GetCalibInputPower(beam='Probe')
        if(isnone(I01) or isnone(I02)):
            logger.warn("Could not determine calibration input beam power. Normalizing to maximum measured values.")
            I01 = np.max(Imax1)
            I02 = np.max(Imax2)
            ampl_units = 'a.u.'
    elif(mode == 'camera'):
        if par_pu is not None:
            max_ampl_pu = np.max(par_pu['ampl'])
            par_pu['ampl'] = par_pu['ampl']/max_ampl_pu

        if par_pr is not None:
            max_ampl_pr = np.max(par_pr['ampl'])
            par_pr['ampl'] = par_pr['ampl']/max_ampl_pr

        ampl_units = 'a.u.'

    if par_pu is not None and par_pr is not None:
        xlims = [plot_xl1, plot_xl2]
        ylims = [plot_yl1, plot_yl2]
        zlims = [plot_zl1, plot_zl2]
        wlims = [plot_wl1, plot_wl2]
    elif par_pu is not None:
        xlims = [plot_xl1]
        ylims = [plot_yl1]
        zlims = [plot_zl1]
        wlims = [plot_wl1]
    elif par_pr is not None:
        xlims = [plot_xl2]
        ylims = [plot_yl2]
        zlims = [plot_zl2]
        wlims = [plot_wl2]

    plot_xl = get_common_range(xlims, mode='bound', expand_frac=0.1)
    plot_yl = get_common_range(ylims, mode='bound', expand_frac=0.1)
    if isnone(plot_wl):
        plot_wl = [0, 75]
        logger.info("Setting width axis range " +
                    "from {:.0f} µm ".format(plot_wl[0]) +
                    "to {:.0f} µm".format(plot_wl[1]))

        #plot_wl = get_common_range(wlims, mode='bound', expand_frac=0.1)
    plot_zl = get_common_range(zlims, mode='bound')

    plt.figure(figsize=[10, 8])
    subplot_col = 1
    if(mode == 'camera'):
        subplot_cols = 3
        z_ax = None
        showxlabel=True
    elif(mode == 'pinhole'):
        subplot_cols = 4
        z_ax = plt.subplot(subplot_rows, subplot_cols, subplot_col+subplot_row*subplot_cols)
        subplot_col = subplot_col+1
        if subplot_row==1:
            showxlabel=True
        else:
            showxlabel=False

    w_ax = plt.subplot(subplot_rows, subplot_cols, subplot_col+subplot_row*subplot_cols)
    subplot_col = subplot_col+1
    x_ax = plt.subplot(subplot_rows, subplot_cols, subplot_col+subplot_row*subplot_cols)
    subplot_col = subplot_col+1
    y_ax = plt.subplot(subplot_rows, subplot_cols, subplot_col+subplot_row*subplot_cols)
    subplot_col = subplot_col+1

    # pump, probe
    colors = [get_color('db'), get_color('dr')]
    fill_colors = [get_color('b'), get_color('r')]

    if(WithCube):
        z_axes_ylabel_preffix = 'With Cube\n'
    else:
        z_axes_ylabel_preffix = 'No Cube\n'

    if par_pr is not None:
        [z_focus_pr, w_at_focus_pr, x_at_focus_pr, y_at_focus_pr] = PlotXYZScan(par_pr['zpos'], par_pr['ampl'], par_pr['xypos'], par_pr['width'], \
            mode = mode, fit_focus_curve=False, \
            z_axes=z_ax, w_axes=w_ax, x_axes=x_ax, y_axes=y_ax, xl=plot_xl, yl=plot_yl, zl=plot_zl, wl=plot_wl,
            color=colors[1], fill_color=fill_colors[1],
            with_titles=False, showxlabel=showxlabel, Imax_units=ampl_units, width_metric=width_metric)
    if par_pu is not None:
        [z_focus_pu, w_at_focus_pu, x_at_focus_pu, y_at_focus_pu] = PlotXYZScan(par_pu['zpos'], par_pu['ampl'], par_pu['xypos'], par_pu['width'], \
            mode = mode, \
            ref_focus=z_focus_pr, show_focus_marker=False, z_axes=z_ax, w_axes=w_ax, x_axes=x_ax, y_axes=y_ax, xl=plot_xl, yl=plot_yl, zl=plot_zl, wl=plot_wl,
            color=colors[0], fill_color=fill_colors[0],
            with_titles=False, showxlabel=showxlabel, z_axes_ylabel_preffix=z_axes_ylabel_preffix, Imax_units=ampl_units, width_metric=width_metric)

    if par_pu is not None and par_pr is not None:
        overlap_ratio = w_at_focus_pu/w_at_focus_pr

        if overlap_ratio < MIN_OVERLAP_RATIO:
            logger.warn("Overlap ratio is too small, increase pump focus size")
            overlap_warn += 1
            overlap_in_spec = False
        if overlap_ratio > MAX_OVERLAP_RATIO:
            logger.warn("Overlap ratio is too large, decrease pump focus size")
            overlap_warn += 1
            overlap_in_spec = False

    if mode == 'pinhole':
        plt.sca(z_ax)
        plt.title('Z offset {:.1f} µm\nPump at {:.1f} µm, probe at {:.1f} µm'.format(z_focus_pr - z_focus_pu, z_focus_pu, z_focus_pr))

    plt.sca(w_ax)
    overlap_str = ''
    if par_pu is not None and par_pr is not None:
        overlap_str += 'Pu/Pr FWHM overlap {:.1f}\n'.format(overlap_ratio)
    if par_pu is not None:
        overlap_str += 'Pump: {:.1f} µm'.format(w_at_focus_pu)
    if par_pr is not None:
        overlap_str += ' Probe: {:.1f} µm'.format(w_at_focus_pr)
    if not par_pu is not None or not par_pr is not None:
        overlap_str += ' FHWM'
    plt.title(overlap_str)

    plt.sca(x_ax)
    xofs_str = ''
    if par_pu is not None and par_pr is not None:
        xofs_str += 'X offset {:.1f} µm\n'.format(x_at_focus_pr - x_at_focus_pu)
    if par_pu is not None:
        xofs_str += 'Pump at {:.1f} µm'.format(x_at_focus_pu)
    if par_pr is not None:
        xofs_str += ' Probe at {:.1f} µm'.format(x_at_focus_pr)
    plt.title(xofs_str)

    plt.sca(y_ax)
    yofs_str = ''
    if par_pu is not None and par_pr is not None:
        yofs_str += 'Y offset {:.1f} µm\n'.format(y_at_focus_pr - y_at_focus_pu)
    if par_pu is not None:
        yofs_str += 'Pump at {:.1f} µm'.format(y_at_focus_pu)
    if par_pr is not None:
        yofs_str += ' Probe at {:.1f} µm'.format(y_at_focus_pr)
    plt.title(yofs_str)

    if suptitle_str is None:
        suptitle_str = "Overlap report"

    if device_sn is not None:
        suptitle_str += ", " + device_sn

    if obj_ind is not None:
        objective_str = ['unspecified objective', 'Nikon Plan Fluor 4x/0.13', 'Nikon Plan Fluor 10x/0.3'][obj_ind]
        suptitle_str += ", " + objective_str

    if date_str is None:
        date_str = time.strftime("%Y-%m-%d %H:%M")

    suptitle_str += ", " + date_str

    if overlap_in_spec:
        suptitle_str += "\n"
        suptitle_str += "Overlap is in spec"
    else:
        suptitle_str += "\n"
        suptitle_str += "Overlap is NOT IN SPEC, number of overlap-related warnings: {:d}".format(overlap_warn)

    plt.suptitle(suptitle_str)

    plt.gcf().set_size_inches(17, 5*subplot_rows + 1)
    if fig_style is 'whole_range':
        fig_name = 'Overlap_whole.pdf'
    if fig_style is 'at_focus':
        fig_name = 'Overlap_focus.pdf'

    plt.savefig(fig_name)

    logger.info("Generating GIFs...")
    if par_pu is not None:
        try:
            MakeXYProfileGIF(path=path_pu)
        except:
            logger.warn("Could not generate pump overlap GIF. " + get_exception_info_str())

    if par_pr is not None:
        try:
            MakeXYProfileGIF(path=path_pr)
        except:
            logger.warn("Could not generate probe overlap GIF. " + get_exception_info_str())

    plt.gcf().tight_layout(pad=3)

    logger.info("Showing report figure")

    plt.show()

def PlotXYZScan(
    Z=None, Imax=None, C=None, W=None, width_metric='mean', mode='pinhole', show_focus_marker=True,
    ref_focus=None, z_axes=None, x_axes=None, y_axes=None, xy_axes=None,
    w_axes=None, xl=None, yl=None, zl=None, wl=None, color=None, show_fill=True, fill_color=None,
    with_titles=True, showxlabel=True, z_axes_ylabel_preffix=None, Imax_units=None,
    **kwargs):

    if(not isnone(ref_focus)):
        focus_marker_color = get_color('dr')
    else:
        focus_marker_color = color

    xpos = C[:, 0]
    ypos = C[:, 1]

    # Plot transmission panel
    if(mode == 'pinhole'):
        plt.sca(z_axes)
        plt.plot(Z,Imax,'.',c=color)

        z_focus = FindFocusPosition(Z=Z,Imax=Imax,color=color,yl=[0,1.1])

        if(isnone(ref_focus)):
            ref_focus = z_focus

        plt.plot([ref_focus, ref_focus], zl, c=focus_marker_color, ls='--')

        if(showxlabel):
            plt.xlabel('Z position, µm')

        ylabel_str = 'Transmission, {:s}'.format(Imax_units)
        if(not isnone(z_axes_ylabel_preffix)):
            ylabel_str = z_axes_ylabel_preffix + ylabel_str
        plt.ylabel(ylabel_str)
        if(with_titles):
            plt.title('Focus position at Z = {:.1f} µm'.format(z_focus))
        plt.xlim(zl)
        plt.ylim([0,1.1])
        plt.draw()

    # Plot width panel
    plt.sca(w_axes)
    if width_metric is 'mean':
        # No point showing x and y widths separately, show averge
        Wm = np.mean(W, 1)
    elif width_metric is 'min':
        Wm = np.min(W, 1)
    elif width_metric is 'max':
        Wm = np.max(W, 1)
    else:
        print('Undefined width mean metric')

    if show_fill:
        plt.fill_between(Z, W[:,0], W[:,1], color=fill_color)

    plt.plot(Z, Wm, c=color, linestyle='solid', marker='.')

    if(mode == 'camera'):
        z_focus = FindFocusPosition(Z=Z, Imax=Wm, color=color, yl=[0,1.1], mode='min', focus_fit_range=2000, plot=False, **kwargs)
        if(isnone(ref_focus)):
            ref_focus = z_focus

    if(show_focus_marker):
        plt.plot([ref_focus, ref_focus], wl, c=focus_marker_color, ls='--')

    w_at_focus = np.interp(ref_focus, Z, Wm)
    plt.plot(zl, [w_at_focus, w_at_focus], c=color, ls='--')
    if(showxlabel):
        plt.xlabel('Z position, µm')
    plt.ylabel('FWHM, µm ')
    if(with_titles):
        plt.title('FWHM={:.1f} µm'.format(w_at_focus))
    plt.xlim(zl)
    plt.ylim(wl)
    plt.grid('on')
    add_x_marker(0, ls='-')
    plt.draw()

    # Plot X position panel
    plt.sca(x_axes)
    plt.plot(Z, xpos, c=color, marker='.')
    plt.plot([ref_focus,ref_focus],xl,c=focus_marker_color,ls='--')
    x_at_focus = np.interp(ref_focus, Z, xpos)
    plt.plot(zl,[x_at_focus,x_at_focus],c=color,ls='--')
    if(showxlabel):
        plt.xlabel('Z position, µm')
    plt.ylabel('X position, µm ')
    if(with_titles):
        plt.title('Focus position at X={:.1f} µm'.format(x_at_focus))
    plt.xlim(zl)
    plt.ylim(xl)
    plt.grid('on')
    add_x_marker(0, ls='-')
    add_y_marker(0, ls='-')
    plt.draw()

    # Plot Y position panel
    plt.sca(y_axes)
    plt.plot(Z, ypos, c=color, marker='.')
    plt.plot([ref_focus,ref_focus],yl,c=focus_marker_color,ls='--')
    y_at_focus = np.interp(ref_focus, Z, ypos)
    plt.plot(zl,[y_at_focus,y_at_focus],c=color,ls='--')
    if(showxlabel):
        plt.xlabel('Z position, µm')
    plt.ylabel('Y position, µm ')
    if(with_titles):
        plt.title('Focus position at Y={:.1f} µm'.format(y_at_focus))
    plt.xlim(zl)
    plt.ylim(yl)
    plt.grid('on')
    add_x_marker(0, ls='-')
    add_y_marker(0, ls='-')
    plt.draw()

    return [z_focus, w_at_focus, x_at_focus, y_at_focus]

def GetDataRanges(par):
    zpos = par['zpos']
    ampl = par['ampl']
    xypos = par['xypos']
    width = par['width']
    dataSpanX = np.max(xypos[:,0]) - np.min(xypos[:,0])
    plot_xl = [ np.min(xypos[:,0]) - dataSpanX*0.1, np.max(xypos[:,0]) + dataSpanX*0.1 ]
    dataSpanY = np.max(xypos[:,1]) - np.min(xypos[:,1])
    plot_yl = [ np.min(xypos[:,1]) - dataSpanY*0.1, np.max(xypos[:,1]) + dataSpanY*0.1 ]

    plot_zl = [np.min(zpos), np.max(zpos)]

    width_avg = np.mean(width, 1)
    dataSpanwidth = np.max(width_avg) - np.min(width_avg)
    plot_wl = [ np.min(width_avg) - dataSpanwidth*0.1, np.max(width_avg) + dataSpanwidth*0.1 ]

    return [plot_xl, plot_yl, plot_zl, plot_wl]

def FindFocusPosition(Z=None, Imax=None, color=None, yl=None, focus_fit_range=600, mode='max', fit_focus_curve=True, show_focus_marker=False, plot=True):
    if(mode=='max'):
        z_focus_est = Z[np.argmax(Imax)]
    elif(mode=='min'):
        z_focus_est = Z[np.argmin(Imax)]

    # print.info("Estimated Z focus position: {:.1f} mm".format(z_focus_est))

    if(z_focus_est>np.max(Z) or z_focus_est<np.min(Z)):
        Z_fd = Z
        Imax_fd = Imax
    else:
        [ Z_fd, Imax_fd ] = cut_by_x_range(Z, Imax, rng_fr = z_focus_est - focus_fit_range/2, rng_to = z_focus_est + focus_fit_range/2)

    if(len(Z_fd) < 3):
        print("Warning: not enough points to find focal position")

    if fit_focus_curve:
        try:
            popt = fit_poly_2(X=Z_fd,Y=Imax_fd,plot_fit=False,color=color)[0]
            z_focus = get_poly_2_max_x(popt)

            if plot:
                Z_all = np.linspace(Z.min(),Z.max(),100)
                plt.plot(Z_all,poly_2(Z_all,popt[0],popt[1],popt[2]),color=color,ls='--')
                if(show_focus_marker):
                    plt.plot([z_focus,z_focus],yl,color=color,ls='--')
        except:
            z_focus = z_focus_est
    else:
        z_focus = z_focus_est

    return z_focus

def GenerateCombinedFocusingGIF(verbose=False):
    path_pu = r"Pump no Cube"
    path_pr = r"Probe no Cube"

    print("Enumerating pump files...")
    [file_names_pu, Z_arr_pu] = enum_files(path=path_pu, extension="dat", preffix="I", files_to_remove=".\\I.dat", prepend_path=True, verbose=verbose)
    print("Enumerating probe files...")
    [file_names_pr, Z_arr_pr] = enum_files(path=path_pr, extension="dat", preffix="I", files_to_remove=".\\I.dat", prepend_path=True, verbose=verbose)

    print("Reading pump images...")
    images_pu = load_img(file_names=file_names_pu)
    print("Reading probe images...")
    images_pr = load_img(file_names=file_names_pr)

    images = comb_img(images_pu, images_pr)

    labels = []
    for Z in Z_arr_pr:
        labels.append("Z={:+d}".format(int(np.round(Z/10)*10)))

    make_gif(images=images, labels=labels, resize=True, verbose=verbose)