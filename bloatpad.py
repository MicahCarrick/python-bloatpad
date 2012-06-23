# coding=utf8
import sys
from gi.repository import Gtk, Gio, GLib, Gdk

MENU_XML = """
<interface>
  <menu id='app-menu'>
    <section>
      <item>
        <attribute name='label' translatable='yes'>_New Window</attribute>
        <attribute name='action'>app.new</attribute>
        <attribute name='accel'>&lt;Primary&gt;n</attribute>
      </item>
    </section>
    <section>
      <item>
        <attribute name='label' translatable='yes'>_About Bloatpad</attribute>
        <attribute name='action'>app.about</attribute>
      </item>
    </section>
    <section>
      <item>
        <attribute name='label' translatable='yes'>_Quit</attribute>
        <attribute name='action'>app.quit</attribute>
        <attribute name='accel'>&lt;Primary&gt;q</attribute>
      </item>
    </section>
  </menu>
  <menu id='menubar'>
    <submenu>
      <attribute name='label' translatable='yes'>_Edit</attribute>
      <section>
        <item>
          <attribute name='label' translatable='yes'>_Copy</attribute>
          <attribute name='action'>win.copy</attribute>
          <attribute name='accel'>&lt;Primary&gt;c</attribute>
        </item>
        <item>
          <attribute name='label' translatable='yes'>_Parse</attribute>
          <attribute name='action'>win.parse</attribute>
          <attribute name='accel'>&lt;Primary&gt;v</attribute>
        </item>
      </section>
    </submenu>
    <submenu>
      <attribute name='label' translatable='yes'>_View</attribute>
      <section>
        <item>
          <attribute name='label' translatable='yes'>_Fullscreen</attribute>
          <attribute name='action'>win.fullscreen</attribute>
          <attribute name='accel'>F11</attribute>
        </item>
      </section>
    </submenu>
  </menu>
</interface>
"""

class Window(Gtk.ApplicationWindow):
    def __init__(self, application):
        Gtk.ApplicationWindow.__init__(self, 
                                       application=application,
                                       default_width=640,
                                       default_height=480,
                                       title="Python Bloatpad")
        # create window ui
        
        toolbar = Gtk.Toolbar()
        
        button = Gtk.ToggleToolButton.new_from_stock(Gtk.STOCK_JUSTIFY_LEFT)
        button.set_detailed_action_name("win.justify::left")
        toolbar.add(button)
        
        button = Gtk.ToggleToolButton.new_from_stock(Gtk.STOCK_JUSTIFY_CENTER)
        button.set_detailed_action_name("win.justify::center")
        toolbar.add(button)
        
        button = Gtk.ToggleToolButton.new_from_stock(Gtk.STOCK_JUSTIFY_RIGHT)
        button.set_detailed_action_name("win.justify::right")
        toolbar.add(button)
        
        button = Gtk.SeparatorToolItem(draw=False, hexpand=True)
        button.set_expand(True)
        toolbar.add(button)
        
        switch = Gtk.Switch()
        switch.set_action_name("win.fullscreen")
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        box.add(Gtk.Label("Fullscreen:"))
        box.add(switch)
        button = Gtk.ToolItem()
        button.add(box)
        toolbar.add(button)

        scrolled = Gtk.ScrolledWindow(hexpand=True, vexpand=True)
        textview = Gtk.TextView()
        scrolled.add(textview)
        
        grid = Gtk.Grid()
        grid.attach(toolbar, 0, 0, 1, 1)
        grid.attach(scrolled, 0, 1, 1, 1) 
        
        self.add(grid)
        self.show_all()
        
        # Cannot use add_action_entries()
        # see https://bugzilla.gnome.org/show_bug.cgi?id=678655
        
        # setup actions
        action = Gio.SimpleAction(name="copy")
        action.connect("activate", self.copy, textview)        
        self.add_action(action)
        
        # is the UI XML "parse" intentional?
        action = Gio.SimpleAction(name="paste")
        action.connect("activate", self.paste, textview)        
        self.add_action(action)
        
        action = Gio.SimpleAction.new_stateful("fullscreen", None, 
                                               GLib.Variant('b', False))
        action.connect("activate", self.activate_toggle)
        action.connect("change-state", self.change_fullscreen_state)
        self.add_action(action)
        
        variant = GLib.Variant('s', "left")
        action = Gio.SimpleAction.new_stateful("justify", variant.get_type(), 
                                               variant)
        action.connect("activate", self.activate_radio)
        action.connect("change-state", self.change_justify_state, textview)
        self.add_action(action)

    def activate_radio(window, action, parameter, data=None):
        action.change_state(parameter)
    
    def change_justify_state(self, action, state, textview):
        if state.get_string() == "left":
            textview.set_justification(Gtk.Justification.LEFT)
        elif state.get_string() == "center":
            textview.set_justification(Gtk.Justification.CENTER)
        elif state.get_string() == "right":
            textview.set_justification(Gtk.Justification.RIGHT)
        else:
            return
        
        action.set_state(state);
            
    def activate_toggle(window, action, data=None):
        action.change_state(GLib.Variant('b', not action.get_state()))
    
    def change_fullscreen_state(self, action, state, data=None):
        if state.unpack():
            self.fullscreen()
        else:
            self.unfullscreen()
        action.set_state(state)
        
    def copy(self, action, state, textview):
        # textview added as user data
        clipboard = textview.get_clipboard(Gdk.SELECTION_CLIPBOARD)
        textview.get_buffer().copy_clipboard(clipboard)
    
    def paste(self, action, state, textview):
        # textview added as user data
        clipboard = textview.get_clipboard(Gdk.SELECTION_CLIPBOARD)
        textview.get_buffer().paste_clipboard(clipboard)
                                       
class BloatPad(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self, 
                                 application_id="com.micahcarrick.Test.bloatpad",
                                 flags=Gio.ApplicationFlags.HANDLES_OPEN,
                                 inactivity_timeout=30000,
                                 register_session=True)
        self.connect("startup", self.on_startup)     
        self.connect("activate", self.on_activate)

    def about_activated(self, action, data=None):
        dialog = Gtk.AboutDialog(program_name="Python Bloatpad",
                                 title="About Bloatpad",
                                 comments="Not much to say, really.")
        dialog.run()
        dialog.destroy()

    def new_window(self, file=None):
        window = Window(self)
        window.show()
    
    def on_activate(self, data=None):
        self.new_window()
        
    def on_startup(self, data=None):
    
        # Cannot use add_action_entries()
        # see https://bugzilla.gnome.org/show_bug.cgi?id=678655
        
        action = Gio.SimpleAction(name="new")
        action.connect("activate", lambda a,b: self.activate())
        self.add_action(action)
        
        action = Gio.SimpleAction(name="about")
        action.connect("activate", self.about_activated)
        self.add_action(action)
        
        action = Gio.SimpleAction(name="quit")
        action.connect("activate", lambda a,b: self.quit())
        self.add_action(action)
        
        builder = Gtk.Builder()
        builder.add_from_string(MENU_XML)
        self.set_menubar(builder.get_object("menubar"))
        self.set_app_menu(builder.get_object("app-menu"))


def install_excepthook():
    """ Make sure we exit when an unhandled exception occurs. """
    old_hook = sys.excepthook
    def new_hook(etype, evalue, etb):
        old_hook(etype, evalue, etb)
        while Gtk.main_level():
            Gtk.main_quit()
        sys.exit()
    sys.excepthook = new_hook
    
if __name__ == "__main__":
    install_excepthook()
    app = BloatPad()
    app.add_accelerator("F11", "win.fullscreen", None); # <-- does not work
    app.run(sys.argv)
    
