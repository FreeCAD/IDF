# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2012 Milos Koutny <milos.koutny@gmail.com>
# SPDX-FileNotice: Part of the IDF addon.

from FreeCAD import Console , Vector
from Part import LineSegment , Shape , Wire , Face , Arc

from .Helper import Per_point , mid_point


def Process_comp_outline(doc,comp_outline,comp_height):
    """Process_comp_outline(doc,comp_outline,comp_height)->part shape
       Create solid component shape base on its outline"""
    vertex_index=-1; #presume no vertex
    out_shape=[]
    if comp_outline==[]:  #force 0.2mm circle shape for components without place outline definition
       comp_outline.append([0.0,0.0,0.0])
       comp_outline.append([0.1,0.0,360.0])
    for point in comp_outline:
       vertex=Vector(point[0],point[1],0)
       vertex_index+=1
       if vertex_index>0:
         if point[2]!=0 and point[2]!=360:
            out_shape.append(Arc(prev_vertex,mid_point(prev_vertex,vertex,point[2]),vertex))
            Console.PrintMessage("mid point "+str(mid_point)+"\n")
         elif point[2]==360:
            per_point=Per_point(prev_vertex,vertex)
            out_shape.append(Arc(per_point,mid_point(per_point,vertex,point[2]/2),vertex))
            out_shape.append(Arc(per_point,mid_point(per_point,vertex,-point[2]/2),vertex))
         else:
            out_shape.append(LineSegment(prev_vertex,vertex))
       prev_vertex=vertex
    out_shape=Shape(out_shape)
    out_shape=Wire(out_shape.Edges)
    out_shape=Face(out_shape)
    out_shape=out_shape.extrude(Vector(0,0,comp_height))
    return out_shape