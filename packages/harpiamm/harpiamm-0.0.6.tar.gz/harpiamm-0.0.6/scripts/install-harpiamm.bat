@echo off

:: HARPIA Microscopy Kit installation script
:: 
:: Contact: lukas.kontenis@lightcon.com, support@lightcon.com
:: Copyright (c) 2019-2021 Light Conversion
:: All rights reserved.
:: www.lightcon.com

echo Installing HARPIA Microscopy Kit
python -m pip --disable-pip-version-check install --index-url https://test.pypi.org/simple --extra-index-url https://pypi.python.org/simple harpiamm

echo Making sure conflicting packages are not installed
python -m pip --disable-pip-version-check uninstall -y clr
