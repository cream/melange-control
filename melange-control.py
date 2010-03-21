#! /usr/bin/env python
# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.

import os

import gtk

import cream
import cream.gui.builder
import cream.ipc

class MelangeControl(cream.Module):

    def __init__(self):

        cream.Module.__init__(self)

        self.interface = cream.gui.builder.GtkBuilderInterface('interface.glade')

        self.interface.window.connect('destroy', lambda *x: self.quit())
        self.interface.button_close.connect('clicked', lambda *x: self.quit())
        self.interface.button_add.connect('clicked', lambda *x: self.launch())

        self.interface.window.show_all()

        self.melange = cream.ipc.get_object('org.cream.melange')

        widgets = self.melange.list_widgets()
        for k, w in widgets.iteritems():
            if w.has_key('icon'):
                p = os.path.join(w['path'], w['icon'])
                pb = gtk.gdk.pixbuf_new_from_file(p).scale_simple(28, 28, gtk.gdk.INTERP_HYPER)
            else:
                pb = gtk.gdk.pixbuf_new_from_file('melange.png').scale_simple(28, 28, gtk.gdk.INTERP_HYPER)
            label = "<b>{0}</b>\n{1}".format(w['name'], w['comment'])
            self.interface.liststore.append((w['hash'], w['filepath'], w['name'], w['comment'], pb, label))


    def launch(self):

        selection = self.interface.treeview.get_selection()
        model, iter = selection.get_selected()

        id = model.get_value(iter, 2)
        self.melange.load_widget(id, False, False)


if __name__ == '__main__':
    from dbus.exceptions import DBusException
    try:
        melange_control = MelangeControl()
    except DBusException:
        raise RuntimeError("Could not connect to Melange via DBus.")
    else:
        melange_control.main()
