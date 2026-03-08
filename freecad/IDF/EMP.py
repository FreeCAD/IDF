# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2012 Milos Koutny <milos.koutny@gmail.com>
# SPDX-FileNotice: Part of the IDF addon.

from builtins import open
from FreeCAD import Placement , Console , Vector
from math import pi

from .Component_Outline import Process_comp_outline
from .Constants import IDF_diag_path , EmpDisplayMode , IDF_diag
from .Helper import toQuaternion
from .Steps import split_records


def process_emp(doc,filename,placement,board_thickness):
   """process_emp(doc,filename,placement,board_thickness) -> place components from emn file to board"""
   filename=filename.partition(".emn")[0]+".emp"
   empfile=open(filename, "r")
   emp_unit=1.0 #presume millimeter like emn unit
   emp_version=2 #presume emn_version 2
   comp_height=0 #presume 0 part height
   comp_outline=[] #no part outline
   comp_GeometryName="" # no geometry name
   comp_PartNumber="" # no Part Number
   comp_height=0 # no Comp Height
   emplines=empfile.readlines()
   empfile.close()
   passed_sections=[]
   current_section=""
   section_counter=0
   comps=[]
   for empline in emplines:
     emprecords=split_records(empline)
     if len( emprecords )==0 : continue
     if len( emprecords[0] )>4 and emprecords[0][0:4]==".END":
        passed_sections.append(current_section)
        current_section=""
        if comp_PartNumber!="":
          if comp_height==0:
            comp_height=0.1
          comps.append((comp_PartNumber,[Process_comp_outline(doc,comp_outline,comp_height),comp_GeometryName]))
          comp_PartNumber=""
          comp_outline=[]
     elif emprecords[0][0]==".":
        current_section=emprecords[0]
        section_counter=0
     section_counter+=1
     if current_section==".HEADER"  and section_counter==2:
        emp_version=int(float(emprecords[1]))
        Console.PrintMessage("Emp version: "+emprecords[1]+"\n")
     if (current_section==".ELECTRICAL" or current_section==".MECHANICAL") and section_counter==2 and emprecords[2]=="THOU":
        emp_unit=0.0254
     if (current_section==".ELECTRICAL" or current_section==".MECHANICAL") and section_counter==2 and emprecords[2]=="MM":
        emp_unit=1
     if (current_section==".ELECTRICAL" or current_section==".MECHANICAL") and section_counter==2:
        comp_outline=[] #no part outline
        comp_GeometryName=emprecords[0] # geometry name
        comp_PartNumber=emprecords[1] # Part Number
        comp_height=emp_unit*float(emprecords[3]) # Comp Height
     if (current_section==".ELECTRICAL" or current_section==".MECHANICAL") and section_counter>2:
        comp_outline.append([float(emprecords[1])*emp_unit,float(emprecords[2])*emp_unit,float(emprecords[3])]) #add point of outline
   Console.PrintMessage("\n".join(passed_sections)+"\n")
   #Write file with list of footprint
   if IDF_diag==1:
     empfile=open(IDF_diag_path+"/footprint.lst", "w")
     for compx in comps:
       empfile.writelines(str(compx[1][1])+"\n")
     empfile.close()
   #End section of list footprint
   comps=dict(comps)
   grp=doc.addObject("App::DocumentObjectGroup", "EMP Models")
   for place_item in placement:
     if place_item[1] in comps:
       doc_comp=doc.addObject("Part::Feature",place_item[0])
       Console.PrintMessage("Adding EMP model "+str(place_item[0])+"\n")
       doc_comp.Shape=comps[place_item[1]][0]
       doc_comp.ViewObject.DisplayMode=EmpDisplayMode
       z_pos=0
       rotateY=0
       if place_item[6]=='BOTTOM':
          rotateY=pi
          z_pos=-board_thickness
       placmnt=Placement(Vector(place_item[3],place_item[4],z_pos),toQuaternion(rotateY,place_item[5]*pi/180,0))
       doc_comp.Placement=placmnt
       grp.addObject(doc_comp)
   return 1