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

__title__ = "FreeCAD FEM constraint magnetostatic vector potential task panel for the document object"
__author__ = "Markus Hovorka, Bernd Hahnebach, Remi Jonkman"
__url__ = "https://www.freecadweb.org"

## @package task_constraint_magnetostaticvectorpotential
#  \ingroup FEM
#  \brief task panel for constraint magnetostatic vector potential object

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
            FreeCAD.getHomePath() + "Mod/Fem/Resources/ui/MagnetostaticVectorPotential.ui")
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
        unit = "V*s/(m^1)"
        q = Units.Quantity("{} {}".format(self._obj.VectorPotential, unit))
        self._paramWidget.vectorPotentialTxt.setText(q.UserString)
        self._paramWidget.vectorPotentialBox.setChecked(not self._obj.VectorPotentialEnabled)
        self._paramWidget.vectorPotentialConstantBox.setChecked(self._obj.VectorPotentialConstant)
        self._paramWidget.magneticInfinityBox.setChecked(self._obj.MagneticInfinity)

    def _applyWidgetChanges(self):
        unit = "V*s/(m^1)"
        self._obj.VectorPotentialEnabled = \
            not self._paramWidget.vectorPotentialBox.isChecked()
        if self._obj.VectorPotentialEnabled:
            # if the input widget shows not a green hook, but the user presses ok
            # we could run into a syntax error on getting the quantity, try mV
            quantity = None
            try:
                quantity = Units.Quantity(self._paramWidget.vectorPotentialTxt.text())
            except ValueError:
                FreeCAD.Console.PrintMessage(
                    "Wrong input. OK has been triggered without a green hook "
                    "in the input field. Not recognised input: '{}' "
                    "Vector potential has not been set.\n"
                    .format(self._paramWidget.vectorPotentialTxt.text())
                )
            if quantity is not None:
                self._obj.VectorPotential = quantity.getValueAs(unit).Value

        self._obj.VectorPotentialConstant = self._paramWidget.vectorPotentialConstantBox.isChecked()
        self._obj.MagneticInfinity = self._paramWidget.magneticInfinityBox.isChecked()
