#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
from PyQt4.QtGui import QCalendarWidget

from atom.api import Typed

from enaml.widgets.calendar import ProxyCalendar

from .qt_bounded_date import QtBoundedDate, CHANGED_GUARD, as_qdate, as_pydate


class QtCalendar(QtBoundedDate, ProxyCalendar):
    """ A Qt implementation of an Enaml ProxyCalendar.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(QCalendarWidget)

    #--------------------------------------------------------------------------
    # Initialization
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the calender widget.

        """
        self.widget = QCalendarWidget(self.parent_widget())

    def init_widget(self):
        """ Initialize the widget.

        """
        super(QtCalendar, self).init_widget()
        self.widget.activated.connect(self.on_date_changed)

    #--------------------------------------------------------------------------
    # Abstract API Implementation
    #--------------------------------------------------------------------------
    def get_date(self):
        """ Return the current date in the control.

        Returns
        -------
        result : date
            The current control date as a Python date object.

        """
        return as_pydate(self.widget.selectedDate())

    def set_minimum(self, date):
        """ Set the widget's minimum date.

        Parameters
        ----------
        date : QDate
            The QDate object to use for setting the minimum date.

        """
        self.widget.setMinimumDate(as_qdate(date))

    def set_maximum(self, date):
        """ Set the widget's maximum date.

        Parameters
        ----------
        date : QDate
            The QDate object to use for setting the maximum date.

        """
        self.widget.setMaximumDate(as_qdate(date))

    def set_date(self, date):
        """ Set the widget's current date.

        Parameters
        ----------
        date : QDate
            The QDate object to use for setting the date.

        """
        self._guard |= CHANGED_GUARD
        try:
            self.widget.setSelectedDate(as_qdate(date))
        finally:
            self._guard &= ~CHANGED_GUARD