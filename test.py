#! /usr/bin/env python

import gtk

import cream.ipc

class MelangeControl:

    def __init__(self):

        self.interface = gtk.Builder()
        self.interface.add_from_file('interface.glade')

        self.treeview = self.interface.get_object('treeview')
        self.liststore = self.interface.get_object('liststore')

        self.interface.get_object('button_close').connect('clicked', lambda *x: gtk.main_quit())
        self.interface.get_object('button_add').connect('clicked', lambda *x: self.launch())

        self.interface.get_object('window').show_all()

        self.melange = cream.ipc.get_object('org.cream.melange')

        widgets = self.melange.list_widgets()
        for k,w in widgets.iteritems():
            pb = gtk.gdk.pixbuf_new_from_file('melange.png').scale_simple(32, 32, gtk.gdk.INTERP_HYPER)
            label = "<b>{0}</b>\n{1}".format(w['name'], w['comment'])
            self.liststore.append((w['hash'], w['path'], w['name'], w['comment'], pb, label))


    def launch(self):

        selection = self.treeview.get_selection()
        model, iter = selection.get_selected()

        id = model.get_value(iter, 0)
        self.melange.load_widget(id)


if __name__ == '__main__':
    MelangeControl()
    gtk.main()
