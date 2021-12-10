# ***************************************************************************
# *   Copyright (c) 2017 Markus Hovorka <m.hovorka@live.de>                 *
# *   Copyright (c) 2020 Bernd Hahnebach <bernd@bimstatik.org>              *
# *   Copyright (c) 2021 Remi Jonkman <rb.jonkman@outlook.com               *
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

__title__ = "FreeCAD FEM constraint body current density document object"
__author__ = "Markus Hovorka, Bernd Hahnebach, Remi Jonkman"
__url__ = "https://www.freecadweb.org"

## @package constraint_bodycurrentdensity
#  \ingroup FEM
#  \brief constraint body current density object

from . import base_fempythonobject


class ConstraintBodyCurrentDensity(base_fempythonobject.BaseFemPythonObject):

    Type = "Fem::ConstraintBodyCurrentDensity"

    def __init__(self, obj):
        super(ConstraintBodyCurrentDensity, self).__init__(obj)

        obj.addProperty(
            "App::PropertyFloat",
            "CurrentDensity",
            "Base",
            "Current density"
        )
