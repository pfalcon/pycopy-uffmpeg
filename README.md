MicroPython bindings for FFmpeg
===============================

These are bindings for FFmpeg video handling library using MicroPython's
`ffi` and `uctypes` modules. The up-to-date `uctypes` module is required,
until corresponding changes are merged upstream,
https://github.com/pfalcon/micropython can be used.

`uffmpeg` is the main module, the rest are sample applications. Two samples
are provided currently:

* decode_video.py - Decode video into serious of individual frames (saved
  as PPM images).
* play_video.py - Play video in the window using SDL2 (usdl2 MicroPython
  module is required, available at https://pypi.org/project/micropython-usdl2/
  or https://github.com/pfalcon/micropython-lib/tree/master/usdl2 .

(c) Paul Sokolovsky

Licensed under MIT license (note that FFmpeg project itself is licenced under
LGPL2.1 license).
