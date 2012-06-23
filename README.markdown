Python Bloatpad
===============

This is a Python port of the "Bloatpad" application used as an example for 
[GtkApplication](http://developer.gnome.org/gtk3/stable/GtkApplication.html) in 
the GTK+ Reference Manual.

I wrote it to get a grasp of the application menu and application menubar 
concepts. It works for the most part. There are a few issues:

1. The `F11` accellerator isn't working. Haven't looked into this yet
2. The GAction stuff has to be done manually rather than using 
   `add_action_entries()` like in the C version. I've submitted
   [Bug #678655](https://bugzilla.gnome.org/show_bug.cgi?id=678655)
3. Parsing command line arguments is not working. I've submitted 
   [Bug #678673](https://bugzilla.gnome.org/show_bug.cgi?id=678673)
