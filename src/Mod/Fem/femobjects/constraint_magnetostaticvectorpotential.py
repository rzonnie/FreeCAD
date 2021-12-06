# ***************************************************************************
# *   Copyright (c) 2017 Markus Hovorka <m.hovorka@live.de>                 *
# *   Copyright (c) 2020 Bernd Hahnebach <bernd@bimstatik.org>              *
# *   Copyright (c) 2021 Remi Jonkman <rb.jonkman@outlook.com>              *
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

__title__ = "FreeCAD FEM constraint magnetostatic vector potential document object"
__author__ = "Markus Hovorka, Bernd Hahnebach, Remi Jonkman"
__url__ = "https://www.freecadweb.org"

## @package constraint_magnetostaticvectorpotential
#  \ingroup FEM
#  \brief constraint magnetostatic vector potential object

from . import base_fempythonobject


class ConstraintMagnetostaticVectorPotential(base_fempythonobject.BaseFemPythonObject):

    Type = "Fem::ConstraintMagnetostaticVectorPotential"

    def __init__(self, obj):
        super(ConstraintMagnetostaticVectorPotential, self).__init__(obj)
        self.add_properties(obj)

    def onDocumentRestored(self, obj):
        self.add_properties(obj)

    def add_properties(self, obj):
        if not hasattr(obj, "VectorPotential"):
            obj.addProperty(
                "App::PropertyFloat", "VectorPotential",
                "Parameter", "Vector Potential"
            ),
            obj.VectorPotential = 0.0

        if not hasattr(obj, "VectorPotentialEnabled"):
            obj.addProperty(
                "App::PropertyBool", "VectorPotentialEnabled",
                "Parameter", "Vector Potential Enabled"
            ),
            obj.VectorPotentialEnabled = False

        if not hasattr(obj, "VectorPotentialConstant"):
            obj.addProperty(
                "App::PropertyBool", "VectorPotentialConstant",
                "Parameter", "Vector Potential Constant"
            ),
            obj.VectorPotentialConstant = False

        if not hasattr(obj, "MagneticInfinity"):
            obj.addProperty(
                "App::PropertyBool", "MagneticInfinity",
                "Parameter", "Magnetic Infinity"
            ),
            obj.MagneticInfinity = False