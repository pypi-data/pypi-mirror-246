#!/usr/bin/env python
# -*- coding: utf-8 -*-
#===============================================================================
# Generate a pump-probe XYZ overlap summary figure showing the dependency of
# intensity, beam size and center positions as a function of Z.
#-------------------------------------------------------------------------------
#
# Copyright (c) 2019-2020 Light Conversion
# All rights reserved.
# www.lightcon.com
#===============================================================================

import os
from harpiamm.harpiamm import PlotOverlapScanSummaryFigure

suptitle_str="Overlap report"
PlotOverlapScanSummaryFigure(suptitle_str=suptitle_str)
input("Press any key to close this window")
