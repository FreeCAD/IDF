# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2012 Milos Koutny <milos.koutny@gmail.com>
# SPDX-FileNotice: Part of the IDF addon.

from FreeCAD import Console , Vector
from Part import LineSegment , makeCircle , Shape , Wire , Face , Arc

from .Helper import Per_point , mid_point


def Process_board_outline(doc,board_outline,drills,board_thickness):
    """Process_board_outline(doc,board_outline,drills,board_thickness)-> number processed loops

        adds emn geometry from emn file"""
    vertex_index=-1; #presume no vertex
    lines=-1 #presume no lines
    out_shape=[]
    out_face=[]
    for point in board_outline:
       vertex=Vector(point[1],point[2],0)
       vertex_index+=1
       if vertex_index==0:
          lines=point[0]
       elif lines==point[0]:
           if point[3]!=0 and point[3]!=360:
              out_shape.append(Arc(prev_vertex,mid_point(prev_vertex,vertex,point[3]),vertex))
              Console.PrintMessage("mid point "+str(mid_point)+"\n")
           elif point[3]==360:
              per_point=Per_point(prev_vertex,vertex)
              out_shape.append(Arc(per_point,mid_point(per_point,vertex,point[3]/2),vertex))
              out_shape.append(Arc(per_point,mid_point(per_point,vertex,-point[3]/2),vertex))
           else:
              out_shape.append(LineSegment(prev_vertex,vertex))
       else:
          out_shape=Shape(out_shape)
          out_shape=Wire(out_shape.Edges)
          out_face.append(Face(out_shape))
          out_shape=[]
          vertex_index=0
          lines=point[0]
       prev_vertex=vertex
    if lines!=-1:
      out_shape=Shape(out_shape)
      out_shape=Wire(out_shape.Edges)
      out_face.append(Face(out_shape))
      outline=out_face[0]
      Console.PrintMessage("Added outline\n")
      if len(out_face)>1:
        for otl_cut in out_face[1: ]:
          outline=outline.cut(otl_cut)
          Console.PrintMessage("Cutting shape inside outline\n")
      for drill in drills:
        Console.PrintMessage("Cutting hole inside outline\n")
        out_shape=makeCircle(drill[0]/2, Vector(drill[1],drill[2],0))
        out_shape=Wire(out_shape.Edges)
        outline=outline.cut(Face(out_shape))
      doc_outline=doc.addObject("Part::Feature","Board_outline")
      doc_outline.Shape=outline.extrude(Vector(0,0,-board_thickness))
      grp=doc.addObject("App::DocumentObjectGroup", "Board_Geoms")
      grp.addObject(doc_outline)
      doc.Board_outline.ViewObject.ShapeColor=(0.0, 0.5, 0.0, 0.0)
    return lines+1
