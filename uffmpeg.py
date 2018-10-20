# The MIT License (MIT)
#
# Copyright (c) 2018 Paul Sokolovsky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import ffi
import uctypes
from ucollections import OrderedDict


NULL = None

AV_NOPTS_VALUE = 0x8000000000000000
AV_CODEC_ID_H264 = 28


def AVERROR(e):
    assert e > 0
    return -e

def FFERRTAG(a, b, c, d):
    return -(ord(a) | ord(b) << 8 | ord(c) << 16 | ord(d) << 24)

AVERROR_EOF = FFERRTAG('E','O','F',' ')


_avcodec = ffi.open("libavcodec.so.57")

avcodec_register_all = _avcodec.func("i", "avcodec_register_all", "")
av_packet_alloc = _avcodec.func("P", "av_packet_alloc", "")
avcodec_find_decoder = _avcodec.func("P", "avcodec_find_decoder", "i")
av_parser_init = _avcodec.func("P", "av_parser_init", "i")
avcodec_alloc_context3 = _avcodec.func("P", "avcodec_alloc_context3", "P")
avcodec_open2 = _avcodec.func("i", "avcodec_open2", "PPP")
av_frame_alloc = _avcodec.func("P", "av_frame_alloc", "")

AVPacket_layout = OrderedDict({
    "buf": (uctypes.PTR, uctypes.VOID),
    "pts": uctypes.INT64,
    "dts": uctypes.INT64,
    "data": (uctypes.PTR, uctypes.UINT8),
    "size": uctypes.INT32,
    # There're more, but for now we don't care
})
uctypes.calc_offsets(AVPacket_layout)
print(AVPacket_layout)

print("sizeof(AVPacket_layout) =", uctypes.sizeof(AVPacket_layout))

AV_NUM_DATA_POINTERS = 8

AVFrame_layout = OrderedDict({
    "data": (uctypes.ARRAY, AV_NUM_DATA_POINTERS, (uctypes.PTR, uctypes.UINT8)),
    "linesize": (uctypes.ARRAY, AV_NUM_DATA_POINTERS | uctypes.INT32),
    "extended_data": (uctypes.PTR, uctypes.VOID),
    "width": uctypes.INT32,
    "height": uctypes.INT32,
    "nb_samples": uctypes.INT32,
    "format": uctypes.INT32,
    "key_frame": uctypes.INT32,
    "pict_type": uctypes.INT32,
})
uctypes.calc_offsets(AVFrame_layout)
print("sizeof(AVPacket_layout) =", uctypes.sizeof(AVFrame_layout))

av_parser_parse2 = _avcodec.func("i", "av_parser_parse2", "PPppPiQQQ")
avcodec_send_packet = _avcodec.func("i", "avcodec_send_packet", "PP")
avcodec_receive_frame = _avcodec.func("i", "avcodec_receive_frame", "PP")
