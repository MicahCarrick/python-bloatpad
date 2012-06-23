Python Bloatpad
===============

This is a Python port of the "Bloatpad" application used as an example for 
[GtkApplication](http://developer.gnome.org/gtk3/stable/GtkApplication.html) in 
the GTK+ Reference Manual.

I wrote it to get a grasp of the application menu and application menubar 
concepts. It works for the most part. There are a few issues:

1. The F11 accellerator isn't working. Note sure why. 
2. The GAction stuff seems a bit wonky. Not very pythonic. I've submitted
   [Bug #678655](https://bugzilla.gnome.org/show_bug.cgi?id=678655).
