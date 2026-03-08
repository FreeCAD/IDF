# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2012 Milos Koutny <milos.koutny@gmail.com>
# SPDX-FileNotice: Part of the IDF addon.

from builtins import open
from FreeCAD import Console
from math import fmod

from .Board_Outline import Process_board_outline
from .Constants import ignore_hole_size , IDF_sort
from .Models import split_records
from .Steps import place_steps
from .EMP import process_emp


def process ( doc , filename ):

   """process_emn(document, filename)-> adds emn geometry from emn file"""
   emnfile=open(filename, "r")
   emn_unit=1.0 #presume millimeter like emn unit
   emn_version=2 #presume emn_version 2
   board_thickness=0 #presume 0 board height
   board_outline=[] #no outline
   drills=[] #no drills
   placement=[] #no placement
   place_item=[] #empty place item
   emnlines=emnfile.readlines()
   emnfile.close()
   passed_sections=[]
   current_section=""
   section_counter=0
   for emnline in emnlines:
       emnrecords=split_records(emnline)
       if len( emnrecords )==0 : continue
       if len( emnrecords[0] )>4 and emnrecords[0][0:4]==".END":
          passed_sections.append(current_section)
          current_section=""
       elif emnrecords[0][0]==".":
          current_section=emnrecords[0]
          section_counter=0
       section_counter+=1
       if current_section==".HEADER"  and section_counter==2:
          emn_version=int(float(emnrecords[1]))
          Console.PrintMessage("Emn version: "+emnrecords[1]+"\n")
       if current_section==".HEADER"  and section_counter==3 and emnrecords[1]=="THOU":
          emn_unit=0.0254
          Console.PrintMessage("UNIT THOU\n" )
       if current_section==".HEADER"  and section_counter==3 and emnrecords[1]=="TNM":
          emn_unit=0.000010
          Console.PrintMessage("TNM\n" )
       if current_section==".BOARD_OUTLINE"  and section_counter==2:
          board_thickness=emn_unit*float(emnrecords[0])
          Console.PrintMessage("Found board thickness "+emnrecords[0]+"\n")
       if current_section==".BOARD_OUTLINE"  and section_counter>2:
          board_outline.append([int(emnrecords[0]),float(emnrecords[1])*emn_unit,float(emnrecords[2])*emn_unit,float(emnrecords[3])])
       if current_section==".DRILLED_HOLES"  and section_counter>1 and float(emnrecords[0])*emn_unit>ignore_hole_size:
          drills.append([float(emnrecords[0])*emn_unit,float(emnrecords[1])*emn_unit,float(emnrecords[2])*emn_unit])
       if current_section==".PLACEMENT"  and section_counter>1 and fmod(section_counter,2)==0:
          place_item=[]
          place_item.append(emnrecords[2]) #Reference designator
          place_item.append(emnrecords[1]) #Component part number
          place_item.append(emnrecords[0]) #Package name
       if current_section==".PLACEMENT"  and section_counter>1 and fmod(section_counter,2)==1:
          place_item.append(float(emnrecords[0])*emn_unit) #X
          place_item.append(float(emnrecords[1])*emn_unit) #Y
          place_item.append(float(emnrecords[emn_version])) #Rotation
          place_item.append(emnrecords[emn_version+1]) #Side
          place_item.append(emnrecords[emn_version+2]) #Place Status
          Console.PrintMessage(str(place_item)+"\n")
          placement.append(place_item)
   Console.PrintMessage("\n".join(passed_sections)+"\n")
   Console.PrintMessage("Proceed "+str(Process_board_outline(doc,board_outline,drills,board_thickness))+" outlines\n")
   placement.sort(key=lambda param: (param[IDF_sort],param[0]))
   process_emp(doc,filename,placement,board_thickness)
   place_steps(doc,placement,board_thickness)
