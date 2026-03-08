# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2012 Milos Koutny <milos.koutny@gmail.com>
# SPDX-FileNotice: Part of the IDF addon.

from .Misc import Paths


## path to table file (simple comma separated values)

model_tab_filename = str( Paths[ 'Resources' ] / 'Models.csv' )

## path to directory containing step models

ignore_hole_size=0.5 # size in MM to prevent huge number of drilled holes
EmpDisplayMode=2 # 0='Flat Lines', 1='Shaded', 2='Wireframe', 3='Points'; recommended 2 or 0

IDF_sort=0 # 0-sort per refdes [1 - part number (not preferred)/refdes] 2-sort per footprint/refdes

IDF_diag=0 # 0/1=disabled/enabled output (footprint.lst/missing_models.lst)
IDF_diag_path="/tmp" # path for output of footprint.lst and missing_models.lst