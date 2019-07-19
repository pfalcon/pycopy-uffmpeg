Pycopy bindings for FFmpeg
==========================

These are bindings for FFmpeg video handling library using Pycopy's
`ffi` and `uctypes` modules. Pycopy is a lightweight Python implementation,
https://github.com/pfalcon/pycopy .

`uffmpeg` is the main module, the rest are sample applications. Two samples
are provided currently:

* decode_video.py - Decode video into serious of individual frames (saved
  as PPM images).
* play_video.py - Play video in the window using SDL2 (the `usdl2` Pycopy
  module is required, available at https://pypi.org/project/pycopy-usdl2/
  or https://github.com/pfalcon/pycopy-lib/tree/master/usdl2 .

(c) Paul Sokolovsky

Licensed under MIT license (note that FFmpeg project itself is licenced under
LGPL2.1 license).
