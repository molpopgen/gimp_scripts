# My collection of GIMP plugins

A collection of Python plugins for [GIMP](http://www.gimp.org).

These are tested/used with version 2.10.

To install, copy them into the correct location for your user.  For example:

```sh
cp foo.py ~/.config/GIMP/2.10/plug-ins
```

Make sure that they are executable!

Also, be sure to restart GIMP after installing any plugins.  There is no "refresh scripts" option that works for Python
plugins.

## "Hacker hints"

When editing GIMP plugins, it may be preferable to have a symbolic link from your GIMP plugin folder to the source file
in your git repo.  The reason is that testing the script requires that it be installed, and it is highly unlikely that
your plugin folder is a repo.  Using symbolic links lets you edit/commit/stash, etc., while keeping the plugin
installed.

## setup_luminosity_mask.py

Filters -> Generic -> Luminosity mask setup

This script automates the procedure laid out in this [tutorial](https://www.gimp.org/tutorials/Luminosity_Masks/) and in
this [video](https://www.youtube.com/watch?v=3Izcmh1ZB4U&vl=en).

Any resizing, etc., of the image should be applied prior to running this script.

The final result is three layer groups (darks, lights, and mid-tones).

This plugin can consume a lot of RAM on big images!

This script is similar in scope to one by Pat David avaiable
[here](https://github.com/pixlsus/GIMP-Scripts/blob/master/sg-luminosity-masks.scm).  His script works via a different
set of operations resulting in the same masks.  The major difference is that his does not group them as layer masks in
layer groups.
