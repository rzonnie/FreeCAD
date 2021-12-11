# ***************************************************************************
# *   Copyright (c) 2017 Remi Jonkman <rb.jonkman@outlook.com>              *
# *                                                                         *
# *   This file is part of the FreeCAD CAx development system.              *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

__title__ = "FreeCAD FEM solver Elmer equation object to calculate fields related to elektromagnetism"
__author__ = "Remi Jonkman"
__url__ = "https://www.freecadweb.org"

## \addtogroup FEM
#  @{

from femtools import femutils
from . import nonlinear
from ... import equationbase


def create(doc, name="MagnetoDynamicCalculateField"):
    return femutils.createObject(
        doc, name, Proxy, ViewProxy)


class Proxy(nonlinear.Proxy, equationbase.MagnetoDynamicCalculateFieldProxy):

    Type = "Fem::EquationElmerMagnetoDynamicCalculateField"

    def __init__(self, obj):
        super(Proxy, self).__init__(obj)
        obj.Priority = 99

        obj.addProperty(
            "App::PropertyBool",
            "CalculateMagneticField",
            "Calculate Magnetic Field",
            ""
        )

        obj.addProperty(
            "App::PropertyBool",
            "CalculateElectricField",
            "Calculate Electric Field",
            ""
        )

        obj.addProperty(
            "App::PropertyBool",
            "CalculateCurrentDensity",
            "Calculate Current Density",
            ""
        )


class ViewProxy(nonlinear.ViewProxy, equationbase.MagnetoDynamicCalculateFieldViewProxy):
    pass


##  @}
