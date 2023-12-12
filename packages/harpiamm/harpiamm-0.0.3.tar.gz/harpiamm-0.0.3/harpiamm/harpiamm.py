"""
=== harpiamm ===

HARPIA microscopy module routines.

Author: Lukas Kontenis
Copyright (c) 2019-2020 Light Conversion
All rights reserved.
www.lightcon.com
"""

import os
import xmltodict
import numpy as np
import matplotlib.pyplot as plt

from scipy.ndimage.measurements import center_of_mass
from PIL import Image

from lklib.fileread import enum_files, join_paths, check_file_exists
from lklib.util import cut_by_x_range, get_common_range, isarray, isnone, handle_general_exception, find_closest, get_color
from lklib.fit import fit_gaussian_2d, fit_poly_2, get_poly_2_max_x
from lklib.standard_func import poly_2
from lklib.image import make_gif, load_img, comb_img
from lklib.plot import add_x_marker, add_y_marker


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
            print("Loading stored fit parameters")
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

def PlotOverlapScanSummaryFigure(
    path=r'./', width_metric='mean',
    xy_pos_rel_to_z0=True,
    mode='camera', WithCube=False, subplot_rows=1, subplot_row=0, fig_style='whole_range', plot_wl=None, suptitle_str=None):
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
        print("Getting pump focus parameters...")
        [Z1, Imax1, xypos_pu, W1] = GetXYZOverlapScanData(path=path_pu, WithCube=WithCube, mode=mode)
        pump_data_available = True
    except:
        print("Pump data not available")
        pump_data_available = False

    try:
        print("Getting probe focus parameters...")
        [Z2, Imax2, xypos_pr, W2] = GetXYZOverlapScanData(path=path_pr, WithCube=WithCube, mode=mode)
        probe_data_available = True
    except:
        probe_data_available = False

    if not pump_data_available and not probe_data_available:
        print("Neither pump nor probe data is available")
        return

    # Minimum and maximum intensity values to check for bad fit values. Th
    # maximum value needs to be larger than 255 even though the data is capped
    # at 255. Gaussian fits with narrow widths can spike above this value and
    # still be valud.

    min_imax = 10
    max_imax = 300
    if pump_data_available:
        imax_check = np.logical_or(Imax1 > max_imax, Imax1 < min_imax)
        if imax_check.any():
            print("Some pump intensity fit values are outside of the valid range")
        failed_pts = np.logical_or(np.logical_or(np.isnan(Z1), np.isnan(W1[:,0])), imax_check)
        if failed_pts.all():
            print("All pump fit values failed, there is no valid pump data")
            pump_data_available = False
        elif failed_pts.any():
            print("Some pump fit values failed, removing...")
            Z1 = Z1[np.logical_not(failed_pts)]
            Imax1 = Imax1[np.logical_not(failed_pts)]
            xypos_pu = xypos_pu[np.logical_not(failed_pts), :]
            W1 = W1[np.logical_not(failed_pts), :]

    if probe_data_available:
        imax_check = np.logical_or(Imax2 > max_imax, Imax2 < min_imax)
        if imax_check.any():
            print("Some probe intensity fit values are outside of the valid range")
        failed_pts = np.logical_or(np.logical_or(np.isnan(Z2), np.isnan(W2[:,0])), imax_check)
        if failed_pts.all():
            print("All probe fit values failed, there is no valid pump data")
            probe_data_available = False
        elif failed_pts.any():
            print("Some probe fit values failed, removing...")
            Z2 = Z2[np.logical_not(failed_pts)]
            Imax2 = Imax2[np.logical_not(failed_pts)]
            xypos_pr = xypos_pr[np.logical_not(failed_pts), :]
            W2 = W2[np.logical_not(failed_pts), :]

    if xy_pos_rel_to_z0:
        if pump_data_available:
            z0_ind = find_closest(Z1, 0)
            xypos_pu -= xypos_pu[z0_ind, :]

        if probe_data_available:
            z0_ind = find_closest(Z2, 0)
            xypos_pr -= xypos_pr[z0_ind, :]

    if probe_data_available:
        beam_sz_pr = np.sqrt(np.mean(W2**2, 1))
        probe_focus_sz = np.min(beam_sz_pr)
        probe_focus_ind = np.argmin(beam_sz_pr)
        probe_focus_x = xypos_pr[probe_focus_ind, 0]
        probe_focus_y = xypos_pr[probe_focus_ind, 1]
        probe_focus_z = Z2[probe_focus_ind]
        print("Probe focus {:.1f} um at Z = {:.2f} mm".format(probe_focus_sz, probe_focus_z))

    if pump_data_available:
        beam_sz_pu = np.sqrt(np.mean(W1**2, 1))
        pump_focus_sz = np.min(beam_sz_pu)
        pump_focus_ind = np.argmin(beam_sz_pu)
        pump_focus_x = xypos_pu[pump_focus_ind, 0]
        pump_focus_y = xypos_pu[pump_focus_ind, 1]
        pump_focus_z = Z1[pump_focus_ind]
        print("Pump focus {:.1f} um at Z = {:.2f} mm".format(pump_focus_sz, pump_focus_z))

    if pump_data_available and probe_data_available:
        pump_probe_distance = np.sqrt((pump_focus_x - probe_focus_x)**2 + (pump_focus_y - probe_focus_y)**2)
        print("Distance between pump and probe: r = {:.1f} um".format(pump_probe_distance))

    focus_region_size = 0.5
    if fig_style is 'at_focus':
        focus_rng = [probe_focus_z - focus_region_size/2, probe_focus_z + focus_region_size/2]
        if pump_data_available:
            Imax1 = cut_by_x_range(Z1, Imax1, rng=focus_rng)[1]
            xypos_pu = cut_by_x_range(Z1, xypos_pu, rng=focus_rng)[1]
            Z1, W1 = cut_by_x_range(Z1, W1, rng=focus_rng)
        if probe_data_available:
            Imax2 = cut_by_x_range(Z2, Imax2, rng=focus_rng)[1]
            xypos_pr = cut_by_x_range(Z2, xypos_pr, rng=focus_rng)[1]
            Z2, W2 = cut_by_x_range(Z2, W2, rng=focus_rng)

    if pump_data_available:
        [plot_xl1, plot_yl1, plot_zl1, plot_wl1] = GetDataRanges(Z1, Imax1, xypos_pu, W1)

    if probe_data_available:
        [plot_xl2, plot_yl2, plot_zl2, plot_wl2] = GetDataRanges(Z2, Imax2, xypos_pr, W2)

    if(mode == 'pinhole'):
        Imax_units = 'T'
        I01 = GetCalibInputPower(beam='Pump')
        I02 = GetCalibInputPower(beam='Probe')
        if(isnone(I01) or isnone(I02)):
            RuntimeWarning("Could not determine calibration input beam power. Normalizing to maximum measured values.")
            I01 = np.max(Imax1)
            I02 = np.max(Imax2)
            Imax_units = 'a.u.'
    elif(mode == 'camera'):
        if pump_data_available:
            I01 = np.max(Imax1)

        if probe_data_available:
            I02 = np.max(Imax2)

        Imax_units = 'a.u.'

    if pump_data_available:
        Imax1 = Imax1/I01

    if probe_data_available:
        Imax2 = Imax2/I02

    if pump_data_available and probe_data_available:
        xlims = [plot_xl1, plot_xl2]
        ylims = [plot_yl1, plot_yl2]
        zlims = [plot_zl1, plot_zl2]
        wlims = [plot_wl1, plot_wl2]
    elif not pump_data_available:
        xlims = [plot_xl2]
        ylims = [plot_yl2]
        zlims = [plot_zl2]
        wlims = [plot_wl2]
    elif not probe_data_available:
        xlims = [plot_xl1]
        ylims = [plot_yl1]
        zlims = [plot_zl1]
        wlims = [plot_wl1]

    plot_xl = get_common_range(xlims, mode='bound', expand_frac=0.1)
    plot_yl = get_common_range(ylims, mode='bound', expand_frac=0.1)
    if isnone(plot_wl):
        print("Setting FWHM range from 5 µm to 75 µm")
        plot_wl = [5, 75]
        #plot_wl = get_common_range(wlims, mode='bound', expand_frac=0.1)
    plot_zl = get_common_range(zlims, mode='bound')

    plt.figure()
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

    if probe_data_available:
        [z_focus_pr, w_at_focus_pr, x_at_focus_pr, y_at_focus_pr] = PlotXYZScan(Z2, Imax2, xypos_pr, W2, \
            mode = mode, fit_focus_curve=False, \
            z_axes=z_ax, w_axes=w_ax, x_axes=x_ax, y_axes=y_ax, xl=plot_xl, yl=plot_yl, zl=plot_zl, wl=plot_wl,
            color=colors[1], fill_color=fill_colors[1],
            with_titles=False, showxlabel=showxlabel, Imax_units=Imax_units, width_metric=width_metric)
    if pump_data_available:
        [z_focus_pu, w_at_focus_pu, x_at_focus_pu, y_at_focus_pu] = PlotXYZScan(Z1, Imax1, xypos_pu, W1, \
            mode = mode, \
            ref_focus=z_focus_pr, show_focus_marker=False, z_axes=z_ax, w_axes=w_ax, x_axes=x_ax, y_axes=y_ax, xl=plot_xl, yl=plot_yl, zl=plot_zl, wl=plot_wl,
            color=colors[0], fill_color=fill_colors[0],
            with_titles=False, showxlabel=showxlabel, z_axes_ylabel_preffix=z_axes_ylabel_preffix, Imax_units=Imax_units, width_metric=width_metric)

    if(mode == 'pinhole'):
        plt.sca(z_ax)
        plt.title('Z offset {:.1f} µm\nPump at {:.1f} µm, probe at {:.1f} µm'.format(z_focus_pr - z_focus_pu, z_focus_pu, z_focus_pr))

    plt.sca(w_ax)
    overlap_str = ''
    if pump_data_available and probe_data_available:
        overlap_str += 'Pu/Pr FWHM overlap {:.1f}\n'.format(w_at_focus_pu/w_at_focus_pr)
    if pump_data_available:
        overlap_str += 'Pump: {:.1f} µm'.format(w_at_focus_pu)
    if probe_data_available:
        overlap_str += ' Probe: {:.1f} µm'.format(w_at_focus_pr)
    if not pump_data_available or not pump_data_available:
        overlap_str += ' FHWM'
    plt.title(overlap_str)

    plt.sca(x_ax)
    xofs_str = ''
    if pump_data_available and probe_data_available:
        xofs_str += 'X offset {:.1f} µm\n'.format(x_at_focus_pr - x_at_focus_pu)
    if pump_data_available:
        xofs_str += 'Pump at {:.1f} µm'.format(x_at_focus_pu)
    if probe_data_available:
        xofs_str += ' Probe at {:.1f} µm'.format(x_at_focus_pr)
    plt.title(xofs_str)

    plt.sca(y_ax)
    yofs_str = ''
    if pump_data_available and probe_data_available:
        yofs_str += 'Y offset {:.1f} µm\n'.format(y_at_focus_pr - y_at_focus_pu)
    if pump_data_available:
        yofs_str += 'Pump at {:.1f} µm'.format(y_at_focus_pu)
    if probe_data_available:
        yofs_str += ' Probe at {:.1f} µm'.format(y_at_focus_pr)
    plt.title(yofs_str)

    if suptitle_str is not None:
        plt.suptitle(suptitle_str)

    plt.gcf().set_size_inches(17, 5*subplot_rows + 1)
    if fig_style is 'whole_range':
        fig_name = 'Overlap_whole.pdf'
    if fig_style is 'at_focus':
        fig_name = 'Overlap_focus.pdf'

    plt.savefig(fig_name)

    print("Generating GIFs...")
    if pump_data_available:
        MakeXYProfileGIF(path=path_pu)

    if probe_data_available:
        MakeXYProfileGIF(path=path_pr)

    print("All done")

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

