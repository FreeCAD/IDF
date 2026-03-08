# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2012 Milos Koutny <milos.koutny@gmail.com>
# SPDX-FileNotice: Part of the IDF addon.

import FreeCAD, os

from FreeCAD import Console
from .EMN import process


def open ( path ):

    file = os.path.basename(path)

    [ name , _ ] = os.path.splitext(file)

    document = FreeCAD.newDocument(name)

    Console.PrintMessage('Started with opening of { file } file\n')

    process(document,path)


def insert ( path , name ):

    FreeCAD.setActiveDocument(name)

    document = FreeCAD.getDocument(name)

    Console.PrintMessage('Started import of { file } file')

    process(document,path)
