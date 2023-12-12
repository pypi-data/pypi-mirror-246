#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
=== delay_line_test ===

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
#import clr
import time
import os
import sys

from tkinter import *
from tkinter import ttk
import threading

import numpy as np

import matplotlib.pyplot as plt

from lightcon.harpia import Harpia
from lightcon.camera_app_client import CameraApp

clear_axes = False

def measure_func():
    global clear_axes
    # HARPIA address
    deviceAddress = '127.0.0.1'

    # Camera address
    cam_address = '127.0.0.1'

    print("HARPIA Delay Line Alignment Tool")
    H = Harpia(deviceAddress)
    cam = CameraApp(cam_address)

    H.open_probe_shutter()
    H.close_pump_shutter()

    plt.figure(1)
    plt.clf()
    ax_x = plt.subplot(2, 1, 1)
    ax_y = plt.subplot(2, 1, 2)

    min_x = None
    max_x = None

    min_y = None
    max_y = None

    while(1):
        delay = H.delay_line_actual_delay()
        beam_par = cam.get_beam_parameters()
        beam_x = beam_par.get('MeanX')
        beam_y = beam_par.get('MeanY')
        print("Beam position: {:.2f}, {:.2f} mm at  {:.2f} ns".format(beam_x, beam_y, delay/1000))

        if clear_axes:
            min_x = None
            max_x = None
            min_y = None
            max_y = None

        if min_x is None:
            min_x = beam_x
            max_x = beam_x
        
        if min_y is None:
            min_y = beam_y
            max_y = beam_y

        if beam_x < min_x:
            min_x = beam_x

        if beam_x > max_x:
            max_x = beam_x

        if beam_y < min_y:
            min_y = beam_y
        
        if beam_y > max_y:
            max_y = beam_y

        plt.sca(ax_x)
        if clear_axes:
            plt.cla()
        plt.scatter(delay, beam_x, c='k')
        plt.title("Variation X: {:.1f} um, Y: {:.1f} um".format((max_x - min_x)*1000, (max_y - min_y)*1000))
        plt.sca(ax_y)
        if clear_axes:
            plt.cla()
        plt.scatter(delay, beam_y, c='k')
        if clear_axes:
            clear_axes = False
        plt.pause(0.05)

    H.close_probe_shutter()
    H.close_pump_shutter()

def reset_graph():
    global clear_axes
    clear_axes = True
    print("Reset graph")

def delay_line_alignment():
    # Main
    start_t = time.time()

    root = Tk()
    root.title("HARPIA Delay Line Alignment Tool")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    ttk.Button(mainframe, text="Reset", command=reset_graph).grid(column=0, row=0, sticky=W)

    root.bind('<Return>', reset_graph)

    x = threading.Thread(target=measure_func, daemon=True)
    x.start()

    root.mainloop()
    