def GetDataRanges(Z=None, Imax=None, C=None, W=None):
    dataSpanX = np.max(C[:,0]) - np.min(C[:,0])
    plot_xl = [ np.min(C[:,0]) - dataSpanX*0.1, np.max(C[:,0]) + dataSpanX*0.1 ]
    dataSpanY = np.max(C[:,1]) - np.min(C[:,1])
    plot_yl = [ np.min(C[:,1]) - dataSpanY*0.1, np.max(C[:,1]) + dataSpanY*0.1 ]

    plot_zl = [np.min(Z), np.max(Z)]

    Wavg = np.mean(W, 1)
    dataSpanW = np.max(Wavg) - np.min(Wavg)
    plot_wl = [ np.min(Wavg) - dataSpanW*0.1, np.max(Wavg) + dataSpanW*0.1 ]

    return [plot_xl, plot_yl, plot_zl, plot_wl]

def FindFocusPosition(Z=None, Imax=None, color=None, yl=None, focus_fit_range=600, mode='max', fit_focus_curve=True, show_focus_marker=False, plot=True):
    if(mode=='max'):
        z_focus_est = Z[np.argmax(Imax)]
    elif(mode=='min'):
        z_focus_est = Z[np.argmin(Imax)]

    print("Estimated Z focus position: {:.1f}".format(z_focus_est))

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