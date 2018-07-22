# My collection of GIMP plugins

A collection of Python plugins for [GIMP](http://www.gimp.org).

These are tested/used with version 2.10.

To install, copy them into the correct location for your user.  For example:

```sh
cp foo.py ~/.config/GIMP/2.10/plug-ins
```

Make sure that they are executable!

## setup_luminosity_mask.py

Filters -> Generic -> Luminosity mask setup

This script automates the procedure laid out in this [tutorial](https://www.gimp.org/tutorials/Luminosity_Masks/) and in
this [video](https://www.youtube.com/watch?v=3Izcmh1ZB4U&vl=en).

Any resizing, etc., of the image should be applied prior to running this script.

The final result is three layer groups (darks, lights, and mid-tones).

This plugin can consume a lot of RAM on big images!
