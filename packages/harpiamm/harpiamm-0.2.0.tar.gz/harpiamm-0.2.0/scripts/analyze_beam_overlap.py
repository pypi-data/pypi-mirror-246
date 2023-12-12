#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Pump-probe overlap analysis script.
M
Generate a pump-probe XYZ overlap report. The report contains three panels
which show the FWHM beam size and the focus X and Y position as a function of
the Z position.

Please specify the objective type and the device serial number

This script is a part of the HARPIA Microscopy Kit, which is a set of tools for
the alignment, characterization and troubleshooting of HARPIA-MM Microscopy
Extension.

Contact: lukas.kontenis@lightcon.com, support@lightcon.com

Copyright (c) 2019-2023 Light Conversion
All rights reserved.
www.lightcon.com
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
from harpiamm.harpiamm import make_overlap_report

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QWidget()

    data_path = QFileDialog.getExistingDirectory(
        widget, "Select folder containing Pump/Probe focus image data")

    # If the obj_id and device_sn arguments are not set a dialog will be shown
    # foruser input. Set these arguments using:
    #   obj_id='nikon_pf_10x'
    #   device_sn="M00000"
    # The following objective ids are supported: nikon_pf_4x, nikon_pf_10x
    # The device serial number must be in the M00000 format

    make_overlap_report(path=data_path)
    input("Press any key to close this window")
