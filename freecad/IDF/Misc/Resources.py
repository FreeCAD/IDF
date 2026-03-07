# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the IDF addon.

import freecad.IDF as module
from importlib.resources import as_file , files

resources = files(module) / 'Resources'

models = resources / 'Models'


Paths = {
    "Resources" : resources
}


def asModel ( file : str ):

    model = models / file

    with as_file(model) as path:
        return str( path )
