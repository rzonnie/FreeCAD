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

__title__ = "FreeCAD FEM constraint current density task panel for the document object"
__author__ = "Markus Hovorka, Bernd Hahnebach, Remi Jonkman"
__url__ = "https://www.freecadweb.org"

## @package task_constraint_currentdensity
#  \ingroup FEM
#  \brief task panel for constraint current density object

import FreeCAD
import FreeCADGui
from FreeCAD import Units

from femguiutils import selection_widgets
from femtools import femutils
from femtools import membertools


class _TaskPanel(object):

    def __init__(self, obj):
        self._obj = obj
        self._refWidget = selection_widgets.BoundarySelector()
        self._refWidget.setReferences(obj.References)
        self._paramWidget = FreeCADGui.PySideUic.loadUi(
            FreeCAD.getHomePath() + "Mod/Fem/Resources/ui/ConstraintCurrentDensity.ui")
        self._initParamWidget()
        self.form = [self._refWidget, self._paramWidget]
        analysis = obj.getParentGroup()
        self._mesh = None
        self._part = None
        if analysis is not None:
            self._mesh = membertools.get_single_member(analysis, "Fem::FemMeshObject")
        if self._mesh is not None:
            self._part = femutils.get_part_to_mesh(self._mesh)
        self._partVisible = None
        self._meshVisible = None

    def open(self):
        if self._mesh is not None and self._part is not None:
            self._meshVisible = self._mesh.ViewObject.isVisible()
            self._partVisible = self._part.ViewObject.isVisible()
            self._mesh.ViewObject.hide()
            self._part.ViewObject.show()

    def reject(self):
        self._restoreVisibility()
        FreeCADGui.ActiveDocument.resetEdit()
        return True

    def accept(self):
        if self._obj.References != self._refWidget.references():
            self._obj.References = self._refWidget.references()
        self._applyWidgetChanges()
        self._obj.Document.recompute()
        FreeCADGui.ActiveDocument.resetEdit()
        self._restoreVisibility()
        return True

    def _restoreVisibility(self):
        if self._mesh is not None and self._part is not None:
            if self._meshVisible:
                self._mesh.ViewObject.show()
            else:
                self._mesh.ViewObject.hide()
            if self._partVisible:
                self._part.ViewObject.show()
            else:
                self._part.ViewObject.hide()

    def _initParamWidget(self):
        unit = "A*mm^-2"
        q = Units.Quantity("{} {}".format(self._obj.CurrentDensity, unit))
        self._paramWidget.currentDensityBox.setChecked(False)
        self._paramWidget.currentDensityTxt.setText(q.UserString)

    def _applyWidgetChanges(self):
        unit = "A*mm^-2"
        quantity = None
        try:
            quantity = Units.Quantity(self._paramWidget.currentDensityTxt.text())
            if quantity is not None:
                self._obj.CurrentDensity = quantity.getValueAs(unit).Value
        except ValueError:
            FreeCAD.Console.PrintMessage(
                "Wrong input. Not recognised input: '{}' "
                "Vector potential has not been set.\n"
                .format(self._paramWidget.currentDensityTxt.text())
            )
