# preferences.py
#
# Copyright 2022 mirkobrombin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundationat version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import time
from gi.repository import Gtk, Gio, GLib, Adw

from vanilla_first_setup.utils.run_async import RunAsync


@Gtk.Template(resource_path='/io/github/vanilla-os/FirstSetup/gtk/layout-preferences.ui')
class VanillaLayoutPreferences(Adw.Bin):
    __gtype_name__ = 'VanillaLayoutPreferences'

    status_page = Gtk.Template.Child()
    prefs_list = Gtk.Template.Child()
    btn_next = Gtk.Template.Child()

    def __init__(self, window, distro_info, key, step, **kwargs):
        super().__init__(**kwargs)
        self.__window = window
        self.__distro_info = distro_info
        self.__key = key
        self.__step = step
        self.__register_widgets = []
        self.__build_ui()

        # signals
        self.btn_next.connect("clicked", self.__window.next)

    def __build_ui(self):
        self.status_page.set_icon_name(self.__step["icon"])
        self.status_page.set_title(self.__step["title"])
        self.status_page.set_description(self.__step["description"])

        for item in self.__step["preferences"]:
            _action_row = Adw.ActionRow(
                title=item["title"],
                subtitle=item.get("subtitle", "")
            )
            _switcher = Gtk.Switch()
            _switcher.set_active(item.get("default", False))
            _switcher.set_valign(Gtk.Align.CENTER)
            _action_row.add_suffix(_switcher)

            self.prefs_list.add(_action_row)

            self.__register_widgets.append((item["id"], _switcher))

    def get_finals(self):
        finals = {"vars": {}, "funcs": [x for x in self.__step["final"]]}

        for _id, switcher in self.__register_widgets:
            finals["vars"][_id] = switcher.get_active()

        return finals
