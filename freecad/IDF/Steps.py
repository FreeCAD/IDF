# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2012 Milos Koutny <milos.koutny@gmail.com>
# SPDX-FileNotice: Part of the IDF addon.

from ImportGui import insert
from builtins import open
from FreeCAD import activeDocument , Placement , Console , Vector
from math import pi

from .Constants import model_tab_filename , IDF_diag_path , IDF_diag
from .Models import split_records
from .Helper import toQuaternion
from .Misc import asModel



def place_steps(doc,placement,board_thickness):
    """ place_steps(doc,placement,board_thickness)->place step models on board

        list of models and path to step files is set at start of this script
                 model_tab_filename= "" &   step_path="" """
    model_file=open(model_tab_filename, "r")
    model_lines=model_file.readlines()
    model_file.close()
    model_dict=[]
    if IDF_diag==1:
        model_file=open(IDF_diag_path+"/missing_models.lst", "w")
    keys=[]
    step_dict=[]
    for model_line in model_lines:
        model_records=split_records(model_line)
        if len(model_records)>1 and model_records[0] and not model_records[0] in keys:
           keys.append(model_records[0])
           model_dict.append((str(model_records[0]).replace('"',''),str(model_records[1]).replace('"','')))
    model_dict=dict(model_dict)
    validkeys=filter(lambda x:x in  [place_item[2] for place_item in placement], model_dict.keys())
    Console.PrintMessage("Step models to be loaded for footprints: "+str(validkeys)+"\n")
    grp=doc.addObject("App::DocumentObjectGroup", "Step Lib")
    for validkey in validkeys:
        print('Key',validkey,model_dict[validkey])
        path = asModel(model_dict[validkey])

        document = activeDocument()

        insert(path,document.Name)
        impPart=document.ActiveObject
        impPart.ViewObject.Visibility=0
        impPart.Label=validkey
        grp.addObject(impPart)
        step_dict.append((validkey,impPart))
        Console.PrintMessage("Reading step file "+str(model_dict[validkey])+" for footprint "+str(validkey)+"\n")
    step_dict=dict(step_dict)
    grp=doc.addObject("App::DocumentObjectGroup", "Step Models")
    for place_item in placement:
      if place_item[2] in step_dict:
        step_model=doc.addObject("Part::Feature",place_item[0]+"_s")
        Console.PrintMessage("Adding STEP model "+str(place_item[0])+"\n")
        step_model.Shape=step_dict[place_item[2]].Shape
        step_model.ViewObject.DiffuseColor=step_dict[place_item[2]].ViewObject.DiffuseColor
        z_pos=0
        rotateY=0
        if place_item[6]=='BOTTOM':
           rotateY=pi
           z_pos=-board_thickness
        placmnt=Placement(Vector(place_item[3],place_item[4],z_pos),toQuaternion(rotateY,place_item[5]*pi/180,0))
        step_model.Placement=placmnt
        grp.addObject(step_model)
      else:
        if IDF_diag==1:
            model_file.writelines(str(place_item[0])+" "+str(place_item[2])+"\n")
            model_file.close()

