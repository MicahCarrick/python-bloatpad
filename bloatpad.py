# coding=utf8
import sys
from gi.repository import Gtk, Gio, GLib

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
                                       
        # Gtk.ActionMap.add_action_entries() sure would be nice....
        # do we really want to be playing with GVariants in python?
        action = Gio.SimpleAction.new_stateful("fullscreen", None, 
                                               GLib.Variant("b", False))
        action.connect("activate", self.activate_toggle)
        action.connect("change-state", self.change_fullscreen_state)
        self.add_action(action)
    
    def activate_toggle(window, action, data=None):
        action.change_state(GLib.Variant('b', not action.get_state()))
    
    def change_fullscreen_state(self, action, state, data=None):
        if state.unpack():
            self.fullscreen()
        else:
            self.unfullscreen()
        action.set_state(state)
        
    def on_cut_activate(self, action, data=None):
        print("cut")
                                       
class BloatPad(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self, 
                                 application_id="com.micahcarrick.Test.bloatpad",
                                 flags=Gio.ApplicationFlags.HANDLES_OPEN,
                                 #inactivity_timeout=30000,
                                 register_session=True)
        self.connect("startup", self.on_startup)     
        self.connect("activate", self.on_activate)

    def about_activated(self, action, data=None):
        Gtk.AboutDialog(program_name="Python Bloatpad",
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
        """
        Using self.add_action_entries() is not playing nice with introspection. 
        I tried patching gi/overrides/Gio.py but the GLib.Variant stuff went 
        over my head. I think a few of the GAction related classes need to be
        tweaked. I need to submit a bug.
        
        For now, manually creating each action will work.
        """
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
    app.run(sys.argv)
    
