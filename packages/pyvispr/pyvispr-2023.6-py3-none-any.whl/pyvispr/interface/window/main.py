# Copyright CNRS/Inria/UniCA
# Contributor(s): Eric Debreuve (since 2017)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import dataclasses as dtcl
from typing import cast

import PyQt6.QtWidgets as wdgt

from pyvispr import __version__
from pyvispr.config.main import TITLE
from pyvispr.flow.visual.link import link_t
from pyvispr.flow.visual.node import node_t
from pyvispr.flow.visual.whiteboard import whiteboard_t
from pyvispr.interface.storage.loading import LoadWorkflowFromFile
from pyvispr.interface.storage.stowing import SaveWorkflow, SaveWorkflowAsScript
from pyvispr.interface.window.menu import AddEntryToMenu
from pyvispr.interface.window.messenger import CreateMessageCanal
from pyvispr.interface.window.node_list import node_list_wgt_t


@dtcl.dataclass(slots=True, repr=False, eq=False)
class pyflow_wdw_t(wdgt.QMainWindow):
    node_list_wgt: node_list_wgt_t = dtcl.field(init=False)
    whiteboard: whiteboard_t = dtcl.field(init=False)
    status_bar: wdgt.QStatusBar = dtcl.field(init=False)
    _ref_keeper: list = dtcl.field(init=False, default_factory=list)

    def __post_init__(self) -> None:
        """"""
        wdgt.QMainWindow.__init__(self)
        self.setWindowTitle(TITLE)

        self.node_list_wgt = node_list_wgt_t()
        self.whiteboard = whiteboard_t()

        CreateMessageCanal(self.node_list_wgt, "itemClicked", self.AddNodeToGraph)

        layout = wdgt.QGridLayout()
        layout.addWidget(self.node_list_wgt, 1, 1)
        layout.addWidget(self.node_list_wgt.filter_wgt, 2, 1)
        layout.addWidget(self.whiteboard, 1, 2, 2, 1)

        central = wdgt.QWidget(self)
        central.setLayout(layout)
        self.setCentralWidget(central)

        self.status_bar = self.statusBar()
        self._AddMenuBar()

    def _AddMenuBar(self) -> None:
        """"""
        menu_bar = self.menuBar()

        _ = _AddMenu(
            "py&Vispr",
            (
                ("Get Info", self.OpenAboutDialog),
                ("Configure", self.OpenConfiguration),
                None,
                ("&Quit", lambda checked_u: self.close(), {"shortcut": "Ctrl+Q"}),
            ),
            menu_bar,
            self,
        )

        menu = menu_bar.addMenu("&Workflow")
        AddEntryToMenu(
            menu,
            self,
            "&Run",
            self.Run,
            shortcut="Ctrl+R",
        )
        menu.addSeparator()
        AddEntryToMenu(
            menu,
            self,
            "&Save",
            lambda *_, **__: SaveWorkflow(self),
            shortcut="Ctrl+S",
        )
        AddEntryToMenu(
            menu,
            self,
            "L&oad",
            lambda *_, **__: LoadWorkflowFromFile(self),
            shortcut="Ctrl+O",
        )
        menu.addSeparator()
        AddEntryToMenu(
            menu, self, "Save As Script", lambda *_, **__: SaveWorkflowAsScript(self)
        )
        menu.addSeparator()
        submenu = menu.addMenu("Reset...")
        AddEntryToMenu(
            submenu,
            self,
            "Now",
            lambda checked_u: self.whiteboard.graph.functional.InvalidateAllNodes(),
        )
        submenu = menu.addMenu("Clear...")
        AddEntryToMenu(
            submenu, self, "Now", lambda checked_u: self.whiteboard.graph.Clear()
        )

        submenu = _AddMenu(
            "Show Info Boxes...",
            (
                (
                    "For Nodes (toggle)",
                    pyflow_wdw_t.ToggleShowInfoBoxesForNodes,
                    {"checkable": True, "checked": node_t.should_show_info_boxes},
                ),
                (
                    "For Links (toggle)",
                    pyflow_wdw_t.ToggleShowInfoBoxesForLinks,
                    {"checkable": True, "checked": link_t.should_show_info_boxes},
                ),
            ),
            None,
            self,
        )
        self._ref_keeper.append(submenu)
        _ = _AddMenu(
            "&View",
            (
                submenu,
                (
                    "Merged Ins/Outs (toggle)",
                    self.ToggleMergedInsOutsPresentation,
                    {"checkable": True},
                ),
            ),
            menu_bar,
            self,
        )

        _ = _AddMenu(
            "&Catalog",
            (("Refresh", lambda checked_u: self.node_list_wgt.Reload()),),
            menu_bar,
            self,
        )

    @staticmethod
    def ToggleShowInfoBoxesForNodes(checked: bool, /) -> None:
        """"""
        node_t.should_show_info_boxes = checked

    @staticmethod
    def ToggleShowInfoBoxesForLinks(checked: bool, /) -> None:
        """"""
        link_t.should_show_info_boxes = checked

    def ToggleMergedInsOutsPresentation(self, checked: bool, /):
        """"""
        if checked:
            wdgt.QMessageBox.about(
                cast(wdgt.QWidget, self), "Merged Ins/Outs", "Merged Ins/Outs: YES\n"
            )
        else:
            wdgt.QMessageBox.about(
                cast(wdgt.QWidget, self), "Merged Ins/Outs", "Merged Ins/Outs: NO\n"
            )

    def AddNodeToGraph(self, item: wdgt.QListWidgetItem, /) -> None:
        """"""
        self.whiteboard.graph.AddNode(item.text())

    def Run(self) -> None:
        """
        Calling self.whiteboard.graph.Run() directly from the menu will not work anymore if the graph changes.
        """
        self.whiteboard.graph.Run()

    def OpenAboutDialog(self, _: bool, /) -> None:
        """"""
        wdgt.QMessageBox.about(
            cast(wdgt.QWidget, self),
            "About pyVispr",
            f"pyVispr {__version__}\n"
            f"Nodes:{self.whiteboard.graph.nodes.__len__()}/{self.whiteboard.graph.functional.__len__()}\n"
            f"Links:{self.whiteboard.graph.links.__len__()}",
        )

    def OpenConfiguration(self, _: bool, /) -> None:
        """"""
        wdgt.QMessageBox.about(
            cast(wdgt.QWidget, self),
            "pyVispr Configuration",
            "No configuration options yet\n",
        )


def _AddMenu(
    name: str,
    entries: tuple,
    parent_menu: wdgt.QMenuBar | wdgt.QMenu | None,
    parent_widget: wdgt.QWidget,
    /,
) -> wdgt.QMenu:
    """"""
    if parent_menu is None:
        output = wdgt.QMenu(name)
    else:
        output = parent_menu.addMenu(name)

    for entry in entries:
        if entry is None:
            output.addSeparator()
        elif isinstance(entry, wdgt.QMenu):
            output.addMenu(entry)
        else:
            if isinstance(entry[-1], dict):
                args = entry[:-1]
                kwargs = entry[-1]
            else:
                args = entry
                kwargs = {}
            AddEntryToMenu(output, parent_widget, *args, **kwargs)

    return output
