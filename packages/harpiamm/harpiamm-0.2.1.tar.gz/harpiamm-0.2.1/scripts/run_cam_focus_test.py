#!/usr/bin/env python
# -*- coding: utf-8 -*-
#===============================================================================
# Acquire pump-probe XYZ overlap images using a sample plane camera.
#-------------------------------------------------------------------------------
#
# Copyright (c) 2019-2020 Light Conversion
# All rights reserved.
# www.lightcon.com
#===============================================================================

from harpiamm.cam_focus_test import cam_focus_test

cam_focus_test(start_pos=-2, end_pos=2, num_steps=50, cam_sn='19105005')
