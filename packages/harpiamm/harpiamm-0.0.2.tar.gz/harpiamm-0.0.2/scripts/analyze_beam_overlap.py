#!/usr/bin/env python
# -*- coding: utf-8 -*-
#===============================================================================
# Generate a pump-probe XYZ overlap summary figure showing the dependency of
# intensity, beam size and center positions as a function of Z.
#-------------------------------------------------------------------------------
#
# Copyright (c) 2019 Light Conversion
# All rights reserved.
# www.lightcon.com
#===============================================================================

import os
from harpiamm.harpiamm import PlotOverlapScanSummaryFigure

suptitle_str="4x M20038"
PlotOverlapScanSummaryFigure(suptitle_str=suptitle_str)
#PlotOverlapScanSummaryFigure(fig_style='at_focus', suptitle_str=suptitle_str)
print("Press any key to close this window")
input()

