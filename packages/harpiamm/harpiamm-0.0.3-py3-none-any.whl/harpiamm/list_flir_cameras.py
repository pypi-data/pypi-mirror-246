#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
=== list_flir_cameras ===

List FLIR cameras connected to the computer.

Author: Lukas Kontenis
Copyright (c) 2019-2020 Light Conversion
All rights reserved.
www.lightcon.com
"""
import PySpin

system = PySpin.System.GetInstance()
cam_list = system.GetCameras()

if len(cam_list) > 0:
    print("Camera list:")
    for ind, cam in enumerate(cam_list):
        print("Cam {:d}, SN: {:s}".format(ind, cam.GetUniqueID()))
else:
    print("No cameras found")
