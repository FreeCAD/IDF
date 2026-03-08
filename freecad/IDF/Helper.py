# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2012 Milos Koutny <milos.koutny@gmail.com>
# SPDX-FileNotice: Part of the IDF addon.

from FreeCAD import Rotation , Vector
from math import radians , hypot , atan2 , sin ,  cos , pi


def mid_point(prev_vertex,vertex,angle):
    """mid_point(prev_vertex,vertex,angle)-> mid_vertex

       returns mid point on arc of angle between prev_vertex and vertex"""
    angle=radians(angle/2)
    basic_angle=atan2(vertex.y-prev_vertex.y,vertex.x-prev_vertex.x)-pi/2
    shift=(1-cos(angle))*hypot(vertex.y-prev_vertex.y,vertex.x-prev_vertex.x)/2/sin(angle)
    midpoint=Vector((vertex.x+prev_vertex.x)/2+shift*cos(basic_angle),(vertex.y+prev_vertex.y)/2+shift*sin(basic_angle),0)
    return midpoint


def toQuaternion(heading, attitude,bank): # rotation heading=around Y, attitude =around Z,  bank attitude =around X
    """toQuaternion(heading, attitude,bank)->FreeCAD.Base.Rotation(Quternion)"""
    c1 = cos(heading/2)
    s1 = sin(heading/2)
    c2 = cos(attitude/2)
    s2 = sin(attitude/2)
    c3 = cos(bank/2)
    s3 = sin(bank/2)
    c1c2 = c1*c2
    s1s2 = s1*s2
    w = c1c2*c3 - s1s2*s3
    x = c1c2*s3 + s1s2*c3
    y = s1*c2*c3 + c1*s2*s3
    z = c1*s2*c3 - s1*c2*s3
    return  Rotation(x,y,z,w)

def Per_point(prev_vertex,vertex):
    """Per_point(center,vertex)->per point

       returns opposite perimeter point of circle"""
    perpoint=Vector(2*prev_vertex.x-vertex.x,2*prev_vertex.y-vertex.y,0)
    return perpoint
