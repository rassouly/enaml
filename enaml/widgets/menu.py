#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
from atom.api import Bool, Typed, ForwardTyped, Unicode, observe

from enaml.core.declarative import d_

from .action import Action
from .action_group import ActionGroup
from .toolkit_object import ToolkitObject, ProxyToolkitObject


class ProxyMenu(ProxyToolkitObject):
    """ The abstract definition of a proxy Menu object.

    """
    #: A reference to the Control declaration.
    declaration = ForwardTyped(lambda: Menu)

    def set_title(self, title):
        raise NotImplementedError

    def set_enabled(self, enabled):
        raise NotImplementedError

    def set_visible(self, visible):
        raise NotImplementedError

    def set_context_menu(self, context):
        raise NotImplementedError


class Menu(ToolkitObject):
    """ A widget used as a menu in a MenuBar.

    """
    #: The title to use for the menu.
    title = d_(Unicode())

    #: Whether or not the menu is enabled.
    enabled = d_(Bool(True))

    #: Whether or not the menu is visible.
    visible = d_(Bool(True))

    #: Whether this menu should behave as a context menu for its parent.
    context_menu = d_(Bool(False))

    #: A reference to the ProxyMenu object.
    proxy = Typed(ProxyMenu)

    @property
    def items(self):
        """ A read only property for the items declared on the menu.

        A menu item is one of Action, ActionGroup, or Menu.

        """
        isinst = isinstance
        allowed = (Action, ActionGroup, Menu)
        return [child for child in self.children if isinst(child, allowed)]

    #--------------------------------------------------------------------------
    # Observers
    #--------------------------------------------------------------------------
    @observe(('title', 'enabled', 'visible', 'context_menu'))
    def _update_proxy(self, change):
        """ An observer which updates the proxy when the menu changes.

        """
        # The superclass implementation is sufficient.
        super(Menu, self)._update_proxy(change